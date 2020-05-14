# Automation of Docker and Container Switch Deployments

This directory contains the Python scripts to automate the setup of Docker
on your NX-OS switch using the recommended practices for protecting the
switch's control plane.

The safety of these scripts are only suitable for this demonstration.

## Requirements

This directory and its defaults assume you are using a local, Vagrant
deployed Nexus 9000v instance on your laptop/server. To set up this
environment, you should follow the instructions in the
[local-n9kv/README.md](../local-n9kv/README.md)

They should (and do) work just fine against remote Nexus 9000 (virtual
or physical) deployments with the proper arguments. Feel free to try
them out against the DevNet Sandbox environment:
[Open NX-OS with Nexus 9Kv](https://developer.cisco.com/docs/sandbox/#!data-center/featured-sandboxes)

This directory also assumes that you have build a Python virtual
environment - using virtualenv or Anaconda - with this repository's
[NXAPI Package](../nxapi/README.md) installed into that environment.
Please follow the package installation instructions and activate the
virtual environment prior to running these commands.

Finally, to deploy the container below, that container needs to be built
and pushed to a Docker compatible repository. The application in this
repository has been containerize and pushed to Docker Hub. The scripts
in this directory reference that container. The container was built using
the [container/README.md](../container/README.md) instructions.

## Common command line arguments

As mentioned above, the default host, port, username, and password
values will suffice for a local Vagrant deployment based on my
[Vagrantfile](../local-n9kv/Vagrantfile). Here are the command line
options that you can leverage to configure a remote Nexus 9000/9000v
device:

```bash
usage: script.py [-h] [-c] [-t TARGET] [-p PORT] [-u USER] [-w PASSWORD] [-v] [-s] [-x]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Provide remote hostname/IP for NXAPI
  -p PORT, --port PORT  Provide remote port for NXAPI
  -u USER, --user USER  Provide remote username for NXAPI
  -w PASSWORD, --password PASSWORD
                        Provide remote password for NXAPI
  -s, --ssl             Connect via SSL for NXAPI
  -x, --proxy           Flag proxy requirement

```

Note: use of the proxy flag when running the docker.py script
also requires modifying the script and providing the correct
proxy information. Currently, the script merely uncomments the
existing proxy settings in the Docker startup script.

Also note: use of the SSL flag assumes you have separately and
correctly configured the SSL certificates on the target Nexus 9000
device, with a known SSL Certificate authority. Testing of these
scripts with SSL use cases has not been done. Pull requests are
welcome!

## Docker Configuration

There are a great many commands to configure Docker to start and
run across switch reloads that are encoded in the docker.py script.
Extensive error handling has not been encoded as this is a demo,
although some error handling examples are built in to guide you.

```bash
python3 docker.py
```

The credentials (either default or CLI arguments provided) are used
one time in order to connect to the switch's NXAPI instance. They need
to have network-admin privileges.

## Container Deployment

The container deployment script connects via NXAPI to the Nexus 9000
device - using the default or CLI credentials provided - and executes
the **docker run** command in the switch's **bash shell** environment.

The credentials provided to the script are also provided to the container
so that the script within the container can also connect to the switch
for the periodic metric generation.

In this way, realistic, sensitive credentials are not hardcoded into
the automation environment. As such, in the example below, it is assumed
that you have defined the NXAPI_USER and NXAPI_PASS environment variables
prior to running the script. Specification of a host by *IP address only*
is required because of the docker run command requirements.

```bash
python3 container.py -t 127.0.0.1 -u ${NXAPI_USER} -w ${NXAPI_PASS}
```

To validate successful container operation, simply point a web browser
toward the container:

```bash
curl http://127.0.0.1:8888/
```

Note: the nature of this script requires it to be deployed on Nexus 9000
instances that are VXLAN EVPN VTEP devices (leafs or border devices).
Otherwise, the script as written will fail.

## Demonstrate CPU protections

The above **docker.py** script places the Docker daemon into the /ext_ser/
cgroup that contains CPU usage to 40% (per core).  This demo will simply
demonstrate that the CPU load is properly capped.

You will need two terminal windows for this demonstration - one to
monitor CPU utilization and one to stress the CPUs.

The REPO environment variable represents the top level of this GitHub
repository checkout.

* Session 1: SSH into a switch and run top

```bash
cd ${REPO}/local-n9kv
vagrant ssh

! On Nexus CLI
run bash
top
```

* Session 2: SSH into the same switch and start the stress container

```bash
cd ${REPO}/local-n9kv
vagrant ssh

! On Nexus CLI
run bash sudo ip netns exec management bash

# Nexus 9000v only has 2 vCPUs so stress them both
docker run -it --name=stress progrium/stress --cpu 2 --timeout 20
docker rm stress

# But what about a container that will spin up 6 processes/threads?
docker run -it --name=stress progrium/stress --cpu 6 --timeout 20
docker rm stress

# Exit NXOS Bash
exit

# Exit NXOS CLI
exit

```
