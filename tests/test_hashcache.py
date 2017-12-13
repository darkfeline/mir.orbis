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
def test_hashcache(tmpdir):
    os.environ['XDG_CACHE_HOME'] = str(tmpdir)
    s = _stat_result(
        st_mode=33204,
        st_ino=369494,
        st_dev=48,
        st_nlink=1,
        st_uid=1007,
        st_gid=1007,
        st_size=10,
        st_atime=1513137496,
        st_mtime=1513137496,
        st_ctime=1513137498)
    with hashcache.connect() as con:
        hashcache.add_sha256(
            con, '/tmp/foo', s,
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
        got = hashcache.get_sha256(
            con, '/tmp/foo', s)
    assert got == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


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


class _stat_result:

    def __init__(self, **kwargs):
        self.__dict__ = kwargs
