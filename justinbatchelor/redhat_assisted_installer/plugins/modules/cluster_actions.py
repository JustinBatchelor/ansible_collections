#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.api import *
from ..module_utils.tools import *


__metaclass__ = type

DOCUMENTATION = r'''
'''

EXAMPLES = r'''

'''

RETURN = r'''

'''
SUCCESS_GET_CODE = 200
SUCCESS_POST_CODE = SUCCESS_PATCH_CODE = 201
SUCCESS_ACTION_CODE = 202
SUCCESS_DELETE_CODE = 204

def format_module_results(results: dict, msg: str = None, cluster: list = None, changed: bool = None):
    if msg is not None:
        results['msg'] = msg

    if cluster is not None:
        results['cluster'] = cluster

    if changed is not None:
        results['changed'] = changed

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        cluster_id = dict(type='str', default=None),
        cluster_name = dict(type='str', default=None),
        offline_token=dict(type='str', required=False, no_log=True),
        pull_secret=dict(type='str', required=False, no_log=True),
        state=dict(type='str', required=True, choices=["install", "cancel", "reset"])
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        msg='',
        cluster='',

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

    # get all clusters
    get_cluster_response = get_clusters()

    if get_cluster_response.status_code != SUCCESS_GET_CODE:
        format_module_results(results=result,
                              msg=f"Failed to get clusters {get_cluster_response.json()}",
                              changed=False,
                              cluster=[],
                              )
        # fail module
        module.fail_json(**result)
    
        # check that a name or id was provided, fail if not
    if module.params['cluster_id'] is None and module.params['name'] is None:
        format_module_results(results=result,
                              msg=f"You must specifiy either an cluster ID or a NAME when STATE == {module.params['state']}",
                              changed=False,
                              result=[],
                              )
        module.fail_json(**result)

    filtered_response = jmespath_id_validator(module.params['cluster_id'], get_cluster_response.json()) if module.params['cluster_id'] is not None else jmespath_name_validator(module.params['name'], get_cluster_response.json())

    if len(filtered_response) != 1:
        format_module_results(results=result,
                              msg="Found more than one instance of the cluster you defined, or the cluster you defined does not exist",
                              changed=False,
                              cluster=[])
        module.fail_json(**result)
    
    action_response = None

    if module.params["state"] == "install":
        action_response = cluster_action_install(filtered_response[0]['id'])
    elif module.params["state"] == "cancel":
        action_response = cluster_action_cancel(filtered_response[0]['id'])
    else:
        action_response = cluster_action_reset(filtered_response[0]['id'])

    if action_response.status_code != SUCCESS_ACTION_CODE:
        format_module_results(results=result,
                              msg=f"Failed to {module.params['state']} the cluster {filtered_response[0]['id']}. {action_response.json()}",
                              changed=False,
                              cluster=[])
        module.fail_json(**result)
    
    format_module_results(results=result,
                          msg=f"Successfully {module.params["state"]} cluster. {filtered_response[0]['id']}",
                          changed=True,
                          cluster=[action_response.json()]
                          )

    module.exit_json(**result)
    

def main():
    run_module()


if __name__ == '__main__':
    main()