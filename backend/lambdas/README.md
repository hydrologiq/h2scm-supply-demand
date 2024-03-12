# Lambdas

We use [Poetry](https://python-poetry.org/) to manage lambda bundles and dependencies. Python version is `3.12`.

## Python setup

To be able to run the lambdas locally we need to install python and the `poetry` package locally and to do this we use [pyenv](https://github.com/pyenv/pyenv).

1. `brew install pyenv` (optional if already installed)
1. `eval "$(pyenv init -)"` (optional if already installed)
1. `pyenv install` (optional if already installed)
1. `pyenv exec python -m venv .venv` (optional if already installed)
1. `source .venv/bin/activate`
1. `pip3 install -r requirements.txt` (optional if already installed)
