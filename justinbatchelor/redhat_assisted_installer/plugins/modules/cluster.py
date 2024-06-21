#!/usr/bin/python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.api import *
from ..module_utils.tools import *
from ..module_utils.schema.cluster import *

import jmespath, os

__metaclass__ = type

DOCUMENTATION = r'''
---
module: cluster
short_description: Manage OpenShift clusters
version_added: "1.0.0"
description: >
  This module allows managing OpenShift clusters using the Red Hat Assisted Installer API.
options:
  additional_ntp_source:
    description: A list of NTP sources (name or IP) to be added to all the hosts.
    type: list
    required: false
  api_vips:
    description: A list of virtual IPs used to reach the OpenShift cluster's API.
    type: list
    required: false
    elements: dict
    suboptions:
      cluster_id:
        description: The cluster that this VIP is associated with.
        type: str
        required: true
      ip:
        description: The virtual IP address.
        type: str
        required: true
      verification:
        description: VIP verification result.
        type: str
        required: false
        choices: ["unverified", "failed", "succeeded"]
  base_dns_domain:
    description: Base domain of the cluster. All DNS records must be sub-domains of this base and include the cluster name.
    type: str
    required: false
  cluster_networks:
    description: Cluster networks that are associated with this cluster.
    type: list
    required: false
    elements: dict
    suboptions:
      cidr:
        description: A network from which Pod IPs are allocated. This block must not overlap with existing physical networks.
        type: str
        required: true
      cluster_id:
        description: The cluster that this network is associated with.
        type: str
        required: false
      host_prefix:
        description: The subnet prefix length to assign to each individual node.
        type: int
        required: false
  cluster_id:
    description: ID of the cluster.
    type: str
    required: false
  cpu_architecture:
    description: The CPU architecture of the image.
    type: str
    required: false
    choices: ['x86_64', 'aarch64', 'arm64', 'ppc64le', 's390x']
  disk_encryption:
    description: Disk encryption settings.
    type: dict
    required: false
    suboptions:
      enable_on:
        description: Enable/disable disk encryption on master nodes, worker nodes, or all nodes.
        type: str
        required: true
        choices: ["none", "all", "masters", "workers"]
      mode:
        description: The disk encryption mode to use.
        type: str
        required: true
        choices: ["tang", "tpmv2"]
      tang_server:
        description: JSON-formatted string containing additional information regarding tang's configuration.
        type: str
        required: false
  high_availability_mode:
    description: Guaranteed availability of the installed cluster.
    type: str
    required: false
    choices: ["None", "Full"]
  http_proxy:
    description: A proxy URL to use for creating HTTP connections outside the cluster.
    type: str
    required: false
  https_proxy:
    description: A proxy URL to use for creating HTTPS connections outside the cluster.
    type: str
    required: false
  hyperthreading:
    description: Enable/disable hyperthreading on master nodes, worker nodes, or all nodes.
    type: str
    required: false
    choices: ['all', 'none', "masters", "workers"]
  ignition_endpoint:
    description: Explicit ignition endpoint overrides the default ignition endpoint.
    type: dict
    required: false
    suboptions:
      ca_certificate:
        description: Base64 encoded CA certificate to be used when contacting the URL via https.
        type: str
        required: true
      url:
        description: The URL for the ignition endpoint.
        type: str
        required: true
  ingress_vips:
    description: The virtual IPs used for cluster ingress traffic.
    type: list
    required: false
    elements: dict
    suboptions:
      cluster_id:
        description: The cluster that this VIP is associated with.
        type: str
        required: false
      ip:
        description: The virtual IP address.
        type: str
        required: true
      verification:
        description: VIP verification result.
        type: str
        required: false
        choices: ["unverified", "failed", "succeeded"]
  machine_networks:
    description: Machine networks that are associated with this cluster.
    type: list
    required: false
    elements: dict
    suboptions:
      cidr:
        description: A network that all hosts belonging to the cluster should have an interface with IP address in.
        type: str
        required: true
      cluster_id:
        description: The cluster that this network is associated with.
        type: str
        required: false
  name:
    description: Name of the OpenShift cluster.
    type: str
    required: false
  network_type:
    description: The desired network type used.
    type: str
    required: false
    choices: ['OpenShiftSDN', 'OVNKubernetes']
  offline_token:
    description: Offline token for authentication.
    type: str
    required: false
    no_log: true
  olm_operators:
    description: List of OLM operators to be installed.
    type: list
    required: false
    elements: dict
    suboptions:
      name:
        description: Name of the OLM operator.
        type: str
        required: true
      properties:
        description: Blob of operator-dependent parameters that are required for installation.
        type: str
        required: false
  openshift_version:
    description: Version of the OpenShift cluster.
    type: str
    required: false
  platform:
    description: The configuration for the specific platform upon which to perform the installation.
    type: dict
    required: false
    suboptions:
      external:
        description: Configuration used when installing with an external platform type.
        type: dict
        required: false
        suboptions:
          cloud_controller_manager:
            description: When set to external, this property will enable an external cloud provider.
            type: str
            required: true
            choices: ["", "External"]
          platform_name:
            description: Holds the arbitrary string representing the infrastructure provider name.
            type: str
            required: true
      type:
        description: Type of platform.
        type: str
        required: true
        choices: ["baremetal", "nutanix", "vsphere", "none", "external"]
  pull_secret:
    description: The pull secret obtained from Red Hat OpenShift Cluster Manager.
    type: str
    required: false
    no_log: true
  schedulable_masters:
    description: Schedule workloads on masters.
    type: bool
    required: false
  service_networks:
    description: Service networks that are associated with this cluster.
    type: list
    required: false
    elements: dict
    suboptions:
      cidr:
        description: IP address block for service IP blocks.
        type: str
        required: true
      cluster_id:
        description: A network to use for service IP addresses.
        type: str
        required: false
  state:
    description: The desired state of the cluster.
    type: str
    required: true
    choices: ['present', 'absent']
  tags:
    description: A comma-separated list of tags that are associated to the cluster.
    type: str
    required: false
  user_managed_networking:
    description: Indicate if the networking is managed by the user.
    type: bool
    required: false
  ssh_public_key:
    description: SSH public key for debugging OpenShift nodes.
    type: str
    required: false
  vip_dhcp_allocation:
    description: Indicate if virtual IP DHCP allocation mode is enabled.
    type: bool
    required: false


requirements:
  - requests==2.32.3
  - ansible==10.1.0
  - jmespath==1.0.1

  
author:
  - Justin Batchelor (@justinbatchelor)
'''

EXAMPLES = r'''
# Create a new OpenShift cluster
- name: Create a new OpenShift cluster
  justinbatchelor.redhat_assisted_installer.cluster:
    state: present
    name: "my-new-cluster"
    base_dns_domain: "example.com"
    pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
    ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
  register: result

- debug:
    msg: "{{ result }}"

# Delete an existing OpenShift cluster
- name: Delete an OpenShift cluster
  justinbatchelor.redhat_assisted_installer.cluster:
    state: absent
    cluster_id: "your-cluster-id"
  register: result

- debug:
    msg: "{{ result }}"
'''

RETURN = r'''
cluster:
  description: >
    Details of the created, updated, or deleted cluster.
  returned: always
  type: list
  elements: dict
  sample: 
    - id: "123"
      name: "my-cluster"
      status: "active"
msg:
  description: >
    Message indicating the status of the operation.
  returned: always
  type: str
  sample: "Successfully created the cluster."
'''


SUCCESS_GET_CODE = 200
SUCCESS_POST_CODE = SUCCESS_PATCH_CODE = 201
SUCCESS_DELETE_CODE = 204

def format_module_results(results: dict, msg: str = None, cluster: list = None, changed: bool = None):
    if msg is not None:
        results['msg'] = msg

    if cluster is not None:
        results['cluster'] = cluster

    if changed is not None:
        results['changed'] = changed

def run_module():
    module_args = dict(
        additional_ntp_sources=dict(type='list', required=False),
        api_vips=dict(type='list', elements='dict', required=False, options=dict(
            cluster_id=dict(type='str', required=False),
            ip=dict(type='str', required=True),
            verification=dict(type='str', required=False, choices=["unverified", "failed", "succeeded"])
        )),
        base_dns_domain=dict(type='str', required=False),
        cluster_networks=dict(type='list',elements='dict', required=False, options=dict(
            cidr=dict(type='str', required=True),
            cluster_id=dict(type='str', required=False),
            host_prefix=dict(type='int', required=False),
        )),
        cluster_id=dict(type='str', required=False),
        cpu_architecture=dict(type='str', required=False, choices=['x86_64', 'aarch64', 'arm64', 'ppc64le', 's390x']),
        disk_encryption=dict(type='dict',required=False,options=dict(
            enable_on=dict(type='str', required=True, choices=["none", "all", "masters", "workers"]),
            mode=dict(type='str', required=True, choices=["tang", "tpmv2"]),
            tang_server=dict(type='str', required=False),
        )),
        high_availability_mode=dict(type='str', required=False, choices=["None", "Full"]),
        http_proxy=dict(type='str', required=False),
        https_proxy=dict(type='str', required=False),
        hyperthreading=dict(type='str', required=False, choices=['all', 'none', "masters", "workers"]),
        ignition_endpoint=dict(type='dict',elements='dict', required=False, options=dict(
            ca_certificate=dict(type='str', required=True),
            url=dict(type='str', required=True)
        )),
        ingress_vips=dict(type='list',elements='dict',required=False,options=dict(
            cluster_id=dict(type='str', required=False),
            ip=dict(type='str', required=True),
            verification=dict(type='str', required=False, choices=["unverified", "failed", "succeeded"]),
        )),
        machine_networks=dict(type='list', elements='dict', required=False, options=dict(
            cidr=dict(type='str', required=True),
            cluster_id=dict(type='str', required=False),
        )),
        name=dict(type='str', required=False),
        network_type=dict(type='str', required=False, choices=['OpenShiftSDN', 'OVNKubernetes']),
        offline_token=dict(type='str', required=False, no_log=True),
        olm_operators=dict(type='list', elements='dict', required=False, options=dict(
            name=dict(type='str', required=True),
            properties=dict(type='str', required=False),
        )),
        openshift_version=dict(type='str', required=False),
        platform=dict(type='dict', required=False, options=dict(
            external=dict(type='dict', required=False, options=dict(
                cloud_controller_manager=dict(type='str', required=True, choices=["", "External"]),
                platform_name=dict(type='str', required=True),
            )),
            type=dict(type='str', required=True, choices=["baremetal", "nutanix", "vsphere", "none", "external"]),
        )),
        pull_secret=dict(type='str', required=False, no_log=True),
        schedulable_masters=dict(type='bool', required=False),
        service_networks=dict(type='list', elements='dict', required=False, options=dict(
            cidr=dict(type='str', required=True),
            cluster_id=dict(type='str', required=False),
        )),
        state=dict(type='str', required=True, choices=['present', 'absent']),
        tags=dict(type='str', required=False),
        user_managed_networking=dict(type='bool', required=False),
        ssh_public_key=dict(type='str', required=False),
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
        cluster=[],
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

    # get all clusters
    get_cluster_response = get_clusters()

    if get_cluster_response.status_code != SUCCESS_GET_CODE:
        format_module_results(results=result,
                              msg=f"Failed to get clusters {get_cluster_response.json()}",
                              changed=True,
                              cluster=[],
                              )
        # fail module
        module.fail_json(**result)
    
    # check that a name or id was provided, fail if not
    if module.params['cluster_id'] is None and module.params['name'] is None:
        format_module_results(results=result,
                              msg=f"You must specifiy either an cluster ID or a NAME when STATE == {module.params['state']}",
                              changed=True,
                              result=[],
                              )
        module.fail_json(**result)

    filtered_response = jmespath_id_validator(module.params['cluster_id'], get_cluster_response.json()) if module.params['cluster_id'] is not None else jmespath_name_validator(module.params['name'], get_cluster_response.json())

    # user defined a state of present
    if module.params['state'] == "present":
        ## First we want to create the cluster object provided the arguments from the user
        cluster = Cluster(
            additional_ntp_sources=create_additional_ntp_sources_from_params(module.params['additional_ntp_sources']),
            api_vips=create_api_vips_from_module_params(module.params['api_vips']),
            base_dns_domain=module.params['base_dns_domain'],
            cluster_networks=create_cluster_networks_from_module_params(module.params['cluster_networks']),
            cluster_id=module.params['cluster_id'],
            cpu_architecture=module.params['cpu_architecture'],
            disk_encryption=create_disk_encryption_from_module_params(module.params['disk_encryption']),
            high_availability_mode=module.params['high_availability_mode'],
            http_proxy=module.params['http_proxy'],
            https_proxy=module.params['https_proxy'],
            hyperthreading=module.params['hyperthreading'],
            ignition_endpoint=create_ignition_endpoint_from_module_params(module.params['ignition_endpoint']),
            ingress_vips=create_ingress_vips_from_module_params(module.params['ingress_vips']),
            machine_networks=create_machine_networks_from_module_params(module.params['machine_networks']),
            name=module.params['name'],
            network_type=module.params['network_type'],
            olm_operator=create_olm_operators_from_module_params(module.params['olm_operators']),
            openshift_version=module.params["openshift_version"],
            platform=create_platform_from_module_params(module.params['platform']),
            schedulable_masters=module.params['schedulable_masters'],
            service_networks=create_service_networks_from_module_params(module.params['service_networks']),
            tags=module.params['tags'],
            user_managed_networking=module.params['user_managed_networking'],
            ssh_public_key=module.params['ssh_public_key'],
            vip_dhcp_allocation=module.params['vip_dhcp_allocation'],
        )
        
        if len(filtered_response) == 0:
            create_cluster_response = post_cluster(cluster=cluster)
            if create_cluster_response.status_code != SUCCESS_POST_CODE:
                format_module_results(results=result,
                                      msg=f'Failed to create the cluster: {create_cluster_response.json()}',
                                      cluster=[],
                                      changed=False,
                                      )
                module.fail_json(**result)
              
            format_module_results(results=result,
                                  msg=f"Successfully created the cluster: {create_cluster_response.json()['id']}",
                                  changed=True,
                                  cluster=[create_cluster_response.json()],
                                  )
            module.exit_json(**result)

        elif len(filtered_response) == 1:
            modified_params = remove_matching_pairs(cluster.create_params(), filtered_response[0])
            result['msg'] = modified_params
            patch_cluster_response = patch_cluster(filtered_response[0]['id'], modified_params)
            if patch_cluster_response.status_code != SUCCESS_PATCH_CODE:
                format_module_results(results=result,
                                      msg=f'Failed to patch the cluster: {patch_cluster_response.json()}',
                                      cluster=[],
                                      changed=False,
                                      )
                module.fail_json(**result)
            format_module_results(results=result,
                                  msg=f"Successfully patched the cluster: {patch_cluster_response.json()['id']}",
                                  changed=True,
                                  cluster=[patch_cluster_response.json()],
                                  )
            module.exit_json(**result)
            
        else:
           format_module_results(results=result,
                                 msg="Found more than one instance of the cluster you defined",
                                 changed=False,
                                 cluster=[])
           module.fail_json(**result)
    # otherwise the state is absent
    else:     
        if len(filtered_response) == 0:
          format_module_results(results=result,
                                msg="cluster not found.",
                                changed=False,
                                cluster=[])
          module.exit_json(**result)

        elif len(filtered_response) == 1:
            if delete_cluster(cluster_id=filtered_response[0]['id']):
                format_module_results(results=result, 
                                      msg=result['msg'] + f"Successfully deleted cluster: {filtered_response[0]['id']}\n",
                                      changed=True,
                                      cluster=result['cluster'].append(filtered_response[0]),
                                      )
                module.exit_json(**result)
            else: 
                format_module_results(results=result, 
                                      msg=result['msg'] + f"Failed to delete cluster: {filtered_response[0]['id']}\n",
                                      changed=False,
                                      cluster=result['cluster'].append(filtered_response[0]),
                                      )
                module.fail_json(**result)
        else:
            # fail for one of two reasons listed in message
            format_module_results(results=result, 
                                  msg='We ran into a stange error. It seems you have multiple clusters with the same name, or our JMESpath expression is not working as expected.',
                                  changed=False,
                                  cluster=[],
                                  )
            module.fail_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()