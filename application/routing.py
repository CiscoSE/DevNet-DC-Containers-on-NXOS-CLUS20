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
import isodate

# Import modules from 3rd parties
import prometheus_client

# Import modules from this repo

# Create metrics objects
ip_prefix_path_count = prometheus_client.Gauge(
                        'ip_prefix_path_count',
                        'Track number of ECMP entries for given prefix',
                        ('vrf', 'prefix')
                        )

ip_prefix_path_uptime = prometheus_client.Gauge(
                        'ip_prefix_path_uptime',
                        'Track uptime in seconds for nexthop of given prefix',
                        ('vrf', 'prefix', 'nexthop')
                        )

ip_prefix_path_traffic = prometheus_client.Gauge(
                        'ip_prefix_path_traffic',
                        'Report on traffic sent over each path',
                        ('interface', 'family')
                        )


def fetch_table_results(switch, command, id=None):
    payload = switch.payload(command)
    response = switch.post(payload)

    # Error checking of response
    if response is None:
        raise Exception('No response')
    if 'result' not in response:
        raise Exception('Result missing')
    if response['result'] is None:
        raise Exception('No results returned')

    if id is None:
        return response['result']['body']

    table = 'TABLE_{0}'.format(id)
    row = 'ROW_{0}'.format(id)

    return response['result']['body'][table][row]


def generate_prefix_paths(switch, vrf, verbose=False):
    command = 'show ip route vrf {0}'.format(vrf)
    vrf_data = fetch_table_results(switch, command, 'vrf')

    if vrf_data['vrf-name-out'] != vrf:
        raise Exception('VRF requested not in output')

    vrf_data = vrf_data['TABLE_addrf']['ROW_addrf']
    if vrf_data['addrf'] != 'ipv4':
        raise Exception('Was expecting IPv4 but failed')

    route_data = vrf_data['TABLE_prefix']['ROW_prefix']

    if isinstance(route_data, dict):
        route_data = [route_data]

    # Track interfaces that have been published
    interfaces = []

    for block in route_data:
        prefix = block['ipprefix']

        # This example isn't interested in connected routes
        if block['attached'] == 'true':
            continue

        paths = block['ucast-nhops']
        ip_prefix_path_count.labels(vrf=vrf, prefix=prefix).set(paths)

        if verbose:
            print(vrf, prefix, paths)

        # Trick to account for snowflake behavior
        if isinstance(block['TABLE_path']['ROW_path'], list):
            block_data = block['TABLE_path']['ROW_path']
        else:
            block_data = [block['TABLE_path']['ROW_path']]

        for path in block_data:
            # Account for I6 bug
            if 'ipnexthop' not in path:
                continue

            nexthop = path['ipnexthop']
            uptime = isodate.parse_duration(path['uptime']).total_seconds()
            uptime = int(uptime)

            ip_prefix_path_uptime.labels(
                vrf=vrf, prefix=prefix, nexthop=nexthop
                ).set(uptime)

            ifname = path['ifname']

            if ifname not in interfaces:
                interfaces.append(ifname)

                command = 'show ip interface {0}'.format(ifname)
                intf_payload = switch.payload(command)
                intf_response = switch.post(intf_payload)

                # Handle connection issue
                if intf_response is None:
                    continue

                if intf_response['result'] in ['null', None]:
                    message = 'Interface {0} show failure'.format(ifname)
                    raise Exception(message)

                # Done in 2 steps because of PEP8 line length
                intf_data = intf_response['result']['body']
                intf_data = intf_data['TABLE_intf']['ROW_intf']

                ip_prefix_path_traffic.labels(
                    interface=ifname, family='unicast'
                    ).set(intf_data['ubyte-sent'])

                ip_prefix_path_traffic.labels(
                    interface=ifname, family='multicast'
                    ).set(intf_data['mbyte-sent'])

                ip_prefix_path_traffic.labels(
                    interface=ifname, family='labeled'
                    ).set(intf_data['lbyte-sent'])

                if verbose:
                    print(ifname, intf_data['ubyte-sent'],
                          intf_data['mbyte-sent'], intf_data['lbyte-sent'])

            if verbose:
                print(vrf, prefix, nexthop, uptime)


def generate(switch, vrf='default', verbose=False):

    generate_prefix_paths(switch=switch, vrf=vrf, verbose=verbose)
