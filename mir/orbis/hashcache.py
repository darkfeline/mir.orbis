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

"""This module implements caching for file hashes."""

import os
from pathlib import Path
import sqlite3

from mir import xdg


class HashCache:

    """Cache for file SHA-256 hashes.

    Hashes are stored in a SQLite database along with the file's path,
    mtime, and size.  The file's mtime and size are checked
    automatically.

    HashCache implements a basic mapping API for access and a context
    manager API for closing the database connection.
    """

    def __init__(self, database: str = None):
        if database is None:
            db = _dbpath()
            db.parent.mkdir(parents=True, exist_ok=True)
            database = str(db)
        self._con = con = sqlite3.connect(database)
        con.row_factory = sqlite3.Row
        self._setup_table(con)

    @staticmethod
    def _setup_table(con):
        con.execute(f"""CREATE TABLE IF NOT EXISTS sha256_cache (
        path TEXT NOT NULL,
        mtime INT NOT NULL,
        size INT NOT NULL,
        hexdigest TEXT NOT NULL,
        CONSTRAINT path_u UNIQUE (path)
        )""")

    def __getitem__(self, key):
        path: str
        path, stat = key
        cur = self._con.execute(
            """SELECT hexdigest FROM sha256_cache
            WHERE path=? AND mtime=? AND size=?""",
            (path, stat.st_mtime, stat.st_size))
        row = cur.fetchone()
        if row is None:
            raise KeyError(path, stat)
        return row['hexdigest']

    def __setitem__(self, key, digest: str):
        path: str
        path, stat = key
        self._con.execute(
            """INSERT OR REPLACE INTO sha256_cache
            (path, mtime, size, hexdigest)
            VALUES (?, ?, ?, ?)""",
            (path, stat.st_mtime, stat.st_size, digest))
        self._con.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._con.close()
        return False


def _dbpath() -> Path:
    """Return the path to the user's hash cache database."""
    return _cachedir() / 'hash.db'


def _cachedir() -> Path:
    return xdg.CACHE_HOME / 'mir.orbis'
