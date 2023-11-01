#!/bin/bash

# Create the conda environment from the environment.yml file in the current directory
conda env create -f environment.yml

# Activate the new environment
conda activate open3d

# Register the environment as a Jupyter kernel
python -m ipykernel install --user --name $env_name

