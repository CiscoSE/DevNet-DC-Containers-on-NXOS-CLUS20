#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python Template for Cisco Sample Code.

Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""


__author__ = "Timothy E Miller, PhD <timmil@cisco.com>"
__contributors__ = [
]
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Import Python Modules
import json

# Import Local Modules
from nxapi import arguments
from nxapi import connection

commands = [

    # Prep for scripted configuration
    'terminal dont-ask',

    # Protect against switch reload
    'configure terminal',

    # Out with the old
    'guestshell destroy',

    # Ensure bash shell is enabled
    'feature bash-shell',

    # Setup DNS correctly
    'vrf context management',
    'ip domain-name clus20.internal',
    'ip name-server 208.67.222.222',

    # Initialize the Docker environment
    'run bash sudo service docker start',
    'run bash sudo chkconfig --add docker',
    'run bash sudo service docker stop',

    # Give your Docker space
    'run bash sudo truncate -s +1000MB /bootflash/dockerpart',
    'run bash sudo e2fsck -f /bootflash/dockerpart',
    'run bash sudo /sbin/resize2fs /bootflash/dockerpart',
    'run bash sudo e2fsck -f /bootflash/dockerpart',

    # Secure your Docker (setup)
    'run bash sudo groupadd dockremap -r',
    'run bash sudo useradd dockremap -r -g dockremap',
    'run bash sudo bash -c \'echo "dockremap:123000:65536" >> /etc/subuid\'',
    'run bash sudo bash -c \'echo "dockremap:123000:65536" >> /etc/subgid\'',

    # Secure your control plane (restrict docker to /ext_ser/)
    'run bash sudo sed -i -e \'s,^other_args=.*,other_args="--debug=true --cgroup-parent=/ext_ser/ --userns-remap=default",g\' /etc/sysconfig/docker',  # noqa: E501

    # Make /var/lib/docker shareable (for Kubernetes)
    'run bash sudo sed -i -e \'s,mount -t ext4 $loopd,mount -t ext4 --make-shared $loopd,g\' /etc/init.d/docker',  # noqa: E501

    # Bring Docker back up for production
    'run bash sudo service docker start',

    # Save the configuration
    'copy running-config startup-config',
]

proxy_commands = [
    'run bash sudo sed -E \'s,^#(export http.*),\1,g\' /etc/sysconfig/docker',  # noqa: E501
    'run bash sudo service docker restart',
    'copy running-config startup-config',
]

if __name__ == '__main__':
    # Fetch connection information from arguments/environment
    host, port, username, password, verbose, ssl, proxy = arguments.process()

    # Fetch a connection object for our target switch
    if ssl:
        protocol = 'https'
    else:
        protocol = 'http'

    switch = connection.nxapi(
        host=host, port=port, protocol=protocol,
        username=username, password=password
    )

    if proxy:
        commands = commands + proxy_commands

    payload = switch.payload()

    for cmd in commands:
        if verbose:
            print(cmd)
        payload.add_command(cmd)

    if verbose:
        print(json.dumps(payload.post_input(), indent=4))

    response = switch.post(payload)

    if not isinstance(response, list):
        print(str(response))
    else:
        for r in response:
            # Print output from successful commands
            if 'result' in r:
                if r['result'] is not None:
                    if 'msg' in r['result']:
                        print(r['result']['msg'])
            # Print error output
            elif 'error' in r:
                if r['error'] is not None:
                    if 'message' in r['error']:
                        print(r['error']['message'])
                    if 'data' in r['error']:
                        if 'msg' in r['error']['data']:
                            print(r['error']['data']['msg'])
            # Print generic output in failure
            else:
                print(r)
