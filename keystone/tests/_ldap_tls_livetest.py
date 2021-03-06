# Copyright 2013 OpenStack Foundation
# Copyright 2013 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ldap
import ldap.modlist

from keystone import config
from keystone import exception
from keystone import identity
from keystone import tests
from keystone.tests import _ldap_livetest


CONF = config.CONF


def create_object(dn, attrs):
    conn = ldap.initialize(CONF.ldap.url)
    conn.simple_bind_s(CONF.ldap.user, CONF.ldap.password)
    ldif = ldap.modlist.addModlist(attrs)
    conn.add_s(dn, ldif)
    conn.unbind_s()


class LiveTLSLDAPIdentity(_ldap_livetest.LiveLDAPIdentity):

    def _set_config(self):
        self.config([tests.dirs.etc('keystone.conf.sample'),
                     tests.dirs.tests('test_overrides.conf'),
                     tests.dirs.tests('backend_tls_liveldap.conf')])

    def test_tls_certfile_demand_option(self):
        self.opt_in_group('ldap',
                          use_tls=True,
                          tls_cacertdir=None,
                          tls_req_cert='demand')
        self.identity_api = identity.backends.ldap.Identity()

        user = {'id': 'fake1',
                'name': 'fake1',
                'password': 'fakepass1',
                'tenants': ['bar']}
        self.identity_api.create_user('fake1', user)
        user_ref = self.identity_api.get_user('fake1')
        self.assertEqual(user_ref['id'], 'fake1')

        user['password'] = 'fakepass2'
        self.identity_api.update_user('fake1', user)

        self.identity_api.delete_user('fake1')
        self.assertRaises(exception.UserNotFound, self.identity_api.get_user,
                          'fake1')

    def test_tls_certdir_demand_option(self):
        self.opt_in_group('ldap',
                          use_tls=True,
                          tls_cacertdir=None,
                          tls_req_cert='demand')
        self.identity_api = identity.backends.ldap.Identity()

        user = {'id': 'fake1',
                'name': 'fake1',
                'password': 'fakepass1',
                'tenants': ['bar']}
        self.identity_api.create_user('fake1', user)
        user_ref = self.identity_api.get_user('fake1')
        self.assertEqual(user_ref['id'], 'fake1')

        user['password'] = 'fakepass2'
        self.identity_api.update_user('fake1', user)

        self.identity_api.delete_user('fake1')
        self.assertRaises(exception.UserNotFound, self.identity_api.get_user,
                          'fake1')

    def test_tls_bad_certfile(self):
        self.opt_in_group(
            'ldap',
            use_tls=True,
            tls_req_cert='demand',
            tls_cacertfile='/etc/keystone/ssl/certs/mythicalcert.pem',
            tls_cacertdir=None)
        self.identity_api = identity.backends.ldap.Identity()

        user = {'id': 'fake1',
                'name': 'fake1',
                'password': 'fakepass1',
                'tenants': ['bar']}
        self.assertRaises(IOError, self.identity_api.create_user, 'fake', user)

    def test_tls_bad_certdir(self):
        self.opt_in_group(
            'ldap',
            use_tls=True,
            tls_cacertfile=None,
            tls_req_cert='demand',
            tls_cacertdir='/etc/keystone/ssl/mythicalcertdir')
        self.identity_api = identity.backends.ldap.Identity()

        user = {'id': 'fake1',
                'name': 'fake1',
                'password': 'fakepass1',
                'tenants': ['bar']}
        self.assertRaises(IOError, self.identity_api.create_user, 'fake', user)
