# Centralized Monitoring Service

On a Linux system (this demo leverages Fedora 31, Server spin), we will
install and setup Docker, and deploy the containers for Prometheus and
Grafana.

## Install Docker

All of these commands are found in the **setup_f31.sh** and **setup_proxy.sh**
scripts in this directory. They are broken out here to explain what is being
done in case you are using a different Linux distribution.

Add Docker CE Yum repository:

```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo \
    https://download.docker.com/linux/fedora/docker-ce.repo
```

Install Docker packages:

```bash
sudo dnf install -y docker-ce docker-ce-cli containerd.io
```

Change cgroup behavior:

```bash
sudo grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=0"
sudo reboot
```

If proxy setup required, modify the entries in http-proxy.conf to
match your environment and then copy the file to the proper location:

```bash
sudo mkdir /etc/systemd/system/docker.service.d
sudo cp http-proxy.conf /etc/systemd/system/docker.service.d

sudo systemctl daemon-reload
```

Enable and start Docker:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

## Setup Docker Networking

Create the new Docker bridge network **demo0** - this provides the
nifty feature of docker container name resolution working within each
container:

```bash
    sudo docker network create --driver=bridge --subnet=192.168.254.0/24 \
                          --gateway=192.168.254.254 --attachable demo0
```

## Deploy Prometheus container

Note: the prometheus.yml configuration is for the author's private lab.
You will need to change the job_name entries to point to the switches
in your environment.

```bash
    sudo docker run --name prometheus -d -p 9999:9090 \
            -v ${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml \
            quay.io/prometheus/prometheus
```

## Deploy Grafana container

```bash
    docker run --name grafana -d --network demo0 -p 3000:3000 \
            grafana/grafana
```

Once Grafana has started, log into the web interface - URL is
'http://server_ip:3000' - with the credentials of admin/admin. Import the
grafana JSON file provided in this directory to provision the dashboards
seen in the presentation.
