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
## Gr00t Peculiarities
- Suggests excluding annotation key from modality.json in docs, but requires annotation key for finetuning
- Annotation keys must be named in a specific format
## Git
- Push and pull in singularity because git-lfs is needed
## Instructions
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