# Ansible Collection - justinbatchelor.redhat_assisted_installer

Ansible collection to interact with the Red Hat Assisted Installer API. 

## Requirements

### Python Packages

A list of required packages can be found in the `requirements.txt` file. You can quickly install all files running the following command

    python -m pip install -r requirments.txt


### Environment Variables

You must have the following environment variables set in before you can successfully use the collection. Some modules and functions in this collection may not require the use of the `REDHAT_PULL_SECRET`. However, all modules will require the `REDHAT_OFFLINE_TOKEN`

- `REDHAT_PULL_SECRET`: The pull secret associated with your RedHat Hybrid Cloud account

- `REDHAT_OFFLINE_TOKEN`: The offline token associated with your RedHat Hybrid Cloud account


## How To Use

### Install Collection

**Option 1**

You can install the collection by using the following command 

    ansible-galaxy collection install git+https://github.com/JustinBatchelor/ansible_collections.git#/justinbatchelor/redhat_assisted_installer

**Option 2**

This repo also provides a `requirements.yaml` file you can copy and then run the following command
        
    ansible-galaxy collection install -r requirements.yaml


### Modules Available

To learn more about how to use a specific module, please refer to `./plugins/modules/README.md` for more detailed information.

#### Info Modules

Implements GET API methods

- `justinbatchelor.redhat_assisted_installer.cluster_info`
- `justinbatchelor.redhat_assisted_installer.host_info`
- `justinbatchelor.redhat_assisted_installer.infra_env_info`

#### Create / Update / Delete

Implements the POST / PATCH / DELETE API methods

- `justinbatchelor.redhat_assisted_installer.cluster`