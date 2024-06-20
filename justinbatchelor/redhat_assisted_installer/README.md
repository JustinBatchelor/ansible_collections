# Ansible Collection - justinbatchelor.redhat_assisted_installer

Ansible collection to interact with the Red Hat Assisted Installer API. 

## Requirements

### Python Packages

This collection makes use of the following python packages

- `requests==2.32.3`
- `ansible==10.1.0`
- `jmespath==1.0.1`

This repository provides a `requirements.txt` you can use to ensure all modules are installed in your environment. 

Run the following command 

    python -m pip install -r requirements.txt

## How To Use

### Install Collection

**Option 1**

You can install the collection by using the following command 

    ansible-galaxy collection install git+https://github.com/JustinBatchelor/ansible_collections.git#/justinbatchelor/redhat_assisted_installer

**Option 2**

This repo also provides a `requirements.yaml` file you can copy and then run the following command
        
    ansible-galaxy collection install -r requirements.yaml


### Modules Available

To learn more about how to use a specific module, please refer to the `docs/` folder for more detailed information on each module.

#### Info Modules

Implements GET API methods

- `justinbatchelor.redhat_assisted_installer.cluster_info`
- `justinbatchelor.redhat_assisted_installer.host_info`
- `justinbatchelor.redhat_assisted_installer.infra_env_info`


#### Create / Update / Delete

Implements the POST / PATCH / DELETE API methods

- `justinbatchelor.redhat_assisted_installer.cluster`
- `justinbatchelor.redhat_assisted_installer.infra_env`