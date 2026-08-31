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