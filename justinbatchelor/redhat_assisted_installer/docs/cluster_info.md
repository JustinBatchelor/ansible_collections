# justinbatchelor.redhat_assisted_installer.module 

Module to implement the GET operations for cluster objects documented by the [Red Hat Assisted Installer API](https://developers.redhat.com/api-catalog/api/assisted-install-service#content-operations)

## Examples

```
---
- name: Get information about a specific cluste
  hosts: localhost
  tasks:
    - name: Get information about all clusters
      justinbatchelor.redhat_assisted_installer.cluster_info:
      register: all_cluster_info

    - name: Get information about a specific cluster
      justinbatchelor.redhat_assisted_installer.cluster_info:
        cluster_id: "cluster123"
      register: cluster_info

    - name: Get information about all clusters manually passing authentication parameters
      justinbatchelor.redhat_assisted_installer.cluster_info:
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        offline_token: "{{ lookup('file', 'path/to/offline_token.txt') }}" 
      register: all_cluster_info

    - name: Get information about a specific cluster manually passing authentication parameters
      justinbatchelor.redhat_assisted_installer.cluster_info:
        cluster_id: "cluster-123"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        offline_token: "{{ lookup('file', 'path/to/offline_token.txt') }}" 
      register: cluster_info

```

## Parameters

    cluster_id:
        description: ID of the cluster.
        type: str
        required: false

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