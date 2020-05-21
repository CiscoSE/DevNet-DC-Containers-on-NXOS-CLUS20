#!/usr/bin/env

# https://stackoverflow.com/questions/23111631/cannot-download-docker-images-behind-a-proxy
sudo mkdir /etc/systemd/system/docker.service.d
sudo cp http-proxy.conf /etc/systemd/system/docker.service.d

sudo systemctl daemon-reload
sudo systemctl restart docker

