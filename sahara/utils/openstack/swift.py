# Copyright (c) 2014 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import swiftclient

from sahara.swift import swift_helper as sh
from sahara.swift import utils as su
from sahara.utils.openstack import keystone as k


def client(username, password, trust_id=None):
    '''return a Swift client

    This will return a Swift client for the specified username scoped to the
    current context project, unless a trust identifier is specified.

    If a trust identifier is present then the Swift client will be created
    based on a preauthorized token generated by the username scoped to the
    trust identifier.

    :param username: The username for the Swift client
    :param password: The password associated with the username
    :param trust_id: A trust identifier for scoping the username (optional)
    :returns: A Swift client object

    '''
    client_kwargs = dict(auth_version='2.0')
    if trust_id:
        proxyclient = k.client_for_proxy_user(username, password, trust_id)
        client_kwargs.update(preauthurl=su.retrieve_preauth_url(),
                             preauthtoken=proxyclient.auth_token)
    else:
        client_kwargs.update(authurl=su.retrieve_auth_url(),
                             user=username,
                             key=password,
                             tenant_name=sh.retrieve_tenant())

    return swiftclient.Connection(**client_kwargs)
