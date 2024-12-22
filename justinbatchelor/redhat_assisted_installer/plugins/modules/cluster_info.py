#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.api import *
from ..module_utils.tools import *


__metaclass__ = type

DOCUMENTATION = r'''
---
module: cluster_info
short_description: Retrieve information about OpenShift clusters managed by the Red Hat Assisted Installer
version_added: "0.0.1"
description: >
  This module allows you to retrieve information about OpenShift clusters from the Red Hat Assisted Installer,
  either for all clusters or for a specific cluster identified by its cluster_id.
options:
  cluster_id:
    description:
      - Cluster ID for the assisted installer managed cluster.
    type: str
    required: false
author:
  - Justin Batchelor (@justinbatchelor)
'''

EXAMPLES = r'''
# Retrieve information about all clusters
- name: Get information about all clusters
  justinbatchelor.redhat_assisted_installer.cluster_info:
  register: all_cluster_info

# Retrieve information about a specific cluster
- name: Get information about a specific cluster
  justinbatchelor.redhat_assisted_installer.cluster_info:
    cluster_id: '{{ all_cluster_info["cluster_info"][0]["id"] }}'
  register: cluster_info

'''

RETURN = r'''
cluster_info:
  description: >
    List of cluster information retrieved from the Red Hat Assisted Installer.
  returned: always
  type: list
  elements: dict
  sample: 
    - id: "123"
      name: "cluster1"
      status: "active"
count:
  description: >
    The number of clusters returned.
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
        cluster_id = dict(type='str', default=None),
        offline_token=dict(type='str', required=False, no_log=True),
        pull_secret=dict(type='str', required=False, no_log=True),

    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        cluster_info=[],
        count='',
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

    ## First we need to check if the user provided an offline token 
    if module.params['offline_token'] is not None:
        os.environ["REDHAT_OFFLINE_TOKEN"] = module.params["offline_token"]

    ## Now we need to check if the user provided a pull secret
    if module.params['pull_secret'] is not None:
        os.environ["REDHAT_PULL_SECRET"] = module.params["pull_secret"]

    try:
        api_response = None
        if module.params['cluster_id'] is None:
            api_response = get_clusters()
        else:
            api_response = get_cluster(cluster_id=module.params['cluster_id'])
        api_response.raise_for_status()
        result['cluster_info'] = [api_response.json()] if isinstance(api_response.json(), dict) else api_response.json()
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