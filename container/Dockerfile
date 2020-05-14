FROM  fedora:latest
LABEL maintainer "Tim Miller <timmil@cisco.com>"

# Update all packages, install pip, clean packages
RUN     dnf update -y \
            && dnf install -y python3-pip \
            && dnf clean all

# Copy Python package source
COPY    nxapi /root/nxapi
WORKDIR /root/nxapi

# Install required Python modules
RUN     python3 setup.py install

COPY    application /opt/
WORKDIR /opt

# Ensure all dependencies are installed
RUN     yes | pip3 install -r /opt/requirements.txt

EXPOSE  8888
USER    nobody

ENV  NXAPI_HOST "host.docker.internal"
ENV  NXAPI_PORT "23456"
ENV  NXAPI_USER "admin"
ENV  NXAPI_PASS "admin"

CMD [ "/usr/bin/python3", "/opt/generate.py", "--container" ]

