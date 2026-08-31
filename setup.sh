#!/bin/bash
source .venv/bin/activate
# download wheels w/ git lfs pull
git lfs install && git lfs pull
# sync packages (may need to be re-run due to timeout)
# outside singularity bc it has a read-only filesystem
uv sync --python 3.12
uv pip install mpi4py libmpi

