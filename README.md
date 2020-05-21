# DevNet-DC-Containers-on-NXOS-CLUS20

Cisco Live Virtual US 2020 DevNet Day DC Track - Lightning talk
on Containerized Apps on NXOS.   Repo has code to setup the demo
environment and run the demo.

The directory structure maps to the various components of the
demo environment as follows:

- [Local Nexus 9000v](local-n9kv/README.md): Instructions for deploying
  the Nexus 9000v virtual switch using Vagrant and Virtual Box. Use this
  directory to test the application, container, and monitoring components.
- [NX-API Connection Library](nxapi/README.md): A minimalist Python
  package I wrote to simplify connection handling and payload processing.
  You'll install this in your Python virtual environment.
- [Customized Metrics Application](application/README.md): The Python
  scripting for this demo to generate customized metrics and make them
  available for Prometheus collection. This is the "application" that will
  be containerized and run on the Nexus 9000 switches.
- [Containerization](container/README.md): The instructions and Dockerfile
  needed to build the application container.  This is for your reference
  as the demo can leverage the existing, published container from Docker Hub.
- [Switch Setup](switch/README.md): Configuration scripts and instructions
  for deploying Docker on your Nexus 9000 switch as well as deploying the
  application container.
- [Centralized Monitoring Setup](monitoring/README.md): Instructions and
  scripts to install and setup Prometheus and Grafana containers on a Linux
  server to collect the metrics from your Nexus 9000 containerized
  application.

As you can see, there are many parts to this demo but, if you simply want
to try out the application I've built, only the [NX-API](nxapi/README.md),
[Switch Setup](switch/README.md), and [Monitoring](monitoring/README.md)
directories are required.
