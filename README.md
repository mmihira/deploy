# deploy

EC2 boto deployment. This repo is designed to to be a submodule of your project. <br>
Setup a EC2 node configuration and provision your node. <br>
Applications can then be deployed using ansible.

## Requirements
* python3
* python3 virtualenv

## Installation & Usage

Install this repo as a submodule in your project
```bash
git submodule add https://github.com/mmihira/deploy deploy
```

Install python3 for your system as well as pip3 <br>
Install virtualenv
```bash
  pip3 install virtualenv
```

Edit ```.setup_config.json``` and configure it. For example
like below:

```json
{
  "project_prefix": "project",
  "project_dir_name": "project",
  "ec2_priv_key_name": "key",
  "path_to_priv_key_file": "/home/user/.ssh/project/key.pem",
  "path_to_aws_cred_file": "/home/user/.ssh/aws_creds.json",
  "path_to_ansible_vault_password_file": "/home/user/.ssh/project/avKey"
}
```

Setup the virutal environment
```bash
  ./deploy_setup.sh
```
This will generate a ``` config/config.sh``` file. <br>
Next sepcify your node configuration. A sample one is in ``` config/node_config.json ```
For example :

```json
{
  "nodes": {
    "app" : {
      "ami": "ami-96666ff5",
      "security_groups": ["ssh"],
      "type": "t2.micro",
      "tags": { "name": "app" },
      "attach_volume": true,
      "volume": "vol-02b6e03aa9a40d5f3",
      "volume_mount_point": "/dev/xvdb",
      "volume_mount_dir": "/data",
      "ansible_host_groups": [
        "docker",
        "global_env",
        "mount_vol"
      ],
      "env_injection": [
        "INST_NAME=app"
      ]
    }
  }
}
```

Next run the deployment

```bash
  ./full_deploy.sh
```

To come: configure ansible projects


