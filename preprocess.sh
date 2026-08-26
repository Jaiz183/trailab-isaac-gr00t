#!/bin/bash

uv run python3 prepare_dataset.py --config $DATASET_CONFIG

export DATASET_CONFIG="config/dataset_config.yaml"
