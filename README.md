# NAMD to Desmond DMS Conversion

This repository contains a Python script for converting a NAMD molecular
dynamics system into a Desmond `.dms` file.

## Files

- `convertNAMDtoDMS_Maryam.py` — Python script used for the conversion.
- `environment.yml` — Conda environment specification required to run the script.
- `README.md` — Documentation and instructions.

## Requirements

The conversion requires:

- Conda
- Python 3.10
- `vmd-python`

The required packages are listed in `environment.yml`.

## Environment Setup

Create the Conda environment using:

```bash
conda env create -f environment.yml
Activate the environment:

conda activate vmd_env_local
Input Files

The conversion requires:

system.psf — NAMD structure file
system.coor — NAMD coordinate file
system.vel — NAMD velocity file
system.xsc — NAMD extended system configuration file
Usage

After activating the Conda environment, run:

python convertNAMDtoDMS_Maryam.py \
    -p system.psf \
    -c system.coor \
    -v system.vel \
    -x system.xsc \
    -o out.dms
Output

The script generates:

out.dms
