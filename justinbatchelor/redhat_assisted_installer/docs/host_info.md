# justinbatchelor.redhat_assisted_installer.host_info


## Example

```
---
- name: Retrieve information for all hosts in the specified infrastructure environment
  hosts: localhost
  gather_facts: no
  tasks:
    - name: Get all hosts info from infra_env
      justinbatchelor.redhat_assisted_installer.host_info:
        infra_env_id: "your_infra_env_id"
      register: hosts

    - name: Get specific host info
      justinbatchelor.redhat_assisted_installer.host_info:
        infra_env_id: "your_infra_env_id"
        host_id: "your_host_id"
      register: host

    - name: Get all hosts info from infra_env using offline token and pull secret
      justinbatchelor.redhat_assisted_installer.host_info:
        infra_env_id: "your_infra_env_id"
        offline_token: "your_offline_token"
        pull_secret: "your_pull_secret"
      register: hosts

    - name: Get specific host info using offline token and pull secret
      justinbatchelor.redhat_assisted_installer.host_info:
        infra_env_id: "your_infra_env_id"
        host_id: "your_host_id"
        offline_token: "your_offline_token"
        pull_secret: "your_pull_secret"
      register: host

```

## Parameters

    infra_env_id:
        description:
        - The ID of the infrastructure environment managed by the assisted installer.
        type: str
        required: true
    host_id:
        description:
        - The ID of the host managed by the assisted installer within the specified infrastructure environment.
        type: str
        required: false
    offline_token:
        description:
        - Offline token for authentication with the Red Hat Assisted Installer API.
        type: str
        required: false
        no_log: true
    pull_secret:
        description:
        - Pull secret for authentication with the Red Hat Assisted Installer API.
        type: str
        required: false
        no_log: true
