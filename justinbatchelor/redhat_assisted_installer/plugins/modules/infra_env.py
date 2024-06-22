#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule
from ..module_utils.api import *
from ..module_utils.tools import *
from ..module_utils.schema.infra_env import *
import os, json

__metaclass__ = type

DOCUMENTATION = r'''
---
module: infra_env
short_description: Manage infrastructure environments with Red Hat Assisted Installer
description:
  - Create, update, and delete infrastructure environments using the Red Hat Assisted Installer.
  - This module interacts with the Red Hat Assisted Installer API.
version_added: "1.0.0"
requirements:
  - requests==2.32.3
  - ansible==10.1.0
  - jmespath==1.0.1
author:
  - Justin Batchelor (@justinbatchelor)
options:
  additional_ntp_sources:
    description: List of additional NTP sources.
    required: false
    type: list
  additional_trust_bundle:
    description: Additional trust bundle in PEM format.
    required: false
    type: str
  cluster_id:
    description: Cluster ID associated with the infrastructure environment.
    required: false
    type: str
  cpu_architecture:
    description: CPU architecture of the infrastructure environment.
    required: false
    type: str
    choices: ['x86_64', 'aarch64', 'arm64', 'ppc64le', 's390x']
  ignition_config_override:
    description: Ignition config override.
    required: false
    type: str
  image_type:
    description: Type of image to create.
    required: false
    type: str
    choices: ["full-iso", "minimal-iso"]
  infra_env_id:
    description: ID of the infrastructure environment.
    required: false
    type: str
  kernel_arguments:
    description: Kernel arguments for the infrastructure environment.
    required: false
    type: list
    elements: dict
    suboptions:
      operation:
        description: Operation to perform on the kernel arguments.
        required: true
        type: str
        choices: ["append", "replace", "delete"]
      value:
        description: Kernel argument value.
        required: true
        type: str
  name:
    description: Name of the infrastructure environment.
    required: false
    type: str
  offline_token:
    description: Offline token for authentication.
    required: false
    type: str
    no_log: true
  openshift_version:
    description: OpenShift version to use.
    required: false
    type: str
  proxy:
    description: Proxy configuration.
    required: false
    type: dict
    suboptions:
      http_proxy:
        description: HTTP proxy URL.
        required: false
        type: str
      https_proxy:
        description: HTTPS proxy URL.
        required: false
        type: str
      no_proxy:
        description: Comma-separated list of hosts that do not use the proxy.
        required: false
        type: str
  pull_secret:
    description: Pull secret for accessing Red Hat's image registry.
    required: false
    type: str
    no_log: true
  ssh_authorized_key:
    description: SSH public key to authorize.
    required: false
    type: str
  state:
    description: Desired state of the infrastructure environment.
    required: true
    type: str
    choices: ['present', 'absent']
  static_network_config:
    description: Static network configuration.
    required: false
    type: list
    elements: dict
    suboptions:
      mac_interface_map:
        description: Mapping of MAC addresses to network interfaces.
        required: true
        type: list
        elements: dict
        suboptions:
          logical_nic_name:
            description: Logical name of the network interface.
            required: true
            type: str
          mac_address:
            description: MAC address of the network interface.
            required: true
            type: str
      network_yaml:
        description: Network configuration in YAML format.
        required: true
        type: str
'''

EXAMPLES = r'''
# Create a new infrastructure environment
- name: Create a new infrastructure environment
  infra_env:
    state: present
    name: "my-new-infra-env"
    openshift_version: "4.8"
    pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
    offline_token: <offline-token>
    ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
  register: result

# Delete an existing infrastructure environment by id
- name: Delete an infrastructure environment
  infra_env:
    state: absent
    infra_env_id: "your-infra-env-id"
  register: result

  
# Delete an existing infrastructure environment by id
- name: Delete an infrastructure environment
  infra_env:
    state: absent
    infra_env_id: "your-infra-env-id"
  register: result

'''

RETURN = r'''
infra_env:
  description: >
    Details of the created, updated, or deleted infrastructure environment.
  returned: always
  type: list
  elements: dict
  sample: 
    - id: "123"
      name: "my-infra-env"
      status: "active"
msg:
  description: >
    Message indicating the status of the operation.
  returned: always
  type: str
  sample: "Successfully created the infrastructure environment."
changed:
  description: >
    Indicates if any change was made.
  returned: always
  type: bool
  sample: true
'''

SUCCESS_GET_CODE = 200
SUCCESS_POST_CODE = SUCCESS_PATCH_CODE = 201
SUCCESS_DELETE_CODE = 204

def format_module_results(results: dict, msg: str = None, infra_env: list = None, changed: bool = None):
    if msg is not None:
        results['msg'] = msg

    if infra_env is not None:
        results['infra_env'] = infra_env

    if changed is not None:
        results['changed'] = changed

def run_module():
    module_args = dict(
        additional_ntp_sources=dict(type='list', required=False),
        additional_trust_bundle=dict(type='str', required=False),
        cluster_id=dict(type='str', required=False),
        cpu_architecture=dict(type='str', required=False, choices=['x86_64', 'aarch64', 'arm64', 'ppc64le', 's390x']),
        ignition_config_override=dict(type='str', required=False),
        image_type=dict(type='str', required=False, choices=["full-iso", "minimal-iso"]),
        infra_env_id=dict(type='str', required=False),
        kernel_arguments=dict(type='list', elements='dict', required=False, options=dict(
            operation=dict(type='str', required=True, choices=["append", "replace", "delete"]),
            value=dict(type='str', required=True),
        )),
        name=dict(type='str', required=False),
        offline_token=dict(type='str', required=False, no_log=True),
        openshift_version=dict(type='str', required=False),
        proxy=dict(type='dict', required=False, options=dict(
            http_proxy=dict(type='str', required=False),
            https_proxy=dict(type='str', required=False),
            no_proxy=dict(type='str', required=False),
        )),
        pull_secret=dict(type='str', required=False, no_log=True),
        ssh_authorized_key=dict(type='str', required=False),
        state=dict(type='str', required=True, choices=['present', 'absent']),
        static_network_config=dict(type='list', elements='dict', required=False, options=dict(
            mac_interface_map=dict(type='list', elements='dict', required=True, options=dict(
                logical_nic_name=dict(type='str', required=True),
                mac_address=dict(type='str', required=True)
            )),
            network_yaml=dict(type='str', required=True)
        )),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        infra_env=[],
        msg='',
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    ## First we need to check if the user provided an offline token 
    if module.params['offline_token'] is not None:
        os.environ["REDHAT_OFFLINE_TOKEN"] = module.params["offline_token"]

    ## Now we need to check if the user provided a pull secret
    if module.params['pull_secret'] is not None:
        os.environ["REDHAT_PULL_SECRET"] = module.params["pull_secret"]

    # get all infrastructure environment api response
    get_infras_resposne = get_infrastructure_environements()

    if get_infras_resposne.status_code != SUCCESS_GET_CODE:
        # update results with failed message from api
        format_module_results(results=result, 
                              msg=f"Failed to get infrastructure environments {get_infras_resposne.json()}",
                              changed=False,
                              infra_env=[]
                              )
        # fail module
        module.fail_json(**result)

    # check that a name or id was provided, fail if not
    if module.params['infra_env_id'] is None and module.params['name'] is None:
       format_module_results(results=result,
                      msg=f"You must specifiy either an infrastructure environment ID or a NAME when STATE == {module.params['state']}",
                      changed=False,
                      infra_env=[])
       module.fail_json(**result)


    filtered_response = jmespath_id_validator(module.params['infra_env_id'], get_infras_resposne.json()) if module.params['infra_env_id'] is not None else jmespath_name_validator(module.params['name'], get_infras_resposne.json())
        

    # user defined a state of present
    if module.params['state'] == "present":

        infra_env = InfraEnv(
            additional_ntp_sources=create_additional_ntp_sources_from_params(module.params['additional_ntp_sources']),
            additional_trust_bundle=module.params['additional_trust_bundle'],
            cluster_id=module.params['cluster_id'],
            cpu_architecture=module.params['cpu_architecture'],
            ignition_config_override=module.params['ignition_config_override'],
            image_type=module.params['image_type'],
            infra_env_id=module.params['infra_env_id'],
            kernel_arguments=create_kernel_arguments_from_module_params(module.params['kernel_arguments']),
            name=module.params['name'],
            openshift_version=module.params["openshift_version"],
            proxy=create_proxy_from_module_params(module.params['proxy']),
            ssh_authorized_key=module.params['ssh_authorized_key'],
            static_network_config=create_static_network_config_from_module_params(module.params['static_network_config']),
        )
        
        if len(filtered_response) == 0:
            create_infra_response = post_infrastructure_environment(infra_env=infra_env)
            if create_infra_response.status_code != SUCCESS_POST_CODE:
                format_module_results(results=result,
                                      msg=f'Failed to create the infrastructure environment: {create_infra_response.json()}',
                                      infra_env=[],
                                      changed=False,
                                      )
                module.fail_json(**result)
              
            format_module_results(results=result,
                                  msg=f"Successfully created the infrastructure environment: {create_infra_response.json()['id']}",
                                  changed=True,
                                  infra_env=[create_infra_response.json()],
                                  )
            module.exit_json(**result)

        elif len(filtered_response) == 1:
            modified_params = remove_matching_pairs(infra_env.create_params(), filtered_response[0])
            result['msg'] = modified_params
            patch_infra_response = patch_infrastructure_environment(filtered_response[0]['id'], modified_params)
            if patch_infra_response.status_code != SUCCESS_PATCH_CODE:
                format_module_results(results=result,
                                      msg=f'Failed to patch the infrastructure environment: {patch_infra_response.json()}',
                                      infra_env=[],
                                      changed=False,
                                      )
                module.fail_json(**result)
            format_module_results(results=result,
                                  msg=f"Successfully patched the infrastructure environment: {patch_infra_response.json()['id']}",
                                  changed=True,
                                  infra_env=[patch_infra_response.json()],
                                  )
            module.exit_json(**result)
            
        else:
           format_module_results(results=result,
                                 msg="Found more than one instance of the infrastructure environment you defined",
                                 changed=False,
                                 infra_env=[])
           module.fail_json(**result)
    # otherwise the state is absent
    else:     
        if len(filtered_response) == 0:
          format_module_results(results=result,
                                msg="Infrastructure environment not found.",
                                changed=False,
                                infra_env=[])
          module.exit_json(**result)

        elif len(filtered_response) == 1:
            if delete_infrastructure_environment(infra_env_id=filtered_response[0]['id']):
                format_module_results(results=result, 
                                      msg=result['msg'] + f"Successfully deleted infrastructure environment: {filtered_response[0]['id']}\n",
                                      changed=True,
                                      infra_env=result['infra_env'].append(filtered_response[0]),
                                      )
                module.exit_json(**result)
            else: 
                format_module_results(results=result, 
                                      msg=result['msg'] + f"Failed to delete infrastructure environment: {filtered_response[0]['id']}\n",
                                      changed=False,
                                      infra_env=result['infra_env'].append(filtered_response[0]),
                                      )
                module.fail_json(**result)
        else:
            # fail for one of two reasons listed in message
            format_module_results(results=result, 
                                  msg='We ran into a stange error. It seems you have multiple infrastructure environments with the same name, or our JMESpath expression is not working as expected.',
                                  changed=False,
                                  infra_env=[],
                                  )
            module.fail_json(**result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()