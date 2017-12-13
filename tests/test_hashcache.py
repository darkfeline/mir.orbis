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

import os

from unittest import mock

from mir.orbis import hashcache


def test_find_hashdir_default():
    with mock.patch.dict(os.environ):
        os.environ['HOME'] = '/home/yamada'
        os.environ.pop('XDG_CONFIG_HOME', None)
        got = hashcache._xdg_config_home()
    assert str(got) == '/home/yamada/.config'


def test_find_hashdir_explicit():
    with mock.patch.dict(os.environ):
        os.environ['HOME'] = '/home/yamada'
        os.environ['XDG_CONFIG_HOME'] = '/tmp/config'
        got = hashcache._xdg_config_home()
    assert str(got) == '/tmp/config'
