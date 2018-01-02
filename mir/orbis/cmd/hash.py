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

"""Add a file to a directory organized by content hash."""

import argparse
import functools
import logging
import os
from pathlib import Path
import sys

from mir.orbis import hashcache
from mir.orbis import pictus

_HASHDIR = 'hash'

logger = logging.getLogger(__name__)


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs="+", type=Path, metavar='FILES_OR_DIRS')
    args = parser.parse_args(args)

    logging.basicConfig(level='DEBUG')

    hashdir = _find_hashdir(args.files[0])
    logger.info('Found hash dir %s', hashdir)
    with hashcache.HashCache() as cache:
        indexer = pictus.CachingIndexer(hashdir, cache)
        _apply_to_all(_add_logging(indexer), args.files)
    return 0


def _add_logging(func):
    @functools.wraps(func)
    def indexer(path):
        logger.info('Adding %s', path)
        return func(path)
    return indexer


def _find_hashdir(start: 'PathLike') -> Path:
    """Find hash directory."""
    path = Path(start).resolve()
    if path.is_file():
        path = path.parent
    while True:
        if _HASHDIR in os.listdir(path):
            return path / _HASHDIR
        if path.parent == path:
            raise Exception('rootdir not found')
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


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
