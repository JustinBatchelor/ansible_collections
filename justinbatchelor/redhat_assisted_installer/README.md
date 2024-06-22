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

### Authentication

**Environment Variables**

- `REDHAT_PULL_SECRET`: The pull secret associated with your RedHat Hybrid Cloud account

- `REDHAT_OFFLINE_TOKEN`: The offline token associated with your RedHat Hybrid Cloud account

This module uses two environment variables to authenticate with the API. By default this collection will look to use the environment variables listed above in your execution environment in order to authenticate with the API. Optionally, you may pass the `pull-secret` as a json formatted string, and `offline-token` as a string to each task that invokes a module in this collection. 

**Example**

```
- name: Create a basic infrastructure environment
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      infra_env:
        state: present
        name: "basic-infra-env"
        openshift_version: "4.8"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        offline_token: "{{ lookup('file', 'path/to/token.txt') }}"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
      register: result
```


**_You can find these credentials by navigating to https://console.redhat.com/openshift/overview. In the side panel navigate to `Downloads`, and at the bottom of the page you should see the pull secret and token_**

![](https://raw.githubusercontent.com/JustinBatchelor/red-hat-assisted-installer/c33b2eb3570ab498e85944035e71156ee192a816/docs/downloads_console.png)


## How To Use

### Install Collection

**Option 1**

You can install the collection by using the following command 

    ansible-galaxy collection install git+https://github.com/JustinBatchelor/ansible_collections.git#/justinbatchelor/redhat_assisted_installer

**Option 2**

This repo also provides a `requirements.yaml` file you can copy and then run the following command
        
    ansible-galaxy collection install -r requirements.yaml


### Modules Available

To learn more about how to use a specific module, please refer to the `docs/` folder for more detailed information on each module and it's invocation.

#### Info Modules

Implements GET API methods

- `justinbatchelor.redhat_assisted_installer.cluster_info`
- `justinbatchelor.redhat_assisted_installer.host_info`
- `justinbatchelor.redhat_assisted_installer.infra_env_info`


#### Create / Update / Delete

Implements the POST / PATCH / DELETE API methods

- `justinbatchelor.redhat_assisted_installer.cluster`
- `justinbatchelor.redhat_assisted_installer.infra_env`


### Use Case Example 

**Create a Highly Available OpenShift Cluster**

The result of the playbook will create (or patch) a cluster and infrastructure environment in your hybrid cloud Red Hat account. Thus allowing you access to an `iso` file that you can use to boot machines backing your openshift cluster. You can access this iso file by navigating to your hybrid cloud account and click on the newly created cluster, then click the button `Add hosts` to generate your discovery iso. Optionally, the last debug task will contain a json response with a key named "download_url" containing the url you use to obtain your `iso` file.

```
- name: Manage OpenShift Cluster
  hosts: localhost
  tasks:
    - name: Task to set facts to create HA OpenShift cluster
      ansible.builtin.set_fact:
        cluster_name: "ansible-testing-cluster"
        infra_name: "ansible-testing-infra"
        base_dns_domain: "batchelor.live"
        openshift_version: "4.15"
        cpu_architecture: "x86_64"
        high_availability_mode: "No"
        cluster_tags: "sno,openshift"
        platform_type: "baremetal"
        image_type: "minimal-iso"

    - name: Create a HA OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        name: "{{ cluster_name }}"
        base_dns_domain: "{{ base_dns_domain }}"
        openshift_version: "{{ openshift_version }}"
        cpu_architecture: "{{ cpu_architecture }}"
        high_availability_mode: "{{ high_availability_mode }}"
        platform:
          type: "{{ platform_type }}"
        tags: "{{ cluster_tags }}"
        ssh_public_key: "{{ lookup('file', '/home/jbatchel/.ssh/id_rsa.pub') }}"
        state: "present"
      register: cluster

    - name: Task to debug cluster
      ansible.builtin.debug:
        msg: "{{ cluster['cluster'] }}"

    - name: Create an infrastructure environment associated with cluster
      justinbatchelor.redhat_assisted_installer.infra_env:
        name: "{{ infra_name }}"
        state: "present"
        cluster_id: "{{ cluster['cluster'][0]['id'] }}"
        cpu_architecture: "{{ cpu_architecture }}"
        openshift_version: "{{ openshift_version }}"
        image_type: "{{ image_type }}"
      register: infra_env

    - name: Task to debug infrastructure environment
      ansible.builtin.debug:
        msg: "{{ infra_env }}"
```


**Create a Single Node OpenShift Cluster**

The result of the playbook will create (or patch) a cluster and infrastructure environment in your hybrid cloud Red Hat account. Thus allowing you access to an `iso` file that you can use to boot machines backing your openshift cluster. You can access this iso file by navigating to your hybrid cloud account and click on the newly created cluster, then click the button `Add hosts` to generate your discovery iso. Optionally, the last debug task will contain a json response with a key named "download_url" containing the url you use to obtain your `iso` file.

```
- name: Manage OpenShift Cluster
  hosts: localhost
  tasks:
    - name: Task to set facts to create Single Node OpenShift cluster
      ansible.builtin.set_fact:
        cluster_name: "ansible-testing-cluster"
        infra_name: "ansible-testing-infra"
        base_dns_domain: "batchelor.live"
        openshift_version: "4.15"
        cpu_architecture: "x86_64"
        high_availability_mode: "No"
        cluster_tags: "sno,openshift"
        platform_type: "baremetal"
        image_type: "minimal-iso"

    - name: Create a Single Node OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        name: "{{ cluster_name }}"
        base_dns_domain: "{{ base_dns_domain }}"
        openshift_version: "{{ openshift_version }}"
        cpu_architecture: "{{ cpu_architecture }}"
        high_availability_mode: "{{ high_availability_mode }}"
        platform:
          type: "{{ platform_type }}"
        tags: "{{ cluster_tags }}"
        ssh_public_key: "{{ lookup('file', '/home/jbatchel/.ssh/id_rsa.pub') }}"
        state: "present"
      register: cluster

    - name: Task to debug cluster
      ansible.builtin.debug:
        msg: "{{ cluster['cluster'] }}"

    - name: Create an infrastructure environment associated with cluster
      justinbatchelor.redhat_assisted_installer.infra_env:
        name: "{{ infra_name }}"
        state: "present"
        cluster_id: "{{ cluster['cluster'][0]['id'] }}"
        cpu_architecture: "{{ cpu_architecture }}"
        openshift_version: "{{ openshift_version }}"
        image_type: "{{ image_type }}"
      register: infra_env

    - name: Task to debug infrastructure environment
      ansible.builtin.debug:
        msg: "{{ infra_env }}"
```