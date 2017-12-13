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

import filecmp
from functools import partial
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


def add_all(hashdir: 'PathLike', paths: 'Iterable[PathLike]', merge=False):
    """Add files and directories to a hash archive."""
    for path in paths:
        if os.path.isdir(path):
            add_dir(hashdir, path, merge=merge)
        else:
            add_file(hashdir, path, merge=merge)


def add_dir(hashdir: 'PathLike', directory: 'PathLike', merge=False):
    """Add a directory's files to a hash archive."""
    for root, dirs, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            add_file(hashdir, path, merge=merge)


def add_file(hashdir: 'PathLike', path: 'PathLike', merge=False):
    """Add a file to a hash archive.

    If the file is already in the hash archive and is the same file,
    return without doing anything else.  If it is not the same file,
    behavior is determined by merge.  If merge is False, raise
    FileExistsError.  If merge is True, replace the file with a hard
    link to the file in the hash archive if the content is the same.
    """
    logger.info('Adding file %s', path)
    indexer = Indexer(
        index_dir=hashdir,
        hash_func=_sha256_hash,
        path_func=_path256,
        link_func=partial(_merge_link, merge=merge))
    indexer.add_file(path)


class Indexer:

    def __init__(self,
                 index_dir: 'PathLike',
                 hash_func: 'Callable[[Path], str]',
                 path_func: 'Callable[[Path, str], PurePath]',
                 link_func: 'Callable[[Path, Path], Any]'):
        self._index_dir = Path(index_dir)
        self._hash_func = hash_func
        self._path_func = path_func
        self._link_func = link_func

    def add_file(self, path: 'PathLike'):
        """Add a file to the index."""
        path = Path(path)
        digest: 'str' = self._hash_func(path)
        hashed_path: 'PurePath' = self._path_func(path, digest)
        self._link_func(path, self._index_dir / hashed_path)


def _sha256_hash(path: 'Path') -> 'str':
    """Return hex digest for file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        _feed(h, f)
    return h.hexdigest()


def _path256(path: 'Path', digest: 'str') -> 'PurePath':
    ext = ''.join(path.suffixes)
    return PurePath(digest[:2], f'{digest[2:]}{ext}')


def _merge_link(src: 'Path', dst: 'Path', merge=False):
    if not dst.exists():
        logger.info('Storing %s to %s', src, dst)
        dst.parent.mkdir(exist_ok=True)
        os.link(src, dst)
        return
    if dst.samefile(src):
        logger.info('%s already stored to %s', src, dst)
        return
    if not (merge and filecmp.cmp(src, dst, shallow=False)):
        raise FileExistsError(f'{dst} exists but different from {src}')
    dst.unlink()
    os.link(src, dst)


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
