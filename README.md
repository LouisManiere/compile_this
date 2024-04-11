# compile_this

Compile time series dataset

## Baro, Diver, Solinst sensors

Baro = compile_this_solinst_baro.py
F, L, M, N, RAmont, RAval = compile_this_solinst.py
A, B, C, D, E, G, H, I, J, ZGraviere = compile_this_solinst_baro.py

## Installation

Create a Python 3 virtual environment and install dependencies.

Windows

- Install Python with environment PATH
- Install Git for windows
- Open a command prompt

``` python
# go to the working folder you want to download the mapdo application
cd Path/to/my/folder
# copy mapdo repository with git
git clone https://github.com/LouisManiere/compile_this.git
# create a new virtual environnement in python 3
python -m venv env --prompt compile_this
# activate your new environment
# Windows
.\env\Scripts\activate
# Linux
source ./env/bin/activate
# update pip
python -m pip install -U pip
# install all others dependencies
pip install -r requirements.txt
```