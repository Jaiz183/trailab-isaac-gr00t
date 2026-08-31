#!/bin/bash
# conversion uses it's own environment
# need to avoid fetching outdated test artifacts (don't need to run tests anyway)
git config --global lfs.fetchexclude "tests/artifacts"
cd scripts/lerobot_conversion && uv venv && source .venv/bin/activate
git lfs install && git lfs pull
source .venv/bin/activate
# may need to be run multiple times for timeouts and transient failures
uv pip install -e . --verbose
git config --global --unset lfs.fetchexclude

cd ../../
export DATASET_CONFIG="config/dataset_config.yaml"
# call venv python3 executable manually due to Singularity ROFS restrictions
export HF_HUB_OFFLINE=1
.venv/bin/python3 prepare_dataset.py --config $DATASET_CONFIG


