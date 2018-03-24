# Copyright (C) 2018 Allen Li
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

import functools
import logging
import os
from pathlib import Path

from mir.orbis import hashcache
from mir.orbis import indexing

_INDEX_DIR = 'index'

logger = logging.getLogger(__name__)


def index(*files):
    logging.basicConfig(level='DEBUG')
    files = [Path(f) for f in files]
    hashdir = _find_index_dir(files[0])
    logger.info('Found index dir %s', hashdir)
    with hashcache.HashCache() as cache:
        indexer = indexing.CachingIndexer(hashdir, cache)
        _apply_to_all(_add_logging(indexer), files)


def _add_logging(func):
    @functools.wraps(func)
    def indexer(path):
        logger.info('Adding %s', path)
        return func(path)
    return indexer


def _find_index_dir(start: 'PathLike') -> Path:
    path = Path(start).resolve()
    if path.is_file():
        path = path.parent
    while True:
        if _INDEX_DIR in os.listdir(path):
            return path / _INDEX_DIR
        if path.parent == path:
            raise Exception('index dir not found')
        path = path.parent


def _apply_to_all(func, paths: 'Iterable[PathLike]'):
    """Call a function on files and directories."""
    for path in paths:
        path = os.fspath(path)
        if os.path.isdir(path):
            _apply_to_dir(func, path)
        else:
            func(path)


def _apply_to_dir(func, directory: 'PathLike'):
    """Call a function on a directory's files."""
    for root, dirs, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            func(path)
