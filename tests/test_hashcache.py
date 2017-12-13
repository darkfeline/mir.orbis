# Copyright (C) 2017 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from unittest import mock

from mir.orbis import hashcache


@mock.patch.dict(os.environ)
def test_connect(tmpdir):
    os.environ['XDG_CACHE_HOME'] = str(tmpdir)
    with hashcache.connect() as con:
        con.execute(
            """INSERT INTO sha256_cache
            (path, device, inode, mtime, size, hexdigest)
            VALUES (?, ?, ?, ?, ?, ?)""",
            ('/foo/bar', 48, 369494, 1513137496, 10,
             'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'))


def test_cachedir_default():
    with mock.patch.dict(os.environ):
        os.environ['HOME'] = '/home/yamada'
        os.environ.pop('XDG_CACHE_HOME', None)
        got = hashcache._cachedir()
    assert str(got) == '/home/yamada/.cache/mir.orbis'


def test_cachedir_explicit():
    with mock.patch.dict(os.environ):
        os.environ['HOME'] = '/home/yamada'
        os.environ['XDG_CACHE_HOME'] = '/tmp/cache'
        got = hashcache._cachedir()
    assert str(got) == '/tmp/cache/mir.orbis'
