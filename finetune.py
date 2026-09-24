#!/usr/bin/env python3

import os
from math import ceil

import yaml

dataset_config = "config/dataset_config.yaml"
training_config = "config/training_config.yaml"

with open(dataset_config) as config_file:
    dataset_root = yaml.safe_load(config_file)['dataset']['path']

num_gpus = "2"
prep_modality_file = (
    "/home/trossen/Desktop/models/trailab-isaac-gr00t/prepare_modality_config.py"
)

with open(training_config) as config_file:
    training = yaml.safe_load(config_file)

output_dir = f"{training['output_dir']}/{training['model_name']}"
max_steps = training["num_steps"]
num_saves = training["num_saves"]
save_steps = ceil(max_steps / num_saves)
resume_from_checkpoint = training["resume_from_checkpoint"]
val_step_size = training["val_step_size"]
validation_dataset_path = training.get("validation_dataset_path", f"{dataset_root}_val")


master_port = "29500"

torchrun = ".venv/bin/torchrun"
command = [
        torchrun,
        "--nproc_per_node=" + num_gpus,
        "--master_port=" + master_port,
        "gr00t/experiment/launch_finetune.py",
        "--base-model-path",
        "nvidia/GR00T-N1.7-3B",
        "--dataset-path",
        f"{dataset_root}_train",
        "--validation-dataset-path",
        validation_dataset_path,
        "--embodiment-tag",
        "NEW_EMBODIMENT",
        "--modality-config-path",
        prep_modality_file,
        "--num-gpus",
        num_gpus,
        "--output-dir",
        output_dir,
        "--save-total-limit",
        str(num_saves),
        "--save-steps",
        str(save_steps),
        "--max-steps",
        str(max_steps),
        "--use-wandb",
        "--global-batch-size",
        "32",
        "--color-jitter-params",
        "brightness",
        "0.3",
        "contrast",
        "0.4",
        "saturation",
        "0.5",
        "hue",
        "0.08",
        "--dataloader-num-workers",
        "4",
        "--eval-strategy",
        "steps",
        "--eval-steps",
        str(val_step_size),
    ]

if resume_from_checkpoint:
    command.append(f"--resume-from-checkpoint")

os.execvpe(
    torchrun,
    command,
    os.environ,
)
