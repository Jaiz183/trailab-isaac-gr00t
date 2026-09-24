#!/usr/bin/env python3

import os
import subprocess

import yaml

dataset_config = "config/dataset_config.yaml"
training_config = "config/training_config.yaml"
open_loop_inference_config = "config/open_loop_inference.yaml"

with open(dataset_config) as config_file:
    dataset = yaml.safe_load(config_file)

with open(training_config) as config_file:
    training = yaml.safe_load(config_file)

with open(open_loop_inference_config) as config_file:
    open_loop_inference = yaml.safe_load(config_file)

checkpoint = open_loop_inference["checkpoint"]
dataset_type = open_loop_inference["dataset_type"]
model_name = training["model_name"]
action_horizon = training["action_horizon"]
modality_keys = training["modality_keys"]
test_episodes = open_loop_inference["test_episodes"]

for cp in checkpoint:
    for dt in dataset_type:
        # retrieve args
        cp_folder = f"checkpoint-{cp}"
        dataset_path = f"{dataset['dataset']['path']}_{dt}"
        save_path = os.path.join(open_loop_inference["save_path"], model_name, dt, cp_folder)
        model_path = os.path.join(training["output_dir"], model_name, cp_folder)
        command = [
            "uv",
            "run",
            "--no-sync",
            "python",
            "-m",
            "gr00t.eval.open_loop_eval",
            "--dataset-path",
            dataset_path,
            "--embodiment-tag",
            "NEW_EMBODIMENT",
            "--model-path",
            model_path,
            "--traj-ids",
            *[str(episode) for episode in test_episodes],
            "--execution-horizon",
            str(action_horizon),
            "--steps",
            "1000",
            "--save-plot-path",
            save_path
        ]

        if modality_keys:
            command.extend(["--modality-keys", *modality_keys])

        subprocess.run(command, check=True)
