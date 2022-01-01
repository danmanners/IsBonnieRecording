# Is Bonnie Recording

Simple frontend and backend to allow my Voice Over Actress wife ([here](https://vosuperhero.com)) to turn on a USB LED to tell me to shut up so she can record 😂😂

## How does this work

I'm leveraging a [blink(1)](https://blink1.thingm.com/) LED light to turn on/off when my wife needs to tell me to be quiet when she needs to record. The frontend is written in [Svelte](https://svelte.dev/) and is quite simple, and the backend is Python which utilizes [Flask](https://flask.palletsprojects.com/en/2.0.x/) and the [blink(1) Python Library](https://pypi.org/project/blink1/) to turn the light on and off via JSON POSTs with a simple REST API.

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

## Prod Deployment

1. Ensure that the containers are built appropriately and pushed up to Docker Hub.

```bash
# Git Short SHA
export GSSHA="$(git rev-parse --short HEAD)"

# Build Images
podman build -t "docker.io/danielmanners/isbonrecording-frontend:${GSSHA}" frontend
podman build -t "docker.io/danielmanners/isbonrecording-backend:${GSSHA}" backend

# Push Images
podman push "docker.io/danielmanners/isbonrecording-frontend:${GSSHA}"
podman push "docker.io/danielmanners/isbonrecording-backend:${GSSHA}"
```
