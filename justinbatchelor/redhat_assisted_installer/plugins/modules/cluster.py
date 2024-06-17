#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule
from redhat_assisted_installer import assisted_installer
from ..module_utils import tools
import jmespath, requests, os, json

from redhat_assisted_installer.lib.schema.cluster import *

from requests.exceptions import HTTPError

__metaclass__ = type

DOCUMENTATION = r'''
---
module: cluster

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
        state=dict(type='str', required=True, choices=['present', 'absent']),
        pull_secret=dict(type='str', required=False, no_log=True),
        offline_token=dict(type='str', required=False, no_log=True),
        cluster_id=dict(type='str', required=False),
        name=dict(type='str', required=False),
        api_vip=dict(type='str', required=False),
        openshift_version=dict(type='str', required=False),
        additional_ntp_source=dict(type='str', required=False),
        base_dns_domain=dict(type='str', required=False),
        cluster_network_cidr=dict(type='str', required=False),
        cluster_network_host_prefix=dict(type='int', required=False),
        cpu_architecture=dict(type='str', required=False, choices=['x86_64', 'aarch64', 'arm64', 'ppc64le', 's390x']),
        high_availability_mode=dict(type='str', required=False, choices=["None", "Full"]),
        http_proxy=dict(type='str', required=False),
        https_proxy=dict(type='str', required=False),
        hyperthreading=dict(type='str', required=False, choices=['all', 'none', "masters", "workers"]),
        ingress_vip=dict(type='str', required=False),
        network_type=dict(type='str', required=False, choices=['OpenShiftSDN', 'OVNKubernetes']),
        service_network_cidr=dict(type='str', required=False),
        user_managed_networking=dict(type='bool', required=False),
        ssh_authorized_key=dict(type='str', required=False),
        vip_dhcp_allocation=dict(type='bool', required=False),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        msg='',
        auth={
            "offline_token": "",
            "pull_secret": "",
        },
        cluster=''
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

    # set result.auth fields to match env vars
    result['auth']['offline_token'] = os.environ.get("REDHAT_OFFLINE_TOKEN")
    result['auth']['pull_secret'] = os.environ.get("REDHAT_PULL_SECRET")


    ## First we want to create the cluster object provided the arguments from the user
    cluster_params = ClusterParams(name=module.params["name"],
                            openshift_version=module.params["openshift_version"],
                            cluster_id=module.params['cluster_id'],
                            additional_ntp_source=module.params['cluster_id'],
                            api_vip=module.params['api_vip'],
                            base_dns_domain=module.params['base_dns_domain'],
                            cluster_network_cidr=module.params['cluster_network_cidr'],
                            cluster_network_host_prefix=module.params['cluster_network_host_prefix'],
                            cpu_architecture=module.params['cpu_architecture'],
                            high_availability_mode=module.params['high_availability_mode'],
                            http_proxy=module.params['http_proxy'],
                            https_proxy=module.params['https_proxy'],
                            hyperthreading=module.params['hyperthreading'],
                            ingress_vip=module.params['ingress_vip'],
                            network_type=module.params['network_type'],
                            service_network_cidr=module.params['service_network_cidr'],
                            user_managed_networking=module.params['user_managed_networking'],
                            ssh_authorized_key=module.params['ssh_authorized_key'],
                            vip_dhcp_allocation=module.params['vip_dhcp_allocation'],
                            )


    # create installer object that implements the RH assisted installer API
    installer = assisted_installer.assisted_installer()

    # If the state is present, we will need to consider create or update
    if module.params['state'] == 'present':
        # If user did not specifiy either cluster_id or name we need to fail, as a name is required to create a cluster
        if module.params["cluster_id"] is None and module.params["name"] is None:
            # fail message
            module.fail_json(msg='When state is present you must specifiy at least a name. If a cluster does not already exist with that name, this module will create one. Please update the corresponding args and try to rerun.', **result)
        """
        handle cases
        1. User specified both cluster_id and name
        2. User only specified cluster_id
        
        We can infer that at this point that we are updating an existing cluster
        """
        if (module.params['cluster_id'] is not None and module.params['name'] is not None) or (module.params["cluster_id"] is not None):
            try:
                cluster = installer.patch_cluster(cluster_params)
                result['changed'] = True
                result['msg'] = cluster
                result['cluster'] = cluster               
                module.exit_json(**result)

            except Exception as e:
                result['changed'] = False
                module.fail_json(msg=f'Failed to patch the cluster with the following exception from api\nERR: {e}', **result)

        """
        handle case 
        1. only case that remains is the user specifed a name without a cluster id

        We will need to check that a cluster does not already exist with that name before we can determine if we are creating or updating a cluster
        """
        if module.params['cluster_id'] is None and module.params['name'] is not None:
            # need to query for existing clusters and ensure that one does not already exist with that name
            clusters = installer.get_clusters()

            # JMESPath expression to filter objects by name
            expression = f"[?name=='{module.params["name"]}']"

            # Search the API response using the JMESPath expression
            filtered_response = jmespath.search(expression, clusters)
            
            # all cluster names should be unique, fail if filtered response is greater than 1
            if len(filtered_response) > 1:
                # fail for one of two reasons listed in message
                module.fail_json(msg='We ran into a stange error. It seems you have multiple clusters with the same name, or our JMESpath expression is not working as expected.', **result)
            # now we know we are patching an existing cluster
            if len(filtered_response) == 1:
                try:
                    cluster = installer.patch_cluster(cluster_params)
                    result['changed'] = True
                    result['msg'] = cluster
                    result['cluster'] = cluster               
                    module.exit_json(**result)

                except Exception as e:
                    result['changed'] = False
                    module.fail_json(msg=f'Failed to patch the cluster with the following exception from api\nERR: {e}', **result)

            if len(filtered_response) == 0:
                try: 
                    cluster = installer.post_cluster(cluster_params)
                    result['changed'] = True
                    result['msg'] = cluster
                    result['cluster'] = cluster 
                    module.exit_json(**result)

                except Exception as e:
                    result['changed'] = False
                    module.fail_json(msg=f'Failed to create the cluster with the following exception from api\nERR: {e}', **result)
                
    # Otherwise the state is absent and we will delete the cluster
    else:
        # In order to delete the cluster we will need the cluster_id or name at bare minimum 
        if module.params["cluster_id"] is None and module.params["name"] is None:
            # fail because both params are not defined
            module.fail_json(msg='You must provide either the name, cluster_id, or both to delete a cluster. Please update the corresponding args and try to rerun.', **result)
        # handle cases
        # 1. User specified both cluster_id and name
        # 2. User only specified cluster_id
        if (module.params['cluster_id'] is not None and module.params['name'] is not None) or (module.params["cluster_id"] is not None):
            # if delete_cluster() succeeds
            try:
                installer.delete_cluster(cluster_id=module.params['cluster_id'])
                result['changed'] = True
                result['msg'] = f"Successfully deleted cluster: {module.params['cluster_id']}"
                module.exit_json(**result)

            except requests.exceptions.HTTPError as e:
                result['changed'] = False
                result['msg'] = f"Failed to delete cluster: {module.params['cluster_id']}\nAPI call returned a bad status code"
                module.fail_json(msg='Functionality is under development right now... please specify the cluster_id.', **result)
        # handle the case where user specified name only
        else:
            # need to query for existing clusters and ensure that one does not already exist with that name
            clusters = installer.get_clusters()

            # JMESPath expression to filter objects by name
            expression = f"[?name=='{module.params["name"]}']"

            # Search the API response using the JMESPath expression
            filtered_response = jmespath.search(expression, clusters)

            # all cluster names should be unique, fail if filtered response is greater than 1
            if len(filtered_response) > 1:
                # fail for one of two reasons listed in message
                module.fail_json(msg='We ran into a stange error. It seems you have multiple clusters with the same name, or our JMESpath expression is not working as expected.', **result)
            # now we know we are patching an existing cluster
            if len(filtered_response) == 1:
                try:
                    installer.delete_cluster(cluster_id=filtered_response[0]['id'])
                    result['changed'] = True
                    result['msg'] = f"Successfully deleted cluster: {filtered_response[0]['id']}"
                    module.exit_json(**result)
                except Exception as e:
                    result['changed'] = False
                    result['msg'] = f"Failed to delete cluster: {module.params['cluster_id']}\nAPI call returned a bad status code"
                    module.fail_json(msg='Functionality is under development right now... please specify the cluster_id.', **result)
        

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