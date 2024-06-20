#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.api import *
from ..module_utils.tools import *

__metaclass__ = type

DOCUMENTATION = r'''
---
module: host_info
short_description: Communicate with the Red Hat Assisted Installer to get information about all or specific OpenShift agents
version_added: "1.0.0"
description: >
  This module allows you to retrieve information about OpenShift agents from the Red Hat Assisted Installer,
  either for all hosts within an infrastructure environment or for a specific host.
options:
  infra_env_id:
    description:
      - ID for the assisted installer managed infrastructure environment.
    type: str
    required: true
  host_id:
    description:
      - ID for the assisted installer managed host associated with the infra_env_id.
    type: str
    required: false
author:
  - Justin Batchelor (@justinbatchelor)
'''

EXAMPLES = r'''
- name: Get all hosts info from infra_env
  justinbatchelor.redhat_assisted_installer.host_info:
    infra_env_id: "your_infra_env_id"
  register: hosts

- debug:
    msg: "{{ hosts }}"

- name: Get specific host info
  justinbatchelor.redhat_assisted_installer.host_info:
    infra_env_id: "your_infra_env_id"
    host_id: "your_host_id"
  register: host

- debug:
    msg: "{{ host }}"
'''

RETURN = r'''
host_info:
  description: >
    List of host information retrieved from the Red Hat Assisted Installer.
  returned: always
  type: list
  elements: dict
  sample: 
    - id: "123"
      name: "host1"
      status: "active"
count:
  description: >
    The number of hosts returned.
  returned: always
  type: int
  sample: 1
msg:
  description: >
    Message indicating the status of the operation.
  returned: always
  type: str
  sample: "Success"
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
        count="",
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

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)


    try:
        api_response = None
        if module.params['host_id'] is None:
            api_response = get_infrastructure_environement_hosts(infra_env_id=module.params['infra_env_id'])
        else:
            api_response = get_infrastructure_environement_host(infra_env_id=module.params['infra_env_id'], host_id=module.params['host_id'])
        api_response.raise_for_status()
        result['host_info'] = [api_response.json()] if isinstance(api_response.json, dict) else api_response.json()
        result['count'] = len([api_response.json()]) if isinstance(api_response.json(), dict) else len(api_response.json())
        result['msg'] = "Success"
        module.exit_json(**result) 

    except Exception as e:
        result['changed'] = False
        result['msg'] = f"Failed: {e}"
        module.fail_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()