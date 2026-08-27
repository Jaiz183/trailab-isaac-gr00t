#!/bin/bash
export DATASET_CONFIG="config/dataset_config.yaml"
uv run python3 prepare_dataset.py --config $DATASET_CONFIG


