mir.orbis README
================

.. image:: https://circleci.com/gh/darkfeline/mir.orbis.svg?style=shield
   :target: https://circleci.com/gh/darkfeline/mir.orbis
   :alt: CircleCI
.. image:: https://codecov.io/gh/darkfeline/mir.orbis/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/darkfeline/mir.orbis
   :alt: Codecov
.. image:: https://badge.fury.io/py/mir.orbis.svg
   :target: https://badge.fury.io/py/mir.orbis
   :alt: PyPI Release
.. image:: https://readthedocs.org/projects/mir-orbis/badge/?version=latest
   :target: http://mir-orbis.readthedocs.io/en/latest/
   :alt: Latest Documentation

Hashed file archive.

This facilitates the construction of hard linking files to a hash store.

Example::

    $ cd tmp
    $ touch some-pic.jpg
    $ mkdir hash
    $ python3.6 -m mir.orbis.cmd.hash .
    # Now some-pic.jpg will be linked to
    # hash/ff/ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff.jpg

The name is a reference to Orbis Pictus.
