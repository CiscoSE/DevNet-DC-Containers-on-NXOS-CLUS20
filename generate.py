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

# Import Python modules
import time

# Import modules from 3rd parties
import prometheus_client

# Import modules from this repo
from nxapi import arguments, connection
import vxlan


def generate(switch):
    """
    generate(switch) - call all the metric generation methods against
    the provided switch object
    """

    vxlan.generate(switch)


if __name__ == '__main__':

    # Hardcoded default (for now)
    sleep_interval = 5

    # Fetch connection information from arguments/environment
    host, port, username, password, verbose, ssl = arguments.process()

    # Fetch a connection object for our target switch
    if ssl:
        protocol = 'https'
    else:
        protocol = 'http'

    switch = connection.nxapi(
        host=host, port=port, protocol=protocol,
        username=username, password=password
    )

    # Start the Prometheus client library web service
    if not verbose:
        prometheus_client.start_http_server(8888)

    # As a metric generator, we loop/poll on these tasks forever
    while True:
        # Trigger generation and collection preparation
        generate(switch, verbose)

        # Sleep until the next interval
        time.sleep(sleep_interval)
