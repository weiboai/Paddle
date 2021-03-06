# Copyright (c) 2016 PaddlePaddle Authors. All Rights Reserved
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

import paddle.trainer_config_helpers.networks as conf_nw
import inspect
from config_base import __convert_to_v2__

__all__ = []


def __initialize__():
    for each_subnetwork in conf_nw.__all__:
        if each_subnetwork in ['inputs', 'outputs']:
            continue
        func = getattr(conf_nw, each_subnetwork)
        if hasattr(func, 'argspec'):
            argspec = func.argspec
        else:
            argspec = inspect.getargspec(func)
        if each_subnetwork == 'simple_attention':
            parents = ['encoded_sequence', 'encoded_proj', 'decoder_state']
        else:
            parents = filter(lambda x: x.startswith('input'), argspec.args)
        assert len(parents) != 0, each_subnetwork
        v2_subnet = __convert_to_v2__(
            each_subnetwork,
            parent_names=parents,
            is_default_name='name' in argspec.args)
        globals()[each_subnetwork] = v2_subnet
        global __all__
        __all__.append(each_subnetwork)


__initialize__()
