#!/bin/bash
source config.sh

ansible_hosts="$PROJECT_PREFIX""_ANSIBLE_HOSTS"
ssh_config="$PROJECT_PREFIX""_SEVERS_SSH_CONFIG"
vault_key_file="$PROJECT_PREFIX""_ANSIBLE_VAULT_PASSWORD_FILE"
vault_file="$PROJECT_PREFIX""_ANSIBLE_SECRETS_FILE"
ansible_config="$PROJECT_PREFIX""_ANSIBLE_CONFIG"
export ANSIBLE_CONFIG=${!ansible_config}
node_config="$PROJECT_PREFIX""_BOTO_CONFIG_FILE"
deployed_node_config="$PROJECT_PREFIX""_BOTO_DEPLOYED_CONFIG_FILE"

# Create the instances
python3  ./boto/print_details.py
