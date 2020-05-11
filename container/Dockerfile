FROM  fedora:latest
LABEL maintainer "Tim Miller <timmil@cisco.com>"

WORKDIR /opt

# Update all packages, install pip, clean packages
RUN     dnf update -y \
          && dnf install -y python3-pip \
          && dnf clean all

# Install required Python modules
COPY    requirements.txt /root/requirements.txt
RUN     yes | pip3 install --upgrade -r /root/requirements.txt

COPY    nxapi /opt/nxapi
ADD     generate.py vxlan.py /opt/

EXPOSE  8888
USER    nobody

ENV  NXAPI_HOST "host.docker.internal"
ENV  NXAPI_PORT "23456"
ENV  NXAPI_USER "admin"
ENV  NXAPI_PASS "admin"

CMD [ "/usr/bin/python3", "/opt/generate.py", "--container" ]

