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

"""File indexing."""

import filecmp
from functools import partial
import hashlib
import logging
import os
from pathlib import Path
from pathlib import PurePath

_BUFSIZE = 2 ** 20

logger = logging.getLogger(__name__)


def CachingIndexer(index_dir: 'PathLike', con):
    """Returns a one argument callable that indexes files to index_dir."""
    return partial(
        _index_file,
        index_dir,
        partial(_caching_sha256_hash, con),
        _path256,
        _merge_link)


def SimpleIndexer(index_dir: 'PathLike'):
    """Returns a one argument callable that indexes files to index_dir."""
    return partial(
        _index_file,
        index_dir,
        _sha256_hash,
        _path256,
        _merge_link)


def _index_file(index_dir: 'PathLike',
                hash_func: 'Callable[[Path], str]',
                path_func: 'Callable[[Path, str], PurePath]',
                link_func: 'Callable[[Path, Path], Any]',
                path: 'PathLike'):
    """Add a file to an index.

    This is a very generic function for hashing a file and putting it
    into an index directory.

    hash_func is called with the file's path and should return the
    file's hash.

    path_func is called with the file's path and the hash returned from
    hash_func.  path_func should return the path the file should be
    linked to relative to index_dir.

    link_func is called with the file's path and the path to link the
    file to under index_dir.
    """
    index_dir = Path(index_dir)
    path = Path(path)
    digest: 'str' = hash_func(path)
    hashed_path: 'PurePath' = path_func(path, digest)
    link_func(path, index_dir / hashed_path)


def _caching_sha256_hash(cache, path: Path) -> str:
    """Return hex digest for file using a cache.

    cache should support __getitem__ and __setitem__.
    """
    try:
        return cache[str(path), path.stat()]
    except KeyError:
        digest = _sha256_hash(path)
        cache[str(path), path.stat()] = digest
        return digest


def _sha256_hash(path: Path) -> str:
    """Return hex digest for file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        _feed(h, f)
    return h.hexdigest()


def _path256(path: Path, digest: str) -> PurePath:
    """Construct a hashed path with 256 subdirs for a hex hash."""
    ext = ''.join(path.suffixes)
    return PurePath(digest[:2], f'{digest[2:]}{ext}')


def _merge_link(src: Path, dst: Path):
    """Merge link.

    Try to link src to dst.  If dst exists and is the same file as src,
    do nothing.  If dst exists, is a different file, and has the same
    contents, replace dst with a link to src.  If dst exists and has
    different contents, raise CollisionError.
    """
    if not dst.exists():
        logger.info('Storing %s to %s', src, dst)
        dst.parent.mkdir(exist_ok=True)
        os.link(src, dst)
        return
    if dst.samefile(src):
        logger.info('%s already stored to %s', src, dst)
        return
    if not filecmp.cmp(src, dst, shallow=False):
        raise CollisionError(src, dst)
    src.unlink()
    os.link(dst, src)


def _feed(hasher, file):
    """Feed bytes in a file to a hasher."""
    while True:
        b = file.read(_BUFSIZE)
        if not b:
            break
        hasher.update(b)


class CollisionError(Exception):
    pass