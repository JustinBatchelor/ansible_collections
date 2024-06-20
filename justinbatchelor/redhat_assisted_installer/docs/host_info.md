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
