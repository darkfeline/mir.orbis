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

import pytest

from mir.orbis import commands


def test_bucket_without_args(tmpdir):
    tmpdir.mkdir('atelier')
    tmpdir.ensure('atelier sophie')
    with tmpdir.as_cwd():
        commands.bucket()
    assert not tmpdir.join('atelier sophie').exists()
    assert tmpdir.join('atelier/atelier sophie').exists()


def test_bucket_with_args(tmpdir):
    tmpdir.mkdir('atelier')
    tmpdir.ensure('atelier sophie')
    with tmpdir.as_cwd():
        commands.bucket(str(tmpdir), 'atelier sophie')
    assert not tmpdir.join('atelier sophie').exists()
    assert tmpdir.join('atelier/atelier sophie').exists()


def test_bucket_without_matching_dir(tmpdir):
    tmpdir.mkdir('surge')
    tmpdir.ensure('atelier sophie')
    with tmpdir.as_cwd():
        commands.bucket()
    assert tmpdir.join('atelier sophie').exists()
    assert not tmpdir.join('atelier/atelier sophie').exists()


def test_index_without_files(tmpdir):
    with tmpdir.as_cwd():
        commands.index()


def test_index_without_index_dir(tmpdir):
    tmpdir.join('foo').write('foo')
    with tmpdir.as_cwd():
        with pytest.raises(Exception):
            commands.index('foo')


def test_index_file(tmpdir):
    tmpdir.join('foo.txt').write('foo')
    tmpdir.mkdir('index')
    with tmpdir.as_cwd():
        commands.index('foo.txt')
        assert os.path.samefile(
            'index/2c/26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae.txt',
            'foo.txt')


def test_index_dir(tmpdir):
    tmpdir.mkdir('spam').join('foo.txt').write('foo')
    tmpdir.mkdir('index')
    with tmpdir.as_cwd():
        commands.index('spam')
        assert os.path.samefile(
            'index/2c/26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae.txt',
            'spam/foo.txt')
