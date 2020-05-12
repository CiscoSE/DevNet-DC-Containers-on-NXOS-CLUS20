# Application Containerization

This directory contains the Dockerfile required to build the
container that will be deployed on the Nexus 9000 switches.

## Build instructions

The Dockerfile will use contents from multiple subdirectories
within this repository. The **docker build** command below assumes
you are running from the *current* directory that this README.md
file is located in.

```bash
docker build -t devnet-dc-clus20/vxlan:latest -t devnet-dc-clus20/vxlan:1 -f Dockerfile ..
```

The image tags (*devnet-dc-clus20/vxlan:latest* and *devnet-dc-clus20/vxlan:1*)
can be safely used for this command as they only apply locally. If you are
going to push this image to your own Docker Hub repository, you'll either
use different tags

## Publish instructions

Again, these instructions are specific to this session and artifacts.
You'll need to change the final tags and repository names to match your
environment.

### Apply new Docker Hub relevant tags to the image

```bash
docker tag devnet-dc-clus20/vxlan:latest gvevsetim/devnet-dc-clus20:latest
docker tag devnet-dc-clus20/vxlan:1 gvevsetim/devnet-dc-clus20:1
```

### Push images to Docker Hub

```bash
docker login
docker push gvevsetim/devnet-dc-clus20:latest
docker push gvevsetim/devnet-dc-clus20:1
```

## References

- [Docker: Build and Run Your Image](https://docs.docker.com/get-started/part2/)
- [Docker: Share Images on Docker Hub](https://docs.docker.com/get-started/part3/)
