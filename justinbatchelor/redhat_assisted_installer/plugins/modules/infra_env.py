#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule
from redhat_assisted_installer import assisted_installer
from ..module_utils import tools
import jmespath, requests, os, json

from redhat_assisted_installer.lib.schema.infra_env import *

from requests.exceptions import HTTPError

__metaclass__ = type

DOCUMENTATION = r'''
---
module: infra_env

short_description: 

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: 

options:


requirements:
  - "python >= 3.12"
  - "requirements.txt"


author:
    - Justin Batchelor (@justinbatchelor)
'''

EXAMPLES = r'''

'''

RETURN = r'''

'''

def run_module():
    module_args = dict(
        additional_ntp_source=dict(type='str', required=False),
        additional_trust_bundle=dict(type='str', required=False),
        cluster_id=dict(type='str', required=False),
        cpu_architecture=dict(type='str', required=False, choices=['x86_64', 'aarch64', 'arm64', 'ppc64le', 's390x']),
        image_type=dict(type='str', required=False, choices=["full-iso", "minimal-iso"]),
        infra_env_id=dict(type='str', required=False),
        name=dict(type='str', required=False),
        offline_token=dict(type='str', required=False, no_log=True),
        openshift_version=dict(type='str', required=False),
        pull_secret=dict(type='str', required=False, no_log=True),
        state=dict(type='str', required=True, choices=['present', 'absent']),
        ssh_authorized_key=dict(type='str', required=False),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        msg='',
        infra_env='',
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

    ## First we want to create the cluster object provided the arguments from the user
    infra_env = InfraEnv(infra_env_id=module.params['infra_env_id'],
                         name=module.params["name"],
                         openshift_version=module.params["openshift_version"],
                         cluster_id=module.params['cluster_id'],
                         additional_ntp_source=module.params['additional_ntp_source'],
                         additional_trust_bundle=module.params['additional_trust_bundle'],
                         image_type=module.params['image_type'],
                         ssh_authorized_key=module.params['ssh_authorized_key'],
                         )
    

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