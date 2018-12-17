#!/bin/bash

if python3 -c 'import pkgutil; print(1 if pkgutil.find_loader("virtualenv") else 0)'; then
  echo "Using virtualenv"
else
  echo "Please install virutalenv for python3"
  exit 0
fi

python3 -m virtualenv ./.VENV
(source ./.VENV/bin/activate; pip3 install paramiko)
(source ./.VENV/bin/activate; pip3 install boto)
(source ./.VENV/bin/activate; pip3 install configparser)
