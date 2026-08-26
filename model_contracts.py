from gr00t.data.embodiment_tags import EmbodimentTag
from gr00t.policy import Gr00tPolicy
from tabulate import tabulate

BASE_MODEL_PATH = "nvidia/GR00T-N1.7-3B"
BASE_EMBODIMENTS = [
    EmbodimentTag.OXE_DROID_RELATIVE_EEF_RELATIVE_JOINT,
    EmbodimentTag.XDOF,
    EmbodimentTag.XDOF_SUBTASK,
    EmbodimentTag.REAL_G1,
    EmbodimentTag.REAL_R1_PRO_SHARPA,
    EmbodimentTag.REAL_R1_PRO_SHARPA_HUMAN,
    EmbodimentTag.REAL_R1_PRO_SHARPA_MAXINSIGHTS,
    EmbodimentTag.REAL_R1_PRO_SHARPA_MECKA,
]

def generate_contracts_table(model_path: str, embodiments: list, tablefmt: str = "github") -> str:
    headers = [
        "Embodiment Tag",
        "Expected Cameras",
        "Video Horizon",
        "Expected States",
        "State Horizon",
        "Action Outputs",
        "Action Horizon",
    ]
    
    rows = []

    for embodiment in embodiments:
        policy = Gr00tPolicy(
            model_path=model_path,
            embodiment_tag=embodiment,
            device="cpu",
            strict=True,
        )

        modality_configs = policy.get_modality_config()

        # Format list outputs cleanly as comma-separated strings
        video_keys = ", ".join(modality_configs["video"].modality_keys)
        video_horizon = len(modality_configs["video"].delta_indices)

        state_keys = ", ".join(modality_configs["state"].modality_keys)
        state_horizon = len(modality_configs["state"].delta_indices)

        action_keys = ", ".join(modality_configs["action"].modality_keys)
        action_horizon = len(modality_configs["action"].delta_indices)

        rows.append([
            embodiment.name,
            video_keys,
            video_horizon,
            state_keys,
            state_horizon,
            action_keys,
            action_horizon,
        ])

    # tabulate auto-calculates and pads column widths dynamically
    return tabulate(rows, headers=headers, tablefmt=tablefmt)


if __name__ == "__main__":
    # Choose tablefmt:
    # - "github" / "pipe" -> Markdown tables
    # - "fancy_grid" / "grid" -> Pretty ASCII borders for terminal output
    # - "simple" -> Minimalist auto-aligned text
    print(generate_contracts_table(BASE_MODEL_PATH, BASE_EMBODIMENTS, tablefmt="fancy_grid"))