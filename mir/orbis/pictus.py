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

"""Working with hashed archives."""

import hashlib
import logging
import os
from pathlib import Path
from pathlib import PurePath

_BUFSIZE = 2 ** 20
_HASHDIR = 'hash'

logger = logging.getLogger(__name__)


def find_hashdir(start: 'PathLike') -> Path:
    """Find hash archive directory."""
    path = Path(start).resolve()
    if path.is_file():
        path = path.parent
    while True:
        if _HASHDIR in os.listdir(path):
            return path / _HASHDIR
        if path.parent == path:
            raise Error('rootdir not found')
        path = path.parent


def add_all(hashdir: 'PathLike', paths: 'Iterable[PathLike]'):
    """Add files and directories to a hash archive."""
    for path in paths:
        if os.path.isdir(path):
            add_dir(hashdir, path)
        else:
            add_file(hashdir, path)


def add_dir(hashdir: 'PathLike', directory: 'PathLike'):
    """Add a directory's files to a hash archive."""
    for root, dirs, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            add_file(hashdir, path)


def add_file(hashdir: 'PathLike', path: 'PathLike'):
    """Add a file to a hash archive.

    If the file is already in the hash archive and is the same file,
    return without doing anything else.  If it is not the same file,
    raise FileExistsError.
    """
    newpath = Path(hashdir) / _hashed_path(path)
    if newpath.exists():
        if newpath.samefile(os.fspath(path)):
            return
        else:
            raise FileExistsError(f'{newpath} exists but different from {path}')
    newpath.parent.mkdir(exist_ok=True)
    os.link(path, newpath)


def _hashed_path(path: 'PathLike') -> PurePath:
    """Return hashed path for a file."""
    with open(path, 'rb') as f:
        digest = _hexdigest(f)
    ext = os.path.splitext(path)[1]
    return PurePath(digest[:2]) / f'{digest[2:]}{ext}'


def _hexdigest(file):
    """Return hex digest for file."""
    h = hashlib.sha256()
    _feed(h, file)
    return h.hexdigest()


def _feed(hasher, file):
    """Feed bytes in a file to a hasher."""
    while True:
        b = file.read(_BUFSIZE)
        if not b:
            break
        hasher.update(b)


class Error(Exception):
    pass


class FileExistsError(Exception):
    pass
