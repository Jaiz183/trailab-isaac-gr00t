#!/bin/bash

#SBATCH --job-name=gr00t_finetune_handover-cube_rand
#SBATCH --partition=batch
#SBATCH --nodes=1
#SBATCH --ntasks=1              
#SBATCH --gres=gpu:2             
#SBATCH --cpus-per-task=16       
#SBATCH --mem=160G               
#SBATCH --time=1-00:00:00        
#SBATCH --output=/raid/datasets/trossen/results/slurm/%x-%j.out
#SBATCH --error=/raid/datasets/trossen/results/slurm/%x-%j.out

# force the script to fail when using a command fails (-e) or when a variable is unset (-u)
set -eu
singularity exec --nv \
  -B /raid/datasets/trossen:/raid/datasets/trossen \
  -B /home/trossen/Desktop/models/trailab-isaac-gr00t:/home/trossen/Desktop/models/trailab-isaac-gr00t \
  --pwd /home/trossen/Desktop/models/trailab-isaac-gr00t \
  /home/trossen/Desktop/models/trailab-isaac-gr00t/singularity/gr00t.sif \
  ./finetune.sh