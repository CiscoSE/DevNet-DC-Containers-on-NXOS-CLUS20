# Nexus 9000 NX-API Interface

This Python package is designed to provide an easy to consume
interface for making connections to Nexus 9000 switches, leveraging
the NX-API programmability feature.

This package is primarily developed to support several DevNet
programmability sessions for Cisco Live but can be used for general
purposes.

The package defaults - specifically, credentials and non-SSL communication -
are hard coded with the Nexus 9000v virtual box appliance in mind. So,
despite the 'bad practice' of hard coding user credentials, these credentials
are well known.

Note: if you are looking for something more feature rich, you might consider
the nxapi_plumbing package found here: <https://github.com/ktbyers/nxapi-plumbing>
I have not used it myself nor do I know the author. Your mileage may vary.

## Package Installation Instructions

Standard Python package installation methods, after activating your Python
virtual environment (${VENV} is the path to your virtual environment).

```bash
source ${VENV}/bin/activate
python setup.py install
```

## Packages Examples

Run the "show version" CLI command on the switch and extract the NX-OS version.

```python
from nxapi import connection

switch = connection(
            host='localhost',
            port='80',
            username='admin',
            password='admin
         )

payload = switch.payload('show version')
response = switch.post(payload)

# Print the running switch version
print(response['result']['body']['nxos_ver_str'])
```
