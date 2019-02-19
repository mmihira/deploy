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
(source ./.VENV/bin/activate; pip3 install ansible)

python3 ./scripts/setup.py -config ./.setup_config.json
rm -rf .git

# Create the ansible vault file
source ./config/config.sh
vault_key_file="$PROJECT_PREFIX""_ANSIBLE_VAULT_PASSWORD_FILE"
(source ./.VENV/bin/activate; touch ./ansible/secrets/secrets.yml; ansible-vault encrypt ./ansible/secrets/secrets.yml --vault-password-file "${!vault_key_file}")

