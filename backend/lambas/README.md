# Lambdas

## Python env setup

To setup the local python environment locally you need to install python using pyenv and the following pip requirements. You can do this by following the commands below.

1. `eval "$(pyenv init -)"`
1. `pyenv install` (optional - only if you already have the python version installed)
1. `pyenv exec python -m venv .venv` (optional - if the venv already exists)
1. `source .venv/bin/activate`
1. `pip3 install -r requirements.txt` (optional - if you have already installed the requirements)
