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

import io
import os
from pathlib import Path
from pathlib import PurePath

import pytest

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
    with pytest.raises(pictus.Error):
        pictus.find_hashdir(start)


def test_add_all_on_dir(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    pictus.add_all(hashdir, [tmpdir])

    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')
    assert os.path.samefile(path, hashed_path)


def test_add_all_on_file(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    pictus.add_all(hashdir, [path])

    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')
    assert os.path.samefile(path, hashed_path)


def test_add_dir(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    pictus.add_dir(hashdir, str(tmpdir))

    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')
    assert os.path.samefile(path, hashed_path)


def test_add_file(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')

    pictus.add_file(hashdir, path)

    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')
    assert os.path.samefile(path, hashed_path)


def test_add_file_with_extension(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp.jpg')
    path.write('Philosophastra Illustrans')

    pictus.add_file(hashdir, path)

    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53.jpg')
    assert os.path.samefile(path, hashed_path)


def test_add_file_with_collision(tmpdir):
    hashdir = tmpdir.mkdir('hash')
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')
    hashed_path = hashdir.join('8b', 'c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')
    hashed_path.write('Philosophastra Illustrans', ensure=True)

    with pytest.raises(pictus.FileExistsError):
        pictus.add_file(hashdir, path)


def test__hashed_path(tmpdir):
    path = tmpdir.join('tmp')
    path.write('Philosophastra Illustrans')
    got = pictus._hashed_path(path)
    assert got == PurePath('8b/c36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53')


def test__hexdigest():
    f = io.BytesIO('Philosophastra Illustrans'.encode())
    got = pictus._hexdigest(f)
    assert got == '8bc36727b5aa2a78e730bfd393836b246c4d565e4dc3e4f413df26e26656bb53'
