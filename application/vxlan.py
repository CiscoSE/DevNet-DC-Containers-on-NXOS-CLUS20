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

# Import modules from 3rd parties
import prometheus_client

# Import modules from this repo


# Persistent Data
fabric_data = None


# Prometheus data
interface_state = prometheus_client.Gauge(
    'interface_state', 'Track Interface State', ('name', 'type')
)

vni_state = prometheus_client.Gauge(
    'vni_state', 'Track VNI State', ('vni', 'type', 'id', 'mcast')
)

l2route_seqn = prometheus_client.Gauge(
    'l2route_seq_number', 'Track sequence number for Type-2 routes',
    ('mac', 'ip', 'nh', 'vlan')
)

class vxlanException(Exception):
    pass

class fabric:
    """
    Class in which fabric related persistent data will reside
    """

    def __init__(self):
        self.ip = {
            'loopback0': None,
            'loopback1': None,
            'loopback100': None,
        }

        self.interfaces = {
            'all': [],
            'connected': [],
            'notconnect': [],
            'disabled': [],
            'fabric-links': [],
            'dci-links': [],
        }

        self.nve = []
        self.l2route = []

def fetch_table_results(switch, command, id=None):
    payload = switch.payload(command)
    response = switch.post(payload)

    # Error checking of response
    if response is None:
        raise vxlanException('No response')
    if 'result' not in response:
        raise vxlanException('Result missing')
    if response['result'] is None:
        raise vxlanException('No results returned')

    if id is None:
        return response['result']['body']
    
    table = 'TABLE_{0}'.format(id)
    row = 'ROW_{0}'.format(id)

    return response['result']['body'][table][row]


def generate_l2route(switch, first_run=False):
    global fabric_data

    response = fetch_table_results(switch, 
        'show l2route evpn mac-ip all', id='l2route_mac_ip_all'
    )

    latest = []
    for x in response:
        mac = x['mac-addr']
        ip = x['host-ip']
        nh = x['next-hop1']
        vlan = x['topo-id']
        seq = int(x['seq-num']) + 1

        l2route_seqn.labels(mac=mac, ip=ip, nh=nh, vlan=vlan).set(seq)

        latest.append(
            {
                'vlan': vlan,
                'mac': mac,
                'ip': ip,
                'nh': nh,
                'seq': seq
            }
        )

    fabric_data.l2route = latest
    return


def generate_nve(switch, first_run=False):
    global fabric_data

    response = fetch_table_results(switch, 'show nve vni', id='nve_vni')

    state_labels = {
        'Up': 1,
        'Down': 0,
    }

    latest = []
    for x in response:
        vni = x['vni']
        state = state_labels[x['vni-state']]
        vni_type = x['type'][0:2]
        id = x['type'][4:-1]
        mcast = x['mcast']

        vni_state.labels(vni=vni, type=vni_type, id=id, mcast=mcast).set(state)

        latest.append(
            {
                'vni': vni,
                'state': state,
                'type': vni_type,
                'id': id,
                'mcast': mcast
            }
        )

    fabric_data.nve = latest
    return


def generate_interfaces(switch, first_run=False):
    global fabric_data

    response = fetch_table_results(switch, 'show interface status', 'interface')

    connected = []
    notconnect = []
    disabled = []
    int_type = {}
    
    for x in response:
        if x['vlan'] == '--':
            continue
        if x['state'] == 'connected':
            connected.append(x['interface'])
        elif x['state'] == 'notconnect':
            notconnect.append(x['interface'])
        else:
            disabled.append(x['interface'])

        int_type[x['interface']] = x['vlan']

    interfaces = connected + notconnect + disabled

    for i in connected:
        t = int_type[i]
        interface_state.labels(name=i, type=t).set(1)

    for i in notconnect:
        t = int_type[i]
        interface_state.labels(name=i, type=t).set(0)

    for i in disabled:
        t = int_type[i]
        interface_state.labels(name=i, type=t).set(-1)

    fabric_data.interfaces['all'] = interfaces
    fabric_data.interfaces['connected'] = connected
    fabric_data.interfaces['notconnect'] = notconnect
    fabric_data.interfaces['disabled'] = disabled

    return


def generate(switch, verbose=False):
    """
    Entry generate() point for other modules to call.
    
    Connection object 'switch' expected with valid connection information
    pre-populated and ready to consume
    """

    global fabric_data
    if fabric_data is None:
        fabric_data = fabric()
        first_run = True
    else:
        first_run = False

    generate_interfaces(switch, first_run)

    try:
        generate_nve(switch, first_run)
    except vxlanException:
        pass

    try:
        generate_l2route(switch, first_run)
    except vxlanException:
        pass

    # In a more perfect world, these would be classes and would
    # handle their own representation efforts.
    if verbose:
        print('Interface Data')
        for i in ['connected', 'notconnect', 'disabled']:
            print(i)
            print(fabric_data.interfaces[i])

        print('NVE Data')
        for entry in fabric_data.nve:
            print(entry)

        print('L2ROUTE Data')
        for entry in fabric_data.l2route:
            print(entry)
