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

import re
from setuptools import setup


def find_version(path):
    with open(path) as f:
        text = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              text, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='mir.orbis',
    version=find_version('mir/orbis/__init__.py'),
    description='Hashed file archives',
    long_description='',
    keywords='',
    url='https://github.com/darkfeline/mir.orbis',
    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],

    packages=['mir.orbis'],
    install_requires=[
        'mir.xdg~=1.0',
    ],
)
