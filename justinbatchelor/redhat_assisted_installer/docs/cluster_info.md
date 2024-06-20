Cluster info is a module that seeks to implement the following endpoints from the Red Hat Assisted Installer

| Protocol | Endpoint | Query Parameters (implemeted) | Description | 
| -------- | -------- | ----------------------------- | ----------- |
| GET      | `/v2/clusters/` | [with_hosts, owner] | Retrieves the list of OpenShift clusters. |
| GET      | `/v2/clusters/{cluster_id}` | None | Retrieves the details of the OpenShift cluster. |


## Arguments

| Name          | Description               | Type      | Default       | Choices               | Required | 
| ------------- | ------------------------- | --------- | ------------- | --------------------- | -------- |
| cluster_id    | Cluster ID for the assisted installer managed cluster |  str | None | any | False |  


## Returns

A list of clusters defined by the [API schema cluster](https://developers.redhat.com/api-catalog/api/assisted-install-service#schema-cluster)

    result:
      changed: <bool>
      cluster_info: List<Cluster>
      count: <int>


## Examples

    # Implements the /v2/clusters/ endpoint with default query parameters and returns a list of all clusters
    - name: Task to use custom module with no arguments
      justinbatchelor.redhat_assisted_installer.cluster_info:
      register: all_cluster_info

    - debug:
        msg: "{{ all_cluster_info }}"


    # Implements the /v2/clusters/{cluster_id} endpoint and returns a list containing that cluster if it exists
    - name: Task to use custom module with argument
      justinbatchelor.redhat_assisted_installer.cluster_info:
        cluster_id: '{{ all_cluster_info["cluster_info"][0]["id"] }}'
      register: cluster_info

    - debug:
        msg: "{{ cluster_info['cluster_info'][0] }}"