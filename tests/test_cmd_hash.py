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

from pathlib import Path

import pytest

from mir.orbis.cmd import hash


def test_find_hashdir(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    start = tmpdir.ensure('foo/bar/baz', dir=True)

    got = hash._find_hashdir(start)
    assert got == Path(hashdir)


def test_find_hashdir_with_file_start(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    start = tmpdir.ensure('foo/bar/baz')

    got = hash._find_hashdir(start)
    assert got == Path(hashdir)


def test_find_hashdir_missing(tmpdir):
    start = tmpdir.ensure('foo/bar', dir=True)
    with pytest.raises(Exception):
        hash._find_hashdir(start)


def test_apply_to_dir(tmpdir):
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    f = _TestFunc()
    hash._apply_to_dir(f, str(tmpdir))
    assert f.args == [str(path)]


def test_apply_to_all_dir(tmpdir):
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    f = _TestFunc()
    hash._apply_to_all(f, [str(tmpdir)])
    assert f.args == [str(path)]


def test_apply_to_all_file(tmpdir):
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    f = _TestFunc()
    hash._apply_to_all(f, [str(path)])
    assert f.args == [str(path)]


def test_add_logging(caplog):
    f = hash._add_logging(_TestFunc())
    f('foo')
    got = caplog.records
    assert len(got) == 1
    assert got[0].message == 'Adding foo'


class _TestFunc:

    def __init__(self):
        self.args = []

    def __call__(self, arg):
        self.args.append(arg)
