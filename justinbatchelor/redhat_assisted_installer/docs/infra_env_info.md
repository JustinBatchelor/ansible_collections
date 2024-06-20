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
