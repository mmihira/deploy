#!python3
from pathlib import Path
import json
import os
import stat
import argparse

parser = argparse.ArgumentParser(description='Ec2 deployment')
parser.add_argument(
    '-config',
    type=str,
    default='setup_config.json',
    help='Setup config file path'
)

args = parser.parse_args()
f = open(args.config, 'r')
config = json.loads(f.read())

project_prefix = config['project_prefix']
project_dir_name = config['project_dir_name']
ec2_priv_key_name = config['ec2_priv_key_name']
path_to_priv_key_file = config['path_to_priv_key_file']
path_to_aws_cred_file = config['path_to_aws_cred_file']
path_to_ansible_vault_password_file = config['path_to_ansible_vault_password_file']

print("\n\nConfirm the following: ")
print('{:40}: {:}'.format("Project prefix", project_prefix))
print('{:40}: {:}'.format("Project dir", project_dir_name))
print('{:40}: {:}'.format("EC2 private key", ec2_priv_key_name))
print('{:40}: {:}'.format("EC2 private key path", path_to_priv_key_file))
print('{:40}: {:}'.format("AWS cred file path", path_to_aws_cred_file))
print('{:40}: {:}'.format("Ansible vault password file path", path_to_ansible_vault_password_file))

proceed = input("\nProceed (y/n) : ")
if proceed != 'y':
    print("Exiting..")
    exit(0)

WRITE_FILE_PATH = './config/config.sh'

f = open(WRITE_FILE_PATH, 'w')
f.write('#!/bin/bash\n')
f.write('\n####################################################################')
f.write('\n# Change this to the parent directory of the git repo')
f.write('\nexport PARENT_DIRECTORY_OF_REPO="/home/mihira/c"')
f.write('\nexport PARENT_DIRECTORY_OF_REPO="$PARENT_DIRECTORY_OF_REPO"')
f.write('\nexport PROJECT_PREFIX="{:}"'.format(project_prefix))
f.write('\nexport EC2_PROVIDER="AWS"')
f.write('\n####################################################################\n')
f.write('\n####################################################################')
f.write('\n# Do not modify these variables')
f.write('\nexport {:}_SEVERS_SSH_CONFIG="$PARENT_DIRECTORY_OF_REPO/{:}/deploy/ansible/ssh_config"'.format(project_prefix, project_dir_name))
f.write('\nexport {:}_ANSIBLE_HOSTS="$PARENT_DIRECTORY_OF_REPO/{:}/deploy/ansible/hosts"'.format(project_prefix, project_dir_name))
f.write('\nexport {:}_ANSIBLE_CONFIG="$PARENT_DIRECTORY_OF_REPO/{:}/deploy/ansible/ansible.cfg"'.format(project_prefix, project_dir_name))
f.write('\nexport {:}_ANSIBLE_SECRETS_FILE="$PARENT_DIRECTORY_OF_REPO/{:}/deploy/ansible/secrets/secrets.yml"'.format(project_prefix, project_dir_name))
f.write('\nexport {:}_ANSIBLE_DIR="$PARENT_DIRECTORY_OF_REPO/{:}/deploy/ansible"'.format(project_prefix, project_dir_name))
f.write('\nexport {:}_BOTO_CONFIG_FILE="$PARENT_DIRECTORY_OF_REPO/{:}/deploy/config/node_config.json"'.format(project_prefix, project_dir_name))
f.write('\nexport {:}_BOTO_DEPLOYED_CONFIG_FILE="$PARENT_DIRECTORY_OF_REPO/{:}/deploy/config/deployed_config.json"'.format(project_prefix, project_dir_name))
f.write('\n####################################################################\n')
f.write('\n####################################################################')
f.write('\n# These env variables can be set')
f.write('\n# Location of the private key to login to the nectar servers')
f.write('\nexport {:}_PRIVATE_KEY_FILE="{:}"'.format(project_prefix, path_to_priv_key_file))
f.write('\n# The name given to the private key pair on nectar')
f.write('\nexport {:}_KEY_PAIR_NAME="{:}"'.format(project_prefix, ec2_priv_key_name))
f.write('\n# Location of AWS account credentials')
f.write('\nexport {:}_AWS_KEY_FILE="{:}"'.format(project_prefix, path_to_aws_cred_file))
f.write('\n# Location of ansible vault password file')
f.write('\nexport {:}_ANSIBLE_VAULT_PASSWORD_FILE="{:}"'.format(project_prefix, path_to_ansible_vault_password_file))
f.write('\n####################################################################')
f.close()

st = os.stat(WRITE_FILE_PATH)
os.chmod(WRITE_FILE_PATH, st.st_mode | stat.S_IEXEC)
