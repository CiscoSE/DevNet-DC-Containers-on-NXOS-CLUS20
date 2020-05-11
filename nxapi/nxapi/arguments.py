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
import os
import argparse


def process(user='admin', password='admin', host='localhost', port='23456'):
    """
    process_arguments: for this application, process the command line arguments
    and/or environment variables and simply return 6 values:
        - host
        - port
        - user
        - password
        - verbose
        - ssl

    The values passed into the method would be the default values if the
    CLI/ENV did not provide them.  Verbosity always defaults to off.
    SSL encrypted transport always defaults to off.
    """

    # Command line arguments to flag Docker environment
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--container',
                        help='Flag container operation',
                        action='store_true',
                        )

    parser.add_argument('-t', '--target',
                        help='Provide remote hostname/IP for NXAPI',
                        )

    parser.add_argument('-p', '--port',
                        help='Provide remote port for NXAPI',
                        )

    parser.add_argument('-u', '--user',
                        help='Provide remote username for NXAPI',
                        )

    parser.add_argument('-w', '--password',
                        help='Provide remote password for NXAPI',
                        )

    parser.add_argument('-v', '--verbose',
                        help='Enable verbose output',
                        action='store_true'
                        )

    parser.add_argument('-s', '--ssl',
                        help='Connect via SSL for NXAPI',
                        action='store_true'
                        )

    args = parser.parse_args()

    # Enable output - can be overriden by Docker flag
    if args.verbose:
        verbose = True
    else:
        verbose = False

    # Enable SSL transport - can be overriden by Docker flag
    if args.ssl:
        ssl = True
    else:
        ssl = False

    # Credentials
    if args.user:
        user = args.user

    if args.password:
        password = args.password

    # Running against a remote NX-OS system (not local VM)
    if args.target:
        host = args.target

    # Change from the (project historical) default port
    if args.port:
        port = str(args.port)

    # Running in a Docker container
    if args.container:
        host = os.getenv('NXAPI_HOST', 'host.docker.internal')
        port = os.getenv('NXAPI_PORT', port)
        user = os.getenv('NXAPI_USER', 'admin')
        password = os.getenv('NXAPI_PASS', 'admin')
        ssl = False
        verbose = False

    return host, port, user, password, verbose, ssl
