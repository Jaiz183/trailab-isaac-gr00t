# Notes
## Installation
- torchcodec installation issue - ffmpeg isn't installed
- If any docker installs time out, install them before building the image - docker pull (nvidia/cuda:12.8.0-devel-ubuntu24.04)
- uv syncs may time out but typically due to repeated transient failures or big installs, just re-run multiple times after increasing timeout param because previously completed installs are cached
- Singularity has weird quirks around it's filesystem, so uv runs don't work
- Singularity also needs you to bind all non-default paths on the host to make them visible, so that can cause errors
## Setup
- Log into HF and obtain access to VLM on HF before running any files (`hf auth login` and `--force` option if already logged in)
- Any changes in access => log in again with revalidated access token
## Helpful Commands
- `rsync -avzP` - archive folders, verbose, compress and extract w/o intermediate files, progress
  - Note that this command archives all subfolder and transfers them to the dest., not including the parent folder. Create a destination folder first.
## Gr00t Peculiarities
- Suggests excluding annotation key from modality.json in docs, but requires annotation key for finetuning
- Annotation keys must be named in a specific format
## Git
- Push and pull in singularity because git-lfs is needed
## Training Instructions
1. Run `setup.sh`.
2. Start singularity shell w/ appropriate bindings
```
singularity shell --nv \
  -B /raid/datasets/trossen:/raid/datasets/trossen \
  -B /home/trossen/Desktop/models/trailab-isaac-gr00t:/home/trossen/Desktop/models/trailab-isaac-gr00t \
  --pwd /home/trossen/Desktop/models/trailab-isaac-gr00t \
  singularity/gr00t.sif
```
3. Modify `config/dataset_config.yaml` and `training_config.yaml` to match the dataset to be trained on and your preferred training configuration.
4. Run `preprocess.sh`.
5. Modify the job name in `finetune.sbatch`.
6. Schedule fintetune.sbatch outside the singularity shell.
## Inference Instructions

For this PC's Trossen arms, use the native N1.7 runner. The installed LeRobot
policy is N1.5 and does not load these checkpoints directly.

```bash
cd /home/trossen/Desktop/TRAILAB
GR00T_RECORDING="$PWD/dataset/eval/gr00t_handover_$(date +%Y%m%d_%H%M%S)"
NO_ALBUMENTATIONS_UPDATE=1 models/trailab-isaac-gr00t/.venv/bin/python -u \
  models/trailab-isaac-gr00t/run_robot.py \
  --checkpoint "$PWD/results/gr00t_handover-cube_rand/checkpoint-2000" \
  --robot-config "$PWD/Trossen-Dual-Arm/config/inference-cube_rand.yaml" \
  --output "$GR00T_RECORDING" \
  --task "pick up the cube from the desk with one arm, hand it to the other hand, and put it down on the desk again" \
  --seconds 180 --joint-limit-response hold --stage --execute
```

This moves both arms and records all four cameras. Omit `--stage --execute`
for live prediction and recording without motion. The output includes four
individual MP4s, `four_cameras.mp4`, action logs, camera timestamps, and
`summary.json`. Each run needs a new output directory.

Out-of-range action chunks are rejected; the robot holds its measured pose and
replans while the three-minute timer and recording continue. Actual commands
remain bounded by controller joint limits and slew rates. Controller faults,
nonfinite outputs, stale cameras, excessive inference latency, and tracking
errors still stop motion. Ctrl-C holds the arms and finalizes the recording.
`--joint-limit-response stop` restores immediate termination on rejected chunks.

The local SDK must be `trossen-arm==1.10.0` to match firmware 1.10.0. Install
camera support with `uv sync --extra robot` from this model directory.

See [the rig inference guide](../../Trossen-Dual-Arm/doc/inference.md#gr00t-n17-on-robot-with-four-camera-recording)
for recording contents, checkpoint locations, command-rate measurements, and
recorded-observation evaluation.

### Verified local recording

The three-minute physical run completed on 2026-09-19:
`dataset/eval/gr00t_handover_live_003/four_cameras.mp4` under the TRAILAB root.
The video is 183.83 s including staging. The rollout sent 2,944 policy commands,
rejected 280 chunks, and spent 59.67 s holding/replanning. All sent targets
stayed within controller limits. Overall command rate was 16.43 Hz, with
~29.9 Hz between inference/hold pauses. This validates duration and recording;
it does not establish task success. Full logs and per-camera videos are saved
in the same episode directory.
