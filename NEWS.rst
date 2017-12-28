mir.orbis Release Notes
=======================

This project uses `semantic versioning <http://semver.org/>`_.

0.5.0 (2017-12-27)
------------------

Added
-----

- `-p` option to load cache into memory for speed.

Changed
-------

- Hash cache no longer tracks device and inode.

Fixed
-----

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
