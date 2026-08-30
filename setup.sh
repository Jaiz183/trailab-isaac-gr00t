#!/bin/bash

# build docker image and port to singularity in docker image
docker/build.sh
mkdir -p singularity
docker run --rm \
  --privileged \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)":/output \
  ghcr.io/apptainer/apptainer:1.3.0 \
  apptainer -v build /output/singularity/gr00t.sif docker-daemon:gr00t:latest

# download wheels w/ git lfs pull
singularity exec singularity/gr00t.sif git lfs pull
# sync packages
uv sync --python 3.12

source .venv/bin/activate
uv pip install mpi4py libmpi

