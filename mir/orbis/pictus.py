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

logger = logging.getLogger(__name__)


def CachingIndexer(hash_dir: 'PathLike', con):
    return partial(
        _index_file,
        hash_dir,
        partial(_caching_sha256_hash, con),
        _path256,
        _merge_link)


def SimpleIndexer(hash_dir: 'PathLike'):
    return partial(
        _index_file,
        hash_dir,
        _sha256_hash,
        _path256,
        _merge_link)


def _index_file(hash_dir: 'PathLike',
                hash_func: 'Callable[[Path], str]',
                path_func: 'Callable[[Path, str], PurePath]',
                link_func: 'Callable[[Path, Path], Any]',
                path: 'PathLike'):
    hash_dir = Path(hash_dir)
    path = Path(path)
    digest: 'str' = hash_func(path)
    hashed_path: 'PurePath' = path_func(path, digest)
    link_func(path, hash_dir / hashed_path)


def _caching_sha256_hash(cache, path: Path) -> str:
    """Return hex digest for file using a cache."""
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
    """Merge linker."""
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
