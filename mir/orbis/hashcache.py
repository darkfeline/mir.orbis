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

"""Hash cache."""

import os
from pathlib import Path
import sqlite3


def connect():
    """Connect to the user's hash cache database."""
    db = _dbpath()
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    _setup_table(con)
    return con


def get_sha256(con, path: str, stat):
    """Get cached SHA256 hash.

    If the corresponding hash is not in the cache, raise NoHashError.
    """
    cur = con.execute(
        """SELECT hexdigest FROM sha256_cache
        WHERE path=? AND device=? AND inode=? AND mtime=? AND size=?""",
        (path, stat.st_dev, stat.st_ino, stat.st_mtime, stat.st_size))
    row = cur.fetchone()
    if row is None:
        raise NoHashError(path, stat)
    return row['hexdigest']


def add_sha256(con, path: str, stat, digest: str):
    """Add SHA256 hash to the cache."""
    con.execute(
        """INSERT OR REPLACE INTO sha256_cache
        (path, device, inode, mtime, size, hexdigest)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (path, stat.st_dev, stat.st_ino, stat.st_mtime, stat.st_size, digest))


def _setup_table(con):
    con.execute(f"""CREATE TABLE IF NOT EXISTS sha256_cache (
    path TEXT NOT NULL,
    device INT NOT NULL,
    inode INT NOT NULL,
    mtime INT NOT NULL,
    size INT NOT NULL,
    hexdigest TEXT NOT NULL,
    CONSTRAINT path_u UNIQUE (path),
    CONSTRAINT device_inode_u UNIQUE (device, inode)
    )""")


def _dbpath() -> Path:
    """Return the path to the user's hash cache database."""
    return _cachedir() / 'hash.db'


def _cachedir() -> Path:
    return _xdg_cache_home() / 'mir.orbis'


def _xdg_cache_home() -> Path:
    return Path(os.getenv('XDG_CACHE_HOME',
                          Path(os.environ['HOME'], '.cache')))


class NoHashError(ValueError):
    pass
