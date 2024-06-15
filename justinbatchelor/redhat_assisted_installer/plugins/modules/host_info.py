#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule
from redhat_assisted_installer import assisted_installer

__metaclass__ = type

DOCUMENTATION = r'''
---
module: host_info

short_description: Module to communicate with the red hat assisted installer to get information about all or specific openshift agents 

version_added: "1.0.0"

description: 

options:
    infra_env_id:
      description:
      - ID for the assisted installer managed infrastructure environment
      type: str
      default: None
      required: True

    host_id:
      description:
      - ID for the assisted installer managed host associated with the infra_env_id
      type: str
      default: None
      required: False

author:
    - Justin Batchelor (@justinbatchelor)
'''

EXAMPLES = r'''
- name: Task to use custom module to get all infra_env objects
    justinbatchelor.redhat_assisted_installer.infra_env_info:
    register: infra_envs

- debug:
    msg: "{{ infra_envs }}"

- name: Task to use custom module to get all hosts info from infra_env
    justinbatchelor.redhat_assisted_installer.host_info:
    infra_env_id: "{{ infra_envs['infra_env_info'][0]['id'] }}"
    register: hosts

- debug:
    msg: "{{ hosts }}"

- name: Task to use custom module to get specific host info 
    justinbatchelor.redhat_assisted_installer.host_info:
    infra_env_id: "{{ infra_envs['infra_env_info'][0]['id'] }}"
    host_id: "{{ hosts['host_info'][0]['id'] }}"
    register: host

- debug:
    msg: "{{ host['host_info'][0]['id'] }}"
'''

RETURN = r'''
result:
    changed: <bool>
    host_info: List<host>
'''


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        infra_env_id = dict(type='str', default=None, required=True),
        host_id = dict(type='str', default=None),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        host_info='',
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

    if module.params['host_id'] is None:
        result['host_info'] = installer.get_infrastructure_environement_hosts(infra_env_id=module.params['infra_env_id'])

    else:
        result['host_info'] = installer.get_infrastructure_environement_host(infra_env_id=module.params['infra_env_id'], host_id=module.params['host_id'])

    


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