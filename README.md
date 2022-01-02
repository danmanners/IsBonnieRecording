# Is Bonnie Recording

Simple frontend and backend to allow my Voice Over Actress wife ([here](https://vosuperhero.com)) to turn on a USB LED in my office to tell me to be quiet so she can record 😂😂

## How does this work and...why

I'm leveraging a [blink(1)](https://blink1.thingm.com/) LED light to turn on/off when my wife needs to tell me to be quiet when she needs to record. The frontend is written in [Svelte](https://svelte.dev/) and is quite simple, and the backend is Python which utilizes [Flask](https://flask.palletsprojects.com/en/2.0.x/) and the [blink(1) Python Library](https://pypi.org/project/blink1/) to turn the light on and off via JSON POSTs with a simple REST API. The node selection works in conjunction with [node-feature-discovery](https://github.com/kubernetes-sigs/node-feature-discovery), which is a fantastic way to map physically connected devices to nodes.

![ButWhy](https://media2.giphy.com/media/s239QJIh56sRW/giphy.gif)

The few big pushes for this project have been:

- I wanted to prove _at least slightly_ capable with modern frontend frameworks
- I wanted to leverage node auto-selection based on **where** the USB blink(1) devices is connected
- I wanted to have a simple button to press to turn on a light no matter where my wife was to tell me she needs to record
- I wanted to have a good example of multi-architecture containers without having to make any architecture-specific settings in the Kubernetes deployment manifest

## Technologies Leveraged / Utilized

- Svelte (Frontend)
- Python3 (Backend)
  - Flask
- Hardware
  - Blink(1)
  - Turing Pi v2
- Kubernetes
  - Traefik v2
  - Cert-Manager
  - node-feature-discovery
  - podman
  - buildah
  - NGINX

## Local Development

From the root directory, you'll want to build both containers:

```bash
podman build -t localhost/ibr-frontend:dev frontend
podman build -t localhost/ibr-backend:dev backend
```

Using [podman](https://podman.io/), we can then deploy things easily enough:

```bash
podman play kube manifests/deployment-dev.yaml
```

If you want to shut it down or re-deploy, run:

```bash
podman play kube manifests/deployment-dev.yaml --down
```

## Production Deployment

1. Ensure that the containers are built appropriately and pushed up to Docker Hub.

```bash
# Set the Git Tag
export docker_tag="v0.1.1"

# Create the Frontend Manifest
buildah manifest create isbonrecording-frontend

# Build Frontend Images
buildah bud --tag "ghcr.io/danmanners/isbonrecording-frontend:${docker_tag}" \
  --manifest isbonrecording-frontend \
  --arch amd64 frontend

buildah bud --tag "ghcr.io/danmanners/isbonrecording-frontend:${docker_tag}" \
  --manifest isbonrecording-frontend \
  --arch arm64 frontend

# Push Frontend Images
buildah manifest push --all \
  isbonrecording-frontend "docker://ghcr.io/danmanners/isbonrecording-frontend:${docker_tag}"

# Create the Backend Manifest
buildah manifest create isbonrecording-backend

# Build Backend Images
buildah bud --tag "ghcr.io/danmanners/isbonrecording-backend:${docker_tag}" \
  --manifest isbonrecording-backend \
  --arch amd64 backend

buildah bud --tag "ghcr.io/danmanners/isbonrecording-backend:${docker_tag}" \
  --manifest isbonrecording-backend \
  --arch arm64 backend

# Push Backend Images
buildah manifest push --all \
  isbonrecording-backend "docker://ghcr.io/danmanners/isbonrecording-backend:${docker_tag}"
```

2. Deploy/Update the Kubernetes Manifest

```bash
kubectl apply -k manifests
```

3. ???

4. Profit!
