#!/usr/bin/env python3

import os

import yaml

dataset_config = "config/dataset_config.yaml"
training_config = "config/training_config.yaml"

with open(dataset_config) as config_file:
    dataset = yaml.safe_load(config_file)["dataset"]["path"]

with open(training_config) as config_file:
    training = yaml.safe_load(config_file)

num_steps = training["num_steps"]
model_path = os.path.join(training["output_dir"], f"checkpoint-{num_steps}")
action_horizon = training["action_horizon"]
modality_keys = training["modality_keys"]
test_episodes = training["test_episodes"]

command = [
    "uv",
    "run",
    "python",
    "gr00t/eval/open_loop_eval.py",
    "--dataset-path",
    dataset,
    "--embodiment-tag",
    "NEW_EMBODIMENT",
    "--model-path",
    model_path,
    "--traj-ids",
    *[str(episode) for episode in test_episodes],
    "--execution-horizon",
    str(action_horizon),
    "--steps",
    "400",
]

if modality_keys:
    command.extend(["--modality-keys", *modality_keys])

os.execvp(
    "uv",
    command,
)
