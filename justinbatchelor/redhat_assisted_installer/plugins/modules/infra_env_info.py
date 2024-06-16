#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule
from redhat_assisted_installer import assisted_installer
from requests.exceptions import HTTPError

__metaclass__ = type

DOCUMENTATION = r'''
---
module: infra_env_info

short_description: Module to communicatee with the red hat assisted installer to get information about all or specific infrastrucuture environments

version_added: "1.0.0"

description: Module that implements the 'redhat-assisted-installer' python package to provide an easier way to communicate with the red hat assisted installer api

options:
    infra_env_id:
      description:
      - ID for the assisted installer managed infrastructure environment
      type: str
      default: None
      required: False

author:
    - Justin Batchelor (@justinbatchelor)
'''

EXAMPLES = r'''
- name: Task to get all infra_env objects
    justinbatchelor.redhat_assisted_installer.infra_env_info:
    register: infra_envs



- name: Task to get a specific infra_env
    justinbatchelor.redhat_assisted_installer.infra_env_info:
        infra_env_id: "2c478929-bdec-4c02-9bcf-xxxxxxxxxxxx"
    register: hosts
'''

RETURN = r'''

result:
    changed: <bool>
    infra_env_info: List<infra_env>

'''




def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        infra_env_id = dict(type='str', default=None),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        infra_env_info='',
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)


    installer = assisted_installer.assisted_installer()

    if module.params['infra_env_id'] is None:
        result['infra_env_info'] = installer.get_infrastructure_environements()
    else:
        result['infra_env_info'] = installer.get_infrastructure_environements(infra_env_id=module.params['infra_env_id'])
    


    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # if module.params['name'] == 'fail me':
    #     module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()