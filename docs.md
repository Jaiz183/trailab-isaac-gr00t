# Notes
## Installation
- torchcodec installation issue - ffmpeg isn't installed
- If any docker installs time out, install them before building the image - docker pull (nvidia/cuda:12.8.0-devel-ubuntu24.04)
## Setup
- Log into HF and obtain access to VLM on HF before running any files (`hf auth login` and `--force` option if already logged in)
- Any changes in access => log in again with revalidated access token
## Helpful Commands
- `rsync -avzP` - archive folders, verbose, compress and extract w/o intermediate files, progress