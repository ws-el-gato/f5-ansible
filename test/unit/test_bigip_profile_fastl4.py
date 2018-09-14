# -*- coding: utf-8 -*-
#
# Copyright: (c) 2018, F5 Networks Inc.
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import pytest
import sys

from nose.plugins.skip import SkipTest
if sys.version_info < (2, 7):
    raise SkipTest("F5 Ansible modules require Python >= 2.7")

from ansible.compat.tests import unittest
from ansible.compat.tests.mock import Mock
from ansible.compat.tests.mock import patch
from ansible.module_utils.basic import AnsibleModule

try:
    from library.modules.bigip_profile_fastl4 import ApiParameters
    from library.modules.bigip_profile_fastl4 import ModuleParameters
    from library.modules.bigip_profile_fastl4 import ModuleManager
    from library.modules.bigip_profile_fastl4 import ArgumentSpec
    from library.module_utils.network.f5.common import F5ModuleError
    from library.module_utils.network.f5.common import iControlUnexpectedHTTPError
    from test.unit.modules.utils import set_module_args
except ImportError:
    try:
        from ansible.modules.network.f5.bigip_profile_fastl4 import ApiParameters
        from ansible.modules.network.f5.bigip_profile_fastl4 import ModuleParameters
        from ansible.modules.network.f5.bigip_profile_fastl4 import ModuleManager
        from ansible.modules.network.f5.bigip_profile_fastl4 import ArgumentSpec
        from ansible.module_utils.network.f5.common import F5ModuleError
        from ansible.module_utils.network.f5.common import iControlUnexpectedHTTPError
        from units.modules.utils import set_module_args
    except ImportError:
        raise SkipTest("F5 Ansible modules require the f5-sdk Python library")

fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


class TestParameters(unittest.TestCase):
    def test_module_parameters(self):
        args = dict(
            name='foo',
            parent='bar',
            idle_timeout=100,
            client_timeout=101,
            description='description one',
            explicit_flow_migration=False,
            ip_df_mode='pmtu',
            ip_tos_to_client=102,
            ip_tos_to_server=103,
            ip_ttl_v4=104,
            ip_ttl_v6=105,
            ip_ttl_mode='proxy',
            keep_alive_interval=106,
            late_binding=True,
            link_qos_to_client=7,
            link_qos_to_server=6,
            loose_close=False,
            loose_initialization=True,
            mss_override=4,
            reassemble_fragments=True,
            receive_window_size=109,
            reset_on_timeout=False,
            rtt_from_client=True,
            rtt_from_server=False,
            server_sack=True,
            server_timestamp=False,
            syn_cookie_mss=110,
            tcp_close_timeout=111,
            tcp_generate_isn=True,
            tcp_handshake_timeout=112,
            tcp_strip_sack=False,
            tcp_time_wait_timeout=113,
            tcp_timestamp_mode='rewrite',
            tcp_wscale_mode='strip',
            timeout_recovery='fallback',
        )

        p = ModuleParameters(params=args)
        assert p.name == 'foo'
        assert p.parent == '/Common/bar'
        assert p.description == 'description one'
        assert p.idle_timeout == 100
        assert p.client_timeout == 101
        assert p.explicit_flow_migration == 'no'
        assert p.ip_df_mode == 'pmtu'
        assert p.ip_tos_to_client == 102
        assert p.ip_tos_to_server == 103
        assert p.ip_ttl_v4 == 104
        assert p.ip_ttl_v6 == 105
        assert p.ip_ttl_mode == 'proxy'
        assert p.keep_alive_interval == 106
        assert p.late_binding == 'yes'
        assert p.link_qos_to_client == 7
        assert p.link_qos_to_server == 6
        assert p.loose_close == 'no'
        assert p.loose_initialization == 'yes'
        assert p.mss_override == 4
        assert p.reassemble_fragments == 'yes'
        assert p.receive_window_size == 109
        assert p.reset_on_timeout == 'no'
        assert p.rtt_from_client == 'yes'
        assert p.rtt_from_server == 'no'
        assert p.server_sack == 'yes'
        assert p.server_timestamp == 'no'
        assert p.syn_cookie_mss == 110
        assert p.tcp_close_timeout == 111
        assert p.tcp_generate_isn == 'yes'
        assert p.tcp_handshake_timeout == 112
        assert p.tcp_strip_sack == 'no'
        assert p.tcp_time_wait_timeout == 113
        assert p.tcp_timestamp_mode == 'rewrite'
        assert p.tcp_wscale_mode == 'strip'
        assert p.timeout_recovery == 'fallback'

    def test_api_parameters(self):
        args = load_fixture('load_ltm_fastl4_profile_1.json')
        p = ApiParameters(params=args)
        assert p.name == 'fastL4'
        assert p.description is None


class TestManager(unittest.TestCase):

    def setUp(self):
        self.spec = ArgumentSpec()

    def test_create(self, *args):
        # Configure the arguments that would be sent to the Ansible module
        set_module_args(dict(
            name='foo',
            parent='bar',
            password='password',
            server='localhost',
            user='admin'
        ))

        module = AnsibleModule(
            argument_spec=self.spec.argument_spec,
            supports_check_mode=self.spec.supports_check_mode
        )
        mm = ModuleManager(module=module)

        # Override methods to force specific logic in the module to happen
        mm.exists = Mock(return_value=False)
        mm.create_on_device = Mock(return_value=True)

        results = mm.exec_module()

        assert results['changed'] is True
