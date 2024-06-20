#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule
from ..module_utils.api import *
from ..module_utils.tools import *
from ..module_utils.schema.infra_env import *
import jmespath, os




__metaclass__ = type

DOCUMENTATION = r'''
---
module: infra_env
short_description: Manage infrastructure environments
version_added: "1.0.0"
description: >
  This module allows managing infrastructure environments using the Red Hat Assisted Installer API.
options:
  infra_env_id:
    description: ID for the assisted installer managed infrastructure environment.
    type: str
    required: false
  name:
    description: Name of the infrastructure environment.
    type: str
    required: false
  openshift_version:
    description: Version of OpenShift to install.
    type: str
    required: false
  pull_secret:
    description: Pull secret for accessing OpenShift images.
    type: str
    required: false
    no_log: true
  ssh_public_key:
    description: SSH public key for accessing nodes.
    type: str
    required: false
  proxy:
    description: Proxy settings for the infrastructure environment.
    type: dict
    required: false
    suboptions:
      http_proxy:
        description: HTTP proxy URL.
        type: str
        required: false
      https_proxy:
        description: HTTPS proxy URL.
        type: str
        required: false
      no_proxy:
        description: List of URLs that should not be proxied.
        type: str
        required: false
  state:
    description: Desired state of the infrastructure environment.
    type: str
    required: true
    choices: ['present', 'absent']

requirements:
  - requests==2.32.3
  - ansible==10.1.0
  - jmespath==1.0.1

author:
  - Justin Batchelor (@justinbatchelor)
'''

EXAMPLES = r'''
# Create a new infrastructure environment
- name: Create a new infrastructure environment
  justinbatchelor.redhat_assisted_installer.infra_env:
    state: present
    name: "my-new-infra-env"
    openshift_version: "4.8"
    pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
    ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
  register: result

- debug:
    msg: "{{ result }}"

# Delete an existing infrastructure environment
- name: Delete an infrastructure environment
  justinbatchelor.redhat_assisted_installer.infra_env:
    state: absent
    infra_env_id: "your-infra-env-id"
  register: result

- debug:
    msg: "{{ result }}"
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
'''


def run_module():
    module_args = dict(
        additional_ntp_source=dict(type='list', required=False),
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
        infra_env='',
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

    
    infra_env = InfraEnv(
        additional_ntp_sources=create_additional_ntp_sources_from_params(module.params['additional_ntp_source']),
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

    # If user defined a present infra_env
    if module.params['state'] == 'present':
        # If user did not specifiy either infra_env_id or name we need to fail, as a name is required to create an infra_env
        if module.params["infra_env_id"] is None and module.params["name"] is None:
            # fail message
            result['msg'] = 'When state is present you must specifiy at least a name. If a infra_env does not already exist with that name, this module will create one. Please update the corresponding args and try to rerun.'
            module.fail_json(**result)
        # user specified either name or infra_env_id
        else:
            # user specified infra_env_id we are patching an existing infra_env
            if module.params['infra_env_id'] is not None:
                # try / except block for the infra_env patch request
                try:
                    patch_infra_response = patch_infrastructure_environment(infra_env=infra_env)
                    patch_infra_response.raise_for_status()
                    result['changed'] = True
                    result['msg'] = f"Successfully patched the infrastructure environment: {patch_infra_response.json()['id']}"
                    result['infra_env'] = [patch_infra_response.json()]               
                    module.exit_json(**result)
                except Exception as e:
                    result['changed'] = False
                    result['msg'] = f"Failed to patch infra_env: {module.params['infra_env_id']}"
                    module.fail_json(**result)  
            # user specified infra_env name, currently we don't know if we are creating or patching
            else:
                try:
                    get_infra_response = get_infrastructure_environements()
                    get_infra_response.raise_for_status()
                except Exception as e:
                    result['changed'] = False
                    result['msg'] = f"Failed to get infrastructure environments {get_infra_response.json()}"
                    module.fail_json(**result) 
                else:
                    # JMESPath expression to filter objects by name
                    expression = f"[?name=='{module.params["name"]}']"

                    # Search the API response using the JMESPath expression
                    filtered_response = jmespath.search(expression, get_infra_response.json())
                    
                    # all cluster names should be unique, fail if filtered response is greater than 1
                    if len(filtered_response) > 1:
                        # fail for one of two reasons listed in message
                        result['msg'] = 'We ran into a stange error. It seems you have multiple infrastructure environments with the same name, or our JMESpath expression is not working as expected.'
                        module.fail_json(**result)
                    # now we know we are patching an existing cluster
                    if len(filtered_response) == 1:
                        try:
                            patch_infra_response = patch_infrastructure_environment(infra_env)
                            patch_infra_response.raise_for_status()
                            result['changed'] = True
                            result['msg'] = f"Successfully patched the infrastructure environment: {patch_infra_response.json()['id']}"
                            result['infra_env'] = [patch_infra_response.json()]               
                            module.exit_json(**result)
                        except Exception as e:
                            result['changed'] = False
                            result['msg'] = f'Failed to patch the infrastructure environment: {patch_infra_response.json()}'
                            module.fail_json(**result)
                    # no infra_env matching that name provided
                    # we are creating an infra env
                    if len(filtered_response) == 0:
                        try: 
                            create_infra_response = post_infrastructure_environment(infra_env)
                            create_infra_response.raise_for_status()
                            result['changed'] = True
                            result['msg'] = f"Successfully created the infrastructure environment: {create_infra_response.json()['id']}"
                            result['infra_env'] = [create_infra_response.json()] 
                            module.exit_json(**result)
                        except Exception as e:
                            result['changed'] = False
                            result['msg'] = f'Failed to create the infrastructure environment: {create_infra_response.json()}'
                            module.fail_json(**result)
    # otherwise state == absent and we need to delete the cluster      
    else:
        # we need to know which infra_env to delete
        if module.params['infra_env_id'] is None and module.params['name'] is None:
            # fail because both params are not defined
            result['msg'] = 'You must provide either the name, infra_env_id, or both to delete a cluster. Please update the corresponding args and try to rerun.'
            module.fail_json( **result)
        # user supplied either the name or infra_env_id or both
        else:
            # if user supplied infra_env_id
            if module.params['infra_env_id'] is not None:
                # if delete requests returns true
                if delete_infrastructure_environment(infra_env_id=module.params['infra_env_id']):
                    result['changed'] = True
                    result['msg'] = f"Successfully deleted infra_env: {module.params['infra_env_id']}"
                    module.exit_json(**result)
                # otherwise the delete request failed
                else:
                    result['changed'] = False
                    result['msg'] = f"Failed to delete infra_env: {module.params['infra_env_id']}"
                    module.fail_json(**result)                    

            # otherwise the user supplied the name of infra_env
            else:
                # try / except block for the infra_env get request
                try:
                    infra_env_response = get_infrastructure_environements()
                    infra_env_response.raise_for_status()
                except Exception as e:
                    result['changed'] = False
                    result['msg'] = f"Failed to get infrastructure environments {infra_env_response.json()}"
                    module.fail_json(**result) 
                # if infra_env_response.raise_for_status() didn't error
                else:
                    # JMESPath expression to filter objects by name
                    expression = f"[?name=='{module.params["name"]}']"

                    # Search the API response using the JMESPath expression
                    filtered_response = jmespath.search(expression, infra_env_response.json())
                    # all infra names should be unique, fail if filtered response is greater than 1
                    if len(filtered_response) > 1:
                        # fail for one of two reasons listed in message
                        result['msg'] = 'We ran into a stange error. It seems you have multiple infrastructure environments with the same name, or our JMESpath expression is not working as expected.'
                        module.fail_json(**result)
                    # now we know we are patching an existing infra
                    if len(filtered_response) == 1:
                        if delete_infrastructure_environment(infra_env_id=filtered_response[0]['id']):
                            result['changed'] = True
                            result['msg'] = f"Successfully deleted infra_env: {filtered_response[0]['id']}"
                            module.exit_json(**result)
                        else:
                            result['changed'] = False
                            result['msg'] = f"Failed to delete infra_env: {module.params['infra_env_id']}"
                            module.fail_json(**result)                 

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()