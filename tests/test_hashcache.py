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

import pytest


@mock.patch.dict(os.environ)
def test_Cache_by_default_uses_xdg_cache_home(Cache, tmpdir):
    os.environ['XDG_CACHE_HOME'] = str(tmpdir)
    with mock.patch('sqlite3.connect') as connect:
        with Cache():
            pass
        connect.assert_called_with(str(tmpdir.join('mir.orbis', 'hash.db')))


@mock.patch.dict(os.environ)
def test_Cache_by_default_uses_home(Cache, tmpdir):
    os.environ['HOME'] = str(tmpdir)
    os.environ.pop('XDG_CACHE_HOME', None)
    with mock.patch('sqlite3.connect') as connect:
        with Cache():
            pass
        connect.assert_called_with(str(tmpdir.join('.cache', 'mir.orbis', 'hash.db')))


def test_Cache(Cache, tmpdir):
    s1 = _stat_result(
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
    s2 = _stat_result(
        st_mode=33204,
        st_ino=369494,
        st_dev=48,
        st_nlink=1,
        st_uid=1007,
        st_gid=1007,
        st_size=11,
        st_atime=1513137496,
        st_mtime=1513137496,
        st_ctime=1513137498)
    with Cache(str(tmpdir.join('db'))) as c:
        c['/tmp/foo', s1] = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        got = c['/tmp/foo', s1]
        # Should return set value
        assert got == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    with Cache(str(tmpdir.join('db'))) as c:
        got = c['/tmp/foo', s1]
        # Should return cached value
        assert got == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        # Should not have value for new stat
        with pytest.raises(KeyError):
            c['/tmp/foo', s2]
        c['/tmp/foo', s2] = 'f3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        got = c['/tmp/foo', s2]
        # Should return new value
        assert got == 'f3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


def test_Cache_get_missing(Cache, tmpdir):
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
    with Cache(str(tmpdir.join('db'))) as c:
        with pytest.raises(KeyError):
            c['/tmp/foo', s]


class _stat_result:

    def __init__(self, **kwargs):
        self.__dict__ = kwargs
