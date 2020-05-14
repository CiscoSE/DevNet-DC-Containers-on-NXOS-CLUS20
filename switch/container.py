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

    command = 'run bash sudo docker run -d --restart always '
    command += '--name vxlan -p {0}:8888:8888 '.format(host)
    command += '-e NXAPI_HOST={0} -e NXAPI_PORT={1} '.format(host, port)
    command += '-e NXAPI_USER={0} -e NXAPI_PASS={1} '.format(username, password)
    command += 'gvevsetim/devnet-dc-clus20'

    if verbose:
        print(command)

    payload = switch.payload(command)

    if verbose:
        print(json.dumps(payload.post_input(), indent=4))

    response = switch.post(payload)

    # Print output from successful commands
    if 'result' in response:
        if response['result'] is not None:
            if 'msg' in response['result']:
                print('Success: ' + response['result']['msg'])
                
    # Print error output
    elif 'error' in response:
        if response['error'] is not None:
            if 'message' in response['error']:
                print('Error: ' + response['error']['message'])
            if 'data' in response['error']:
                if 'msg' in response['error']['data']:
                    print('Message: ' + response['error']['data']['msg'])

    # Print generic output in failure
    else:
        print(response)
