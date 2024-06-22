# justinbatchelor.redhat_assisted_installer.cluster

Ansible module to implement the POST / PATCH / DELETE operations for cluster objects documented by the [Red Hat Assisted Installer API](https://developers.redhat.com/api-catalog/api/assisted-install-service#content-operations)

## Examples

```
---
- name: Create a basic OpenShift cluster
  hosts: localhost
  tasks:
    - name: Create a new OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: present
        name: "basic-cluster"
        base_dns_domain: "example.com"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
      register: result


---
- name: Create OpenShift cluster with CPU architecture
  hosts: localhost
  tasks:
    - name: Create a new OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: present
        name: "cpu-arch-cluster"
        base_dns_domain: "example.com"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        cpu_architecture: "x86_64"
      register: result

---
- name: Create OpenShift cluster with proxy
  hosts: localhost
  tasks:
    - name: Create a new OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: present
        name: "proxy-cluster"
        base_dns_domain: "example.com"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        http_proxy: "http://proxy.example.com:8080"
        https_proxy: "http://proxy.example.com:8443"
      register: result

---
- name: Create OpenShift cluster with cluster networks
  hosts: localhost
  tasks:
    - name: Create a new OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: present
        name: "network-cluster"
        base_dns_domain: "example.com"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        cluster_networks:
          - cidr: "10.128.0.0/14"
            host_prefix: 23
      register: result

---
- name: Create OpenShift cluster with disk encryption
  hosts: localhost
  tasks:
    - name: Create a new OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: present
        name: "encrypted-cluster"
        base_dns_domain: "example.com"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        disk_encryption:
          enable_on: "all"
          mode: "tang"
          tang_server: "{{ lookup('file', 'path/to/tang-server.json') }}"
      register: result


---
- name: Create OpenShift cluster with high availability mode
  hosts: localhost
  tasks:
    - name: Create a new OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: present
        name: "ha-cluster"
        base_dns_domain: "example.com"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        high_availability_mode: "Full"
      register: result

---
- name: Delete an OpenShift cluster
  hosts: localhost
  tasks:
    - name: Delete the OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: absent
        cluster_id: "cluster-id-to-delete"
      register: result

---
- name: Create OpenShift cluster with API VIPs
  hosts: localhost
  tasks:
    - name: Create a new OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: present
        name: "vip-cluster"
        base_dns_domain: "example.com"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        api_vips:
          - cluster_id: "cluster-id-123"
            ip: "192.168.1.100"
            verification: "succeeded"
      register: result

---
- name: Create OpenShift cluster with ignition endpoint
  hosts: localhost
  tasks:
    - name: Create a new OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: present
        name: "ignition-cluster"
        base_dns_domain: "example.com"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        ignition_endpoint:
          ca_certificate: "{{ lookup('file', 'path/to/ca-cert.pem') }}"
          url: "https://ignition-endpoint.example.com"
      register: result

---
- name: Comprehensive OpenShift cluster creation
  hosts: localhost
  tasks:
    - name: Create a new OpenShift cluster
      justinbatchelor.redhat_assisted_installer.cluster:
        state: present
        name: "comprehensive-cluster"
        base_dns_domain: "example.com"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_public_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        cpu_architecture: "x86_64"
        http_proxy: "http://proxy.example.com:8080"
        https_proxy: "http://proxy.example.com:8443"
        cluster_networks:
          - cidr: "10.128.0.0/14"
            host_prefix: 23
        disk_encryption:
          enable_on: "all"
          mode: "tang"
          tang_server: "{{ lookup('file', 'path/to/tang-server.json') }}"
        high_availability_mode: "Full"
        api_vips:
          - cluster_id: "cluster-id-123"
            ip: "192.168.1.100"
            verification: "succeeded"
        ignition_endpoint:
          ca_certificate: "{{ lookup('file', 'path/to/ca-cert.pem') }}"
          url: "https://ignition-endpoint.example.com"
      register: result

```


## Parameters

    additional_ntp_sources:
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

