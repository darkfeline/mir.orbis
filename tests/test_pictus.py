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
from pathlib import Path
from unittest import mock

import pytest

from mir.orbis import hashcache
from mir.orbis import pictus


def test_find_hashdir(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    start = tmpdir.ensure('foo/bar/baz', dir=True)

    got = pictus.find_hashdir(start)
    assert got == Path(hashdir)


def test_find_hashdir_with_file_start(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    start = tmpdir.ensure('foo/bar/baz')

    got = pictus.find_hashdir(start)
    assert got == Path(hashdir)


def test_find_hashdir_missing(tmpdir):
    start = tmpdir.ensure('foo/bar', dir=True)
    with pytest.raises(pictus.NoHashDirError):
        pictus.find_hashdir(start)


def test_apply_to_dir(tmpdir):
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    f = _TestFunc()
    pictus.apply_to_dir(f, str(tmpdir))
    assert f.args == [str(path)]


def test_apply_to_all_dir(tmpdir):
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    f = _TestFunc()
    pictus.apply_to_all(f, [str(tmpdir)])
    assert f.args == [str(path)]


def test_apply_to_all_file(tmpdir):
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    f = _TestFunc()
    pictus.apply_to_all(f, [str(path)])
    assert f.args == [str(path)]


def test_SimpleIndexer(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp.jpg')
    path.write('Philosophastra Illustrans')

    indexer = pictus.SimpleIndexer(hashdir)
    indexer(path)

    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53.jpg')
    assert os.path.samefile(path, hashed_path)


def test_SimpleIndexer_when_already_indexed(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')
    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')
    hashed_path.join('..').ensure_dir()
    os.link(str(path), str(hashed_path))

    indexer = pictus.SimpleIndexer(hashdir)
    indexer(path)

    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')
    assert os.path.samefile(path, hashed_path)


def test_SimpleIndexer_with_merge(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')
    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')
    hashed_path.write('Philosophastra Illustrans', ensure=True)

    assert not os.path.samefile(str(path), str(hashed_path))
    indexer = pictus.SimpleIndexer(hashdir)
    indexer(path)
    assert os.path.samefile(str(path), str(hashed_path))


def test_SimpleIndexer_with_collision(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')
    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')
    hashed_path.write('Pretend hash collision', ensure=True)

    indexer = pictus.SimpleIndexer(hashdir)
    with pytest.raises(pictus.FileExistsError):
        indexer(path)


@mock.patch.dict(os.environ)
def test_CachingIndexer(tmpdir):
    os.environ['XDG_CACHE_HOME'] = str(tmpdir)
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp.jpg')
    path.write('Philosophastra Illustrans')

    with hashcache.connect() as con:
        indexer = pictus.CachingIndexer(hashdir, con)
        indexer(path)
        indexer(path)

    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53.jpg')
    assert os.path.samefile(path, hashed_path)


class _TestFunc:

    def __init__(self):
        self.args = []

    def __call__(self, arg):
        self.args.append(arg)
