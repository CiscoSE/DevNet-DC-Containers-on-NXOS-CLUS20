# Setting up Nexus 9000v using Vagrant

This directory and instructions are provided to guide you in
setting up a developer NX-OS environment on your local laptop for
your scripting environment.

The concept follows the [NetDevOps](https://blogs.cisco.com/developer/embrace-netdevops-part-1)
methodology where you develop your network configuration changes
against a development environment, which in this repository is
a Nexus 9000v image running locally on your laptop. We will spin
up the Nexus 9000v using [Vagrant](https://www.vagrantup.com/).

## Nexus 9000v Vagrant Box

You'll first need to download the Nexus 9000v image from Cisco's
[software download](https://software.cisco.com/download/home/286312239/type/282088129/release/9.3(4))
website.

This repository is using the 9.3(3) version of NX-OS.

You'll need to add the image (or "box") to Vagrant via:

```bash
vagrant box add nxos/9.3.3 nexus9300v.9.3.3.box
```

Once registered, from this modules directly - specifically, with the
included Vagrantfile in the current directory - start the Vagrant box
image:

```bash
vagrant up
```

The virtual image takes some time to complete the boot process. You can
connect to the serial console of the virtual switch via:

```bash
telnet localhost 2023
```

## Configure the NXOSv image for NXAPI and boot variable

Once the image has completed booting, we need to enable the NXAPI
feature on the switch.

```bash
bash -x enable_nxapi.sh
```

## References

- [Vagrant](https://www.vagrantup.com/)
- [Nexus 9000v Guide](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/nx-osv-93-95/configuration/guide/cisco-nexus-9000v-9300v-9500v-guide-93x.html)
