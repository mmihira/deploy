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
  pip3 install virtualenv pip3
```


Setup the virutal environment
```bash
  ./deploy_setup.sh
```
You will need to provide the following in the interactive setup:

```bash
  project prefix       : Should be a captial alphabetic project identifier
  project dir name     : The root directory name of your project
  EC2 private key name : The ssh private key name you want to use to access your instances
  path to key file     : Absolute path to the private key file for ec2 ssh access
  amazon cred file     : Absolute path to the Amazon credential file. Must be a json file with keys access_key and secret_key
  ansible vault file   : Absolute path to ansible vault password file. Must be text with one line key entry
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


