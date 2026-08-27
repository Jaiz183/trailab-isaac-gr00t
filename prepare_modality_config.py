import yaml
from typing import Dict

from gr00t.configs.data.embodiment_configs import register_modality_config
from gr00t.data.embodiment_tags import EmbodimentTag
from gr00t.data.types import (
    ModalityConfig,
    ActionConfig,
    ActionRepresentation,
    ActionType,
    ActionFormat,
)


def build_modality_config(
    yaml_path: str,
    action_horizon: int = 16,
    language_key: str = "annotation.human.task_description",
) -> Dict[str, ModalityConfig]:
    """
    Builds a GR00T modality configuration dictionary from a dataset YAML file[cite: 1].
    Reads optional ActionConfig overrides directly from the YAML joints definition.
    """
    with open(yaml_path, "r") as f:
        config_data = yaml.safe_load(f)

    # 1. Video keys: Extract the mapped (new) camera names
    video_angles = config_data.get("video_angles", {})
    video_keys = list(video_angles.values())

    # 2. State & Action keys: Extract from the joints dictionary
    joints_dict = config_data.get("joints", {})
    state_keys = list(joints_dict.keys())
    action_keys = list(joints_dict.keys())

    # 3. Build action_configs list (must match same length and order as modality_keys)[cite: 1]
    action_configs = []
    for key, overrides in joints_dict.items():
        # If no overrides were provided (e.g., `{}` or `null` in YAML), default to an empty dict
        if overrides is None:
            overrides = {}

        # Extract string values from YAML or apply defaults[cite: 1]
        rep_str = overrides.get("rep", "RELATIVE")
        type_str = overrides.get("type", "NON_EEF")
        format_str = overrides.get("format", "DEFAULT")
        state_key = overrides.get("state_key", None)

        # Convert strings to their respective Enum classes[cite: 1]
        action_configs.append(
            ActionConfig(
                rep=getattr(ActionRepresentation, rep_str),
                type=getattr(ActionType, type_str),
                format=getattr(ActionFormat, format_str),
                state_key=state_key,
            )
        )

    # 4. Construct the full modality configuration object[cite: 1]
    modality_config = {
        "video": ModalityConfig(
            delta_indices=[0],  # Use [0] for the current timestep[cite: 1]
            modality_keys=video_keys,
        ),
        "state": ModalityConfig(
            delta_indices=[0],  # Use [0] for the current timestep[cite: 1]
            modality_keys=state_keys,
        ),
        "action": ModalityConfig(
            delta_indices=list(
                range(0, action_horizon)
            ),  # Use positive indices for action horizons[cite: 1]
            modality_keys=action_keys,
            action_configs=action_configs,
        ),
        "language": ModalityConfig(
            delta_indices=[0],
            modality_keys=[language_key],
        ),
    }

    return modality_config


def register_custom_embodiment(yaml_path: str) -> None:
    """
    Helper function that builds and registers the modality configuration[cite: 1].
    """
    config = build_modality_config(yaml_path)
    register_modality_config(config, embodiment_tag=EmbodimentTag.NEW_EMBODIMENT)


register_custom_embodiment(
    "/home/trossen/Desktop/models/trailab-isaac-gr00t/config/dataset_config.yaml"
)
