#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule
from redhat_assisted_installer import assisted_installer
import json
__metaclass__ = type

DOCUMENTATION = r'''
---
module: cluster_info

short_description: 

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: 

options:
    cluster_id:
      description:
      - Cluster ID for the assisted installer managed cluster
      type: str
      default: None
      required: False

author:
    - Justin Batchelor (@justinbatchelor)
'''

EXAMPLES = r'''
- name: Task to use custom module with no arguments
    justinbatchelor.redhat_assisted_installer.cluster_info:
    register: all_cluster_info

- debug:
    msg: "{{ all_cluster_info }}"

- debug:
    msg: "{{ all_cluster_info['cluster_info'] }}"

- name: Task to use custom module with argument
    justinbatchelor.redhat_assisted_installer.cluster_info:
    cluster_id: '{{ all_cluster_info["cluster_info"][0]["id"] }}'
    register: cluster_info


- debug:
    msg: "{{ cluster_info['cluster_info'][0] }}"

'''

RETURN = r'''
cluster_info
'''




def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        cluster_id = dict(type='str', default=None),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        cluster_info='',

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

    if module.params['cluster_id'] is None:
        result['cluster_info'] = installer.get_clusters()
    else:
        result['cluster_info'] = installer.get_cluster(cluster_id=module.params['cluster_id'])


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