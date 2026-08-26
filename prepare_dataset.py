import argparse
import json
import os
import subprocess

import yaml

CONVERSION_SCRIPT = "scripts/lerobot_conversion/convert_v3_to_v2.py"
PYTHON_BIN = "python3"


def create_action_config(joints: list[str]) -> dict:
    indices = [{"start": i, "end": i + 1} for i in range(len(joints))]
    return dict(zip(joints, indices))


def create_video_config(video_angles_map: dict[str, str]) -> dict:
    return {
        new_key: {"original key": old_key}
        for old_key, new_key in video_angles_map.items()
    }


def create_modality_file(joints: list[str], video_angles_map: dict[str, str]) -> dict:
    action_config = create_action_config(joints)
    state_config = action_config
    video_config = create_video_config(video_angles_map)
    return {"state": state_config, "action": action_config, "video": video_config}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert dataset to LeRobot v2.1 and generate modality file using YAML config."
    )
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        type=str,
        help="Path to the YAML configuration file.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Load YAML configuration file
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    # Reconstruct dataset_dir and dataset_name from dataset_path
    dataset_path = os.path.abspath(config["dataset"]["path"].rstrip("/\\"))
    dataset_dir, dataset_name = os.path.split(dataset_path)

    joints = config["joints"]
    video_angles_map = config["video_angles"]

    # 1. Unconditionally run conversion script (overwrite / force replacement)
    print(f"Running conversion script on '{dataset_name}' at '{dataset_dir}'...")
    subprocess.run(
        args=[
            PYTHON_BIN,
            CONVERSION_SCRIPT,
            "--repo-id",
            dataset_name,
            "--root",
            dataset_dir,
        ],
        check=True,
    )
    print(f"Conversion script finished.")

    # 2. Build modality dictionary
    modality_file = create_modality_file(joints, video_angles_map)

    # 3. Create meta directory if it doesn't exist and save modality.json
    meta_dir = os.path.join(dataset_path, "meta")
    os.makedirs(meta_dir, exist_ok=True)

    modality_path = os.path.join(meta_dir, "modality.json")

    print(f"Writing modality config to {modality_path}...")
    with open(modality_path, mode="w") as f:
        json.dump(modality_file, f, indent=2)
    print(f"Modality config successfully written.")
