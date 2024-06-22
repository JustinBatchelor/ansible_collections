# justinbatchelor.redhat_assisted_installer.infra_env_info

Module to implement the GET operations for infrastructure environement objects documented by the Red Hat assisted installer

## Examples

```
---
- name: Retrieve information about all environments
  hosts: localhost
  tasks:
    - name: Get information about all environments
      justinbatchelor.redhat_assisted_installer.infra_env_info:
      register: all_env_info

    - name: Get information about a specific environment
      justinbatchelor.redhat_assisted_installer.infra_env_info:
        infra_env_id: "env123"
      register: env_info

    - name: Get information about all environments manually passing authentication parameters
      justinbatchelor.redhat_assisted_installer.infra_env_info:
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        offline_token: "{{ lookup('file', 'path/to/offline_token.txt') }}" 
      register: all_env_info

    - name: Get information about a specific environment manually passing authentication parameters
      justinbatchelor.redhat_assisted_installer.infra_env_info:
        infra_env_id: "env123"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        offline_token: "{{ lookup('file', 'path/to/offline_token.txt') }}" 
      register: env_info
```

## Parameters

    infra_env_id:
        description: ID of the infrastructure environment.
        required: false
        type: str

    offline_token:
        description: Offline token for authentication.
        type: str
        required: false
        no_log: true

    pull_secret:
        description: The pull secret obtained from Red Hat OpenShift Cluster Manager.
        type: str
        required: false
        no_log: true