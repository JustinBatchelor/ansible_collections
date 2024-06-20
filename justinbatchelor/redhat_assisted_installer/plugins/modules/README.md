# Modules

Various modules that implement the Red Hat Assisted Installer 

- [API | Docs](https://developers.redhat.com/api-catalog/api/assisted-install-service#content-operations) 
- [API | Service](https://api.openshift.com/?urls.primaryName=assisted-service%20service)

## Info Modules

### cluster_info

Cluster info is a module that seeks to implement the following endpoints from the Red Hat Assisted Installer

| Protocol | Endpoint | Query Parameters (implemeted) | Description | 
| -------- | -------- | ----------------------------- | ----------- |
| GET      | `/v2/clusters/` | [with_hosts, owner] | Retrieves the list of OpenShift clusters. |
| GET      | `/v2/clusters/{cluster_id}` | None | Retrieves the details of the OpenShift cluster. |


#### Arguments

| Name          | Description               | Type      | Default       | Choices               | Required | 
| ------------- | ------------------------- | --------- | ------------- | --------------------- | -------- |
| cluster_id    | Cluster ID for the assisted installer managed cluster |  str | None | any | False |  


#### Returns

A list of clusters defined by the [API schema cluster](https://developers.redhat.com/api-catalog/api/assisted-install-service#schema-cluster)

    result:
      changed: <bool>
      cluster_info: List<Cluster>
      count: <int>


#### Examples

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


### host_info

Cluster info is a module that seeks to implement the following endpoints from the Red Hat Assisted Installer

| Protocol | Endpoint | Query Parameters (implemeted) | Description | 
| -------- | -------- | ----------------------------- | ----------- |
| GET      | `/v2/infra-envs/{infra_env_id}/hosts` | None | Retrieves the list of OpenShift hosts that belong the infra-env. |
| GET      | `/v2/infra-envs/{infra_env_id}/hosts/{host_id}` | None | Retrieves the details of the OpenShift host. |


#### Arguments

| Name          | Description               | Type      | Default       | Choices               | Required | 
| ------------- | ------------------------- | --------- | ------------- | --------------------- | -------- |
| infra_env_id  | ID for the assisted installer managed infrastructure environment |  str | None | any | True |
| host_id       | ID for the openshift host | str | None | any | False

#### Returns

A list of hosts defined by the [API schema host](https://developers.redhat.com/api-catalog/api/assisted-install-service#schema-host)

    result:
      changed: <bool>
      hosts: List<host>


#### Examples
    # Use infra_env_info module to get a list of infra_envs
    - name: Task to get all infra_env objects associated with account
      justinbatchelor.redhat_assisted_installer.infra_env_info:
      register: infra_envs

    # Implements the /v2/infra-envs/{infra_env}/hosts endpoint
    - name: Task to get all hosts info from {{ infra_envs['infra_env_info'][0]['id'] }}
      justinbatchelor.redhat_assisted_installer.host_info:
        infra_env_id: "{{ infra_envs['infra_env_info'][0]['id'] }}"
      register: hosts

    - name: Task to use custom module to get specific host info 
      justinbatchelor.redhat_assisted_installer.host_info:
        infra_env_id: "{{ infra_envs['infra_env_info'][0]['id'] }}"
        host_id: "{{ hosts['host_info'][0]['id'] }}"
      register: host


### infra_env_info

Cluster info is a module that seeks to implement the following endpoints from the Red Hat Assisted Installer

| Protocol | Endpoint | Query Parameters (implemeted) | Description | 
| -------- | -------- | ----------------------------- | ----------- |
| GET      | `/v2/infra-envs/` | None | Retrieves the list of infra-envs. |
| GET      | `/v2/infra-envs/{infra_env_id}` | None | Retrieves the details of the infra-env. |


#### Arguments

| Name          | Description               | Type      | Default       | Choices               | Required | 
| ------------- | ------------------------- | --------- | ------------- | --------------------- | -------- |
| infra_env_id  | ID for the assisted installer managed infrastructure environment |  str | None | any | False |


#### Returns

A list of `infra_env` defined by the [API schema infra_env](https://developers.redhat.com/api-catalog/api/assisted-install-service#schema-infra-env)

    result:
      changed: <bool>
      hosts: List<infra_env>
