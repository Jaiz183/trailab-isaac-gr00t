#!/bin/bash
source .venv/bin/activate
# download wheels w/ git lfs pull
singularity exec --nv \
  -B /raid/datasets/trossen:/raid/datasets/trossen \
  -B /home/trossen/Desktop/models/trailab-isaac-gr00t:/home/trossen/Desktop/models/trailab-isaac-gr00t \
  --pwd /home/trossen/Desktop/models/trailab-isaac-gr00t \
  singularity/gr00t.sif \
  bash -c "git lfs install && git lfs pull"
# sync packages (may need to be re-run due to timeout)
# outside singularity bc it has a read-only filesystem
uv sync --python 3.12

