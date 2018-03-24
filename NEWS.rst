mir.orbis Release Notes
=======================

This project uses `semantic versioning <http://semver.org/>`_.

0.7.0 (2018-03-24)
------------------

Changed
^^^^^^^

- mir.orbis now uses Fire for commands.
  - `python -m mir.orbis.cmd.hash` is now `python -m mir.orbis hash`.
- `hash` command is now `index`.
- `pictus` module renamed to `indexing`.
- The index/hash dir is renamed from `hash` to `index`.

0.6.0 (2018-01-01)
------------------

Removed
^^^^^^^

- `-p` option (did not improve performance).

0.5.0 (2017-12-27)
------------------

Added
^^^^^

- `-p` option to load cache into memory for speed.

Changed
^^^^^^^

- Hash cache no longer tracks device and inode.

Fixed
^^^^^

- Fixed not committing hash cache.

0.4.0 (2017-12-17)
------------------

Changed
^^^^^^^

- `hash` command now caches file hashes.  This should make it run
  faster on previously seen files.

0.3.0 (2017-11-12)
------------------

Changed
^^^^^^^

- `hash` command now merges files with same content.

0.2.0 (2017-10-04)
------------------

Fixed
^^^^^

- Fixed typo causing `hash` to not work.

0.1.0 (2017-09-17)
------------------

Initial release.
