#!/usr/bin/bash

sudo dnf -y install dnf-plugins-core
sudo dnf config-manager \
    --add-repo \
    https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io
sudo grubby --update-kernel=ALL --args="systemd.unified_cgroup_hierarchy=0"

sudo systemctl enable docker

echo "You must reboot the server to enable cgroup changes for Docker:"
echo "    sudo reboot"

