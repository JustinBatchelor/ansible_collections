# justinbatchelor.redhat_assisted_installer.infra_env


Ansible module to implement the POST / PATCH / DELETE operations for infrastructure environment objects, documented by the [Red Hat Assisted Installer API](https://developers.redhat.com/api-catalog/api/assisted-install-service#content-operations)

## Examples

```
---
- name: Create a basic infrastructure environment
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        name: "basic-infra-env"
        openshift_version: "4.8"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
      
---
- name: Create infrastructure environment with CPU architecture
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        name: "cpu-arch-infra-env"
        openshift_version: "4.8"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        cpu_architecture: "x86_64"
      
---
- name: Create infrastructure environment with proxy
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        name: "proxy-infra-env"
        openshift_version: "4.8"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        proxy:
          http_proxy: "http://proxy.example.com:8080"
          https_proxy: "http://proxy.example.com:8443"
      
---
- name: Create infrastructure environment with kernel arguments
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        name: "kernel-args-infra-env"
        openshift_version: "4.8"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        kernel_arguments:
          - operation: "append"
            value: "console=ttyS0"

---
- name: Create infrastructure environment with static network config
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        name: "static-network-infra-env"
        openshift_version: "4.8"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        static_network_config:
          - mac_interface_map:
              - logical_nic_name: "eth0"
                mac_address: "52:54:00:12:34:56"
            network_yaml: |- ## <----- If passing as var make sure to chomp all trailing whitespace
              interfaces:
                - name: eth0
                  type: ethernet
                  state: up
                  mac-address: 00:1A:2B:3C:4D:5E
                  ipv4:
                    enabled: true
                    address:
                      - ip: 192.168.1.10
                        prefix-length: 24
                    dhcp: false
                  ipv6:
                    enabled: false
              dns-resolver:
                config:
                  server:
                    - 8.8.8.8
                    - 8.8.4.4

---
## Patch operation will work with either infra_env_id or name
- name: Patch an existing infrastructure environment's ntp sources
  hosts: localhost
  tasks:
    - name: Update the infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        infra_env_id: "static-network-infra-env"
        openshift_version: "4.9"
        additional_ntp_sources:
          - "ntp1.example.com"
          - "ntp2.example.com"
      
---
- name: Delete an infrastructure environment by id
  hosts: localhost
  tasks:
    - name: Delete the infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: absent
        infra_env_id: "infra-env-id-to-delete"
      

- name: Delete an infrastructure environment by name
  hosts: localhost
  tasks:
    - name: Delete the infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: absent
        name: "infra-env-id-to-delete"

---
- name: Create infrastructure environment with additional trust bundle by file
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        name: "trust-bundle-infra-env"
        openshift_version: "4.8"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        additional_trust_bundle: "{{ lookup('file', 'path/to/trust-bundle.pem') }}"

---
- name: Create infrastructure environment with additional trust bundle by variable
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        name: "trust-bundle-infra-env"
        openshift_version: "4.8"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        additional_trust_bundle: |- ## <----- If passing as var make sure to chomp all trailing whitespace
          -----BEGIN CERTIFICATE-----
          MIIDXTCCAkWgAwIBAgIEb7RSdzANBgkqhkiG9w0BAQsFADBvMQswCQYDVQQGEwJV
          ...
          -----END CERTIFICATE-----

---
- name: Create infrastructure environment and associate with cluster ID
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        name: "cluster-id-infra-env"
        openshift_version: "4.8"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        cluster_id: "cluster-id-123"

---
- name: Comprehensive infrastructure environment creation
  hosts: localhost
  tasks:
    - name: Create a new infrastructure environment
      justinbatchelor.redhat_assisted_installer.infra_env:
        state: present
        name: "comprehensive-infra-env"
        openshift_version: "4.8"
        pull_secret: "{{ lookup('file', 'path/to/pull-secret.txt') }}"
        ssh_authorized_key: "{{ lookup('file', 'path/to/ssh-key.pub') }}"
        cpu_architecture: "x86_64"
        image_type: "minimal-iso"
        kernel_arguments:
          - operation: "append"
            value: "console=ttyS0"
        static_network_config:
          - mac_interface_map:
              - logical_nic_name: "eth0"
                mac_address: "00:1A:2B:3C:4D:5E"
            network_yaml: "{{ lookup('file', 'path/to/network.yaml') }}"
        proxy:
          http_proxy: "http://proxy.example.com:8080"
          https_proxy: "http://proxy.example.com:8443"
        additional_ntp_sources:
          - "ntp1.example.com"
          - "ntp2.example.com"
        additional_trust_bundle: "{{ lookup('file', 'path/to/trust-bundle.pem') }}"
        cluster_id: "cluster-id-123"
      register: result

```

## Parameters

    additional_ntp_sources:
        description: List of additional NTP sources.
        required: false
        type: list

    additional_trust_bundle:
        description: Additional trust bundle in PEM format.
        required: false
        type: str
    **NOTE** PEM formatting can be tricky, make sure to check the examples for more information on the different ways you can pass arguments that have special formatting rules

    cluster_id:
        description: Cluster ID associated with the infrastructure environment.
        required: false
        type: str

    cpu_architecture:
        description: CPU architecture of the infrastructure environment.
        required: false
        type: str
        choices: ['x86_64', 'aarch64', 'arm64', 'ppc64le', 's390x']

    ignition_config_override:
        description: Ignition config override.
        required: false
        type: str

    image_type:
        description: Type of image to create.
        required: false
        type: str
        choices: ["full-iso", "minimal-iso"]

    infra_env_id:
        description: ID of the infrastructure environment.
        required: false
        type: str

    kernel_arguments:
        description: Kernel arguments for the infrastructure environment.
        required: false
        type: list
        elements: dict
        suboptions:
        operation:
            description: Operation to perform on the kernel arguments.
            required: true
            type: str
            choices: ["append", "replace", "delete"]
        value:
            description: Kernel argument value.
            required: true
            type: str

    name:
        description: Name of the infrastructure environment.
        required: false
        type: str
    offline_token:
        description: Offline token for authentication.
        required: false
        type: str
        no_log: true

    openshift_version:
        description: OpenShift version to use.
        required: false
        type: str

    proxy:
        description: Proxy configuration.
        required: false
        type: dict
        suboptions:
        http_proxy:
            description: HTTP proxy URL.
            required: false
            type: str
        https_proxy:
            description: HTTPS proxy URL.
            required: false
            type: str
        no_proxy:
            description: Comma-separated list of hosts that do not use the proxy.
            required: false
            type: str

    pull_secret:
        description: Pull secret for accessing Red Hat's image registry.
        required: false
        type: str
        no_log: true

    ssh_authorized_key:
        description: SSH public key to authorize.
        required: false
        type: str

    state:
        description: Desired state of the infrastructure environment.
        required: true
        type: str
        choices: ['present', 'absent']

    static_network_config:
        description: Static network configuration.
        required: false
        type: list
        elements: dict
        suboptions:
        mac_interface_map:
            description: Mapping of MAC addresses to network interfaces.
            required: true
            type: list
            elements: dict
            suboptions:
            logical_nic_name:
                description: Logical name of the network interface.
                required: true
                type: str
            mac_address:
                description: MAC address of the network interface.
                required: true
                type: str
        network_yaml:
            description: Network configuration in YAML format.
            required: true
            type: str
