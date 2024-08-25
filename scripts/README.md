# Introduction
***To run this scripts you need to install poetry***. Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.

## System requirements
1. Python 3.8+

## Installing poetry
1. Run `curl -sSL https://install.python-poetry.org | python3 -`
2. Copy `export PATH=$PATH:$HOME/.local/bin` into your $HOME/.profile file
3. Run `. $HOME/.profile` to apply your changes to yout current session

## Installing script dependencies
Before running any scripts it is necessary to execute `poetry install` first to download all dependencies

## Run scritps

### Scale Clients
`poetry run python scale_clients.py <file_name> <n_clients>`

Example of usage
- poetry run python scale_clients.py docker-compose-dev.yaml 5
- poetry run python scale_clients.py docker-compose-dev.yaml 2
