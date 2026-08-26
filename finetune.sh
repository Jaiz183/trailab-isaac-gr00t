#!/bin/bash

export DATASET="/raid/datasets/trossen/dataset/handover-cube_rand"
export NUM_GPUS=2
export PREP_MODALITY_FILE="/home/trossen/Desktop/models/gr00t/prepare_modality_config.py"
export OUTPUT_DIR="/raid/datasets/trossen/results/gr00t_handover-cube_rand"
export MASTER_PORT=29500

exec uv run torchrun \
    --nproc_per_node="$NUM_GPUS" \
    --master_port="$MASTER_PORT" \
    gr00t/experiment/launch_finetune.py \
    --base-model-path nvidia/GR00T-N1.7-3B \
    --dataset-path "$DATASET" \
    --embodiment-tag NEW_EMBODIMENT \
    --modality-config-path "$PREP_MODALITY_FILE" \
    --num-gpus "$NUM_GPUS" \
    --output-dir "$OUTPUT_DIR" \
    --save-total-limit 5 \
    --save-steps 2000 \
    --max-steps 2000 \
    --use-wandb \
    --global-batch-size 32 \
    --color-jitter-params brightness 0.3 contrast 0.4 saturation 0.5 hue 0.08 \
    --dataloader-num-workers 4