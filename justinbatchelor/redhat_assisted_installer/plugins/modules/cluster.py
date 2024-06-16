#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule
from redhat_assisted_installer import assisted_installer
from ..module_utils import tools
import jmespath, requests, os

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
        name=dict(type='str', required=False),
        cluster_id=dict(type='str', required=False),
        openshift_version=dict(type='str', required=False),
        pull_secret=dict(type='str', required=False, no_log=True),
        offline_token=dict(type='str', required=False, no_log=True),
        additional_ntp_source=dict(type='str', required=False),
        # api_vips=dict(type='list', elements='dict', options=dict(
        #     ip=dict(type='str', required=True),
        #     netmask=dict(type='str', required=True)
        # )),
        base_dns_domain=dict(type='str', required=False),
        cluster_network_cidr=dict(type='str', required=False),
        cluster_network_host_prefix=dict(type='int', required=False),
        cluster_networks=dict(type='list', elements='dict', options=dict(
            cidr=dict(type='str', required=True),
            cluster_id=dict(type='str', required=True)
        )),
        cpu_architecture=dict(type='str', required=False, choices=['x86_64', 'aarch64', 'arm64', 'ppc64le', 's390x']),
        disk_encryption=dict(type='dict', options=dict(
            enable_on=dict(type='str', required=True),
            mode=dict(type='str', required=True),
            tang_servers=dict(type='str', required=False),
        )),
        high_availability_mode=dict(type='str', required=False),
        http_proxy=dict(type='str', required=False),
        https_proxy=dict(type='str', required=False),
        hyperthreading=dict(type='str', required=False, choices=['all', 'none']),
        ignition_endpoint=dict(type='dict', options=dict(
            url=dict(type='str', required=True),
            ca_certificate=dict(type='str', required=False),
        )),
        ingress_vips=dict(type='list', elements='dict', options=dict(
            ip=dict(type='str', required=True),
            netmask=dict(type='str', required=True)
        )),
        machine_networks=dict(type='list', elements='dict', options=dict(
            cidr=dict(type='str', required=True),
            cluster_id=dict(type='str', required=True)
        )),
        network_type=dict(type='str', required=False, choices=['OpenShiftSDN', 'OVNKubernetes']),
        no_proxy=dict(type='str', required=False),
        ocp_release_image=dict(type='str', required=False),
        olm_operators=dict(type='list', elements='dict', options=dict(
            name=dict(type='str', required=True),
            namespace=dict(type='str', required=True)
        )),
        platform=dict(type='dict', options=dict(
            type=dict(type='str', required=True, choices=["baremetal", "nutanix", "vsphere", "none", "oci"]),
        )),
        schedulable_masters=dict(type='bool', required=False),
        service_network_cidr=dict(type='str', required=False),
        service_networks=dict(type='list', elements='dict', options=dict(
            cidr=dict(type='str', required=True),
            cluster_id=dict(type='str', required=True)
        )),
        ssh_public_key=dict(type='str', required=False),
        tags=dict(type='str', required=False),
        user_managed_networking=dict(type='bool', required=False),
        vip_dhcp_allocation=dict(type='bool', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        msg = '',
        cluster = '',
        state='',

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

    # create installer object that implements the RH assisted installer API
    installer = assisted_installer.assisted_installer()

    if module.params["pull_secret"] is not None:
        os.environ["REDHAT_PULL_SECRET"] = module.params["pull_secret"]

    if module.params["offline_token"] is not None:
        os.environ["REDHAT_OFFLINE_TOKEN"] = module.params["offline_token"]

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
            ## TODO ## 
            # need to query for existing clusters and patch based on user specified args
            print("under construction... beep boop bop")
        """
        handle case 
        1. only case that remains is the user specifed a name without a cluster id

        We will need to check that a cluster does not already exist with that name before we can determine if we are creating or updating a cluster
        """
        if module.params['cluster_id'] is None and module.params['name'] is not None:
            ## TODO ##
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
                print("under construction")
            # no cluster exists with that name in this org, we are doing a create operation
            if len(filtered_response) == 0:
                try: 
                    cluster = installer.post_cluster(name=module.params['name'], 
                                                    openshift_version=module.params['openshift_version'], 
                                                    additional_ntp_source=module.params['additional_ntp_source'],
                                                    base_dns_domain=module.params['base_dns_domain'], 
                                                    luster_network_cidr=module.params['cluster_network_cidr'], 
                                                    cluster_network_host_prefix=module.params['cluster_network_host_prefix'], 
                                                    cpu_architecture=module.params['cpu_architecture'], 
                                                    high_availability_mode=module.params['high_availability_mode'], 
                                                    http_proxy=module.params['http_proxy'], 
                                                    https_proxy=module.params['https_proxy'], 
                                                    hyperthreading=module.params['hyperthreading'], 
                                                    network_type=module.params['network_type'], 
                                                    no_proxy=module.params['no_proxy'], 
                                                    ocp_release_image=module.params['ocp_release_image'],
                                                    schedulable_masters=module.params['schedulable_masters'], 
                                                    service_network_cidr=module.params['service_network_cidr'],
                                                    service_networks=module.params['service_networks'], 
                                                    ssh_public_key=module.params['ssh_public_key'], 
                                                    tags=module.params['tags'], 
                                                    user_managed_networking=module.params['user_managed_networking'], 
                                                    vip_dhcp_allocation=module.params['vip_dhcp_allocation'],
                                                    )

                    result['changed'] = True
                    result['msg'] = cluster
                    result['state'] = cluster
                    module.exit_json(**result)

                except requests.exceptions.HTTPError as e:
                    result['changed'] = False
                    result['msg'] = f'{e}'
                    module.fail_json(msg=f'Failed to create the cluster api call return bad status code\nERR: {e}', **result)

                except Exception as e:
                    result['changed'] = False
                    result['msg'] = f'{e}'
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
                installer.delete_cluster(id=module.params['cluster_id'])
                result['changed'] = True
                result['msg'] = f"Successfully deleted cluster: {module.params['cluster_id']}"
                module.exit_json(**result)

            except requests.exceptions.HTTPError as e:
                result['changed'] = False
                result['msg'] = f"Failed to delete cluster: {module.params['cluster_id']}\nAPI call returned a bad status code"
                module.fail_json(msg='Functionality is under development right now... please specify the cluster_id.', **result)
        # handle the case where user specified name only
        else:
            # fail because not implemented yet
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