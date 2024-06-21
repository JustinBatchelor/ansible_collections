import os

from .schema import APIObject

"""
{
  "additional_ntp_source": {
    "type": "string",
    "description": "A comma-separated list of NTP sources (name or IP) going to be added to all the hosts."
  },
  "api_vips": [
    {
      "description": "The virtual IPs used to reach the OpenShift cluster's API. Enter one IP address for single-stack clusters, or up to two for dual-stack clusters (at most one IP address per IP stack used). The order of stacks should be the same as order of subnets in Cluster Networks, Service Networks, and Machine Networks.",
      "api_vip": {
        "description": "The virtual IP used to reach the OpenShift cluster's API.",
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "The cluster that this VIP is associated with."
        },
        "ip": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3})|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,}))?$"
        },
        "verification": {
          "type": "string",
          "default": "unverified",
          "description": "VIP verification result.",
          "enum": ["unverified", "failed", "succeeded"]
        }
      }
    }
  ],
  "base_dns_domain": {
    "type": "string",
    "description": "Base domain of the cluster. All DNS records must be sub-domains of this base and include the cluster name."
  },
  "cluster_network_cidr": {
    "type": "string",
    "default": "10.128.0.0/14",
    "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$",
    "description": "IP address block from which Pod IPs are allocated. This block must not overlap with existing physical networks. These IP addresses are used for the Pod network, and if you need to access the Pods from an external network, configure load balancers and routers to manage the traffic."
  },
  "cluster_network_host_prefix": {
    "type": "integer",
    "default": 23,
    "maximum": 128,
    "minimum": 1,
    "description": "The subnet prefix length to assign to each individual node. For example, if clusterNetworkHostPrefix is set to 23, then each node is assigned a /23 subnet out of the given CIDR (clusterNetworkCIDR), which allows for 510 (2^(32 - 23) - 2) pod IP addresses. If you are required to provide access to nodes from an external network, configure load balancers and routers to manage the traffic."
  },
  "cluster_networks": [
    {
      "x-nullable": true,
      "description": "Cluster networks that are associated with this cluster.",
      "cluster_network": {
        "description": "A network from which Pod IPs are allocated. This block must not overlap with existing physical networks. These IP addresses are used for the Pod network, and if you need to access the Pods from an external network, configure load balancers and routers to manage the traffic.",
        "cidr": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$"
        },
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "The cluster that this network is associated with."
        },
        "host_prefix": {
          "type": "integer",
          "maximum": 128,
          "minimum": 1,
          "description": "The subnet prefix length to assign to each individual node. For example, if is set to 23, then each node is assigned a /23 subnet out of the given CIDR, which allows for 510 (2^(32 - 23) - 2) pod IP addresses."
        }
      }
    }
  ],
  "cpu_architecture": {
    "type": "string",
    "default": "x86_64",
    "description": "The CPU architecture of the image (x86_64/arm64/etc).",
    "enum": ["x86_64", "aarch64", "arm64", "ppc64le", "s390x", "multi"]
  },
  "disk_encryption": {
    "type": "object",
    "properties": {
      "enable_on": {
        "type": "string",
        "default": "none",
        "description": "Enable/disable disk encryption on master nodes, worker nodes, or all nodes.",
        "enum": ["none", "all", "masters", "workers"]
      },
      "mode": {
        "type": "string",
        "default": "tpmv2",
        "description": "The disk encryption mode to use.",
        "enum": ["tpmv2", "tang"]
      },
      "tang_servers": {
        "type": "string",
        "example": "[{\"url\":\"http://tang.example.com:7500\",\"thumbprint\":\"PLjNyRdGw03zlRoGjQYMahSZGu9\"}, {\"url\":\"http://tang.example.com:7501\",\"thumbprint\":\"PLjNyRdGw03zlRoGjQYMahSZGu8\"}]",
        "description": "JSON-formatted string containing additional information regarding tang's configuration"
      }
    }
  },
  "high_availability_mode": {
    "type": "string",
    "default": "Full",
    "description": "Guaranteed availability of the installed cluster. 'Full' installs a Highly-Available cluster over multiple master nodes whereas 'None' installs a full cluster over one node.",
    "enum": ["Full", "None"]
  },
  "http_proxy": {
    "type": "string",
    "description": "A proxy URL to use for creating HTTP connections outside the cluster. http://<username>:<pswd>@<ip>:<port>"
  },
  "https_proxy": {
    "type": "string",
    "description": "A proxy URL to use for creating HTTPS connections outside the cluster. http://<username>:<pswd>@<ip>:<port>"
  },
  "hyperthreading": {
    "type": "string",
    "default": "all",
    "description": "Enable/disable hyperthreading on master nodes, worker nodes, or all nodes.",
    "enum": ["masters", "workers", "none", "all"]
  },
  "ignition_endpoint": {
    "type": "object",
    "properties": {
      "description": {
        "type": "string",
        "description": "Explicit ignition endpoint overrides the default ignition endpoint."
      },
      "ca_certificate": {
        "type": "string",
        "description": "Base64 encoded CA certificate to be used when contacting the URL via https."
      },
      "url": {
        "type": "string",
        "description": "The URL for the ignition endpoint."
      }
    }
  },
  "ingress_vips": [
    {
      "description": "The virtual IPs used for cluster ingress traffic. Enter one IP address for single-stack clusters, or up to two for dual-stack clusters (at most one IP address per IP stack used). The order of stacks should be the same as order of subnets in Cluster Networks, Service Networks, and Machine Networks.",
      "ingress_vip": {
        "description": "The virtual IP used for cluster ingress traffic.",
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "The cluster that this VIP is associated with."
        },
        "ip": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3})|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,}))?$"
        },
        "verification": {
          "type": "string",
          "default": "unverified",
          "description": "VIP verification result.",
          "enum": ["unverified", "failed", "succeeded"]
        }
      }
    }
  ],
  "machine_networks": [
    {
      "x-nullable": true,
      "description": "Machine networks that are associated with this cluster.",
      "machine_network": {
        "description": "A network that all hosts belonging to the cluster should have an interface with IP address in. The VIPs (if exist) belong to this network.",
        "cidr": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$"
        },
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "The cluster that this network is associated with."
        }
      }
    }
  ],
  "name": {
    "type": "string",
    "maxLength": 54,
    "minLength": 1,
    "description": "Name of the OpenShift cluster."
  },
  "network_type": {
    "type": "string",
    "description": "The desired network type used.",
    "enum": ["OpenShiftSDN", "OVNKubernetes"]
  },
  "no_proxy": {
    "type": "string",
    "description": "An \"*\" or a comma-separated list of destination domain names, domains, IP addresses, or other network CIDRs to exclude from proxying."
  },
  "ocp_release_image": {
    "type": "string",
    "description": "OpenShift release image URI."
  },
  "olm_operators": [
    {
      "name": {
        "type": "string",
        "description": "List of OLM operators to be installed."
      },
      "properties": {
        "type": "string",
        "description": "Blob of operator-dependent parameters that are required for installation."
      }
    }
  ],
  "openshift_version": {
    "type": "string",
    "description": "Version of the OpenShift cluster."
  },
  "platform": {
    "type": "object",
    "description": "The configuration for the specific platform upon which to perform the installation.",
    "properties": {
      "external": {
        "type": "object",
        "description": "Configuration used when installing with an external platform type.",
        "properties": {
          "cloud_controller_manager": {
            "type": "string",
            "description": "When set to external, this property will enable an external cloud provider.",
            "enum": ["", "External"]
          },
          "platform_name": {
            "type": "string",
            "minLength": 1,
            "description": "Holds the arbitrary string representing the infrastructure provider name."
          }
        }
      },
      "type": {
        "type": "string",
        "enum": ["baremetal", "nutanix", "vsphere", "none", "external"],
        "description": "Type of platform."
      }
    }
  },
  "pull_secret": {
    "type": "string",
    "description": "The pull secret obtained from Red Hat OpenShift Cluster Manager at console.redhat.com/openshift/install/pull-secret."
  },
  "schedulable_masters": {
    "type": "boolean",
    "default": false,
    "description": "Schedule workloads on masters"
  },
  "service_network_cidr": {
    "type": "string",
    "default": "172.30.0.0/16",
    "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$",
    "description": "The IP address pool to use for service IP addresses. You can enter only one IP address pool. If you need to access the services from an external network, configure load balancers and routers to manage the traffic."
  },
  "service_networks": [
    {
      "x-nullable": true,
      "description": "Service networks that are associated with this cluster.",
      "service_network": {
        "description": "IP address block for service IP blocks.",
        "cidr": {
          "type": "string",
          "pattern": "^(?:(?:(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\/((?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})\\/((?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$"
        },
        "cluster_id": {
          "type": "string",
          "format": "uuid",
          "description": "A network to use for service IP addresses. If you need to access the services from an external network, configure load balancers and routers to manage the traffic."
        }
      }
    }
  ],
  "ssh_public_key": {
    "type": "string",
    "description": "SSH public key for debugging OpenShift nodes."
  },
  "tags": {
    "type": "string",
    "description": "A comma-separated list of tags that are associated to the cluster."
  },
  "user_managed_networking": {
    "type": "boolean",
    "default": false,
    "description": "(DEPRECATED) Indicate if the networking is managed by the user."
  },
  "vip_dhcp_allocation": {
    "type": "boolean",
    "default": false,
    "description": "Indicate if virtual IP DHCP allocation mode is enabled."
  }
}

"""

class APIVIP(APIObject):
    def __init__(self,
                 cluster_id: str = None,
                 ip: str = None,
                 verification: str = None,
                 ) -> None:
        
        super().__init__()

        if cluster_id is not None:
            self.params['cluster_id'] = cluster_id

        if ip is not None:
            self.params['ip'] = ip
        
        if verification is not None:
            self.params['verification'] = verification

class ClusterNetwork(APIObject):
    def __init__(self,
                 cidr: str = None,
                 cluster_id: str = None,
                 host_prefix: int = None,
                 ) -> None:
        super().__init__()
        
        if cidr is not None:
            self.params['cidr'] = cidr

        if cluster_id is not None:
            self.params["cluster_id"] = cluster_id

        if host_prefix is not None:
            self.params['host_prefix'] = host_prefix


class DiskEncryption(APIObject):
    def __init__(self,
                 enable_on: str = None,
                 mode: str = None,
                 tang_server: str = None,
                 ) -> None:
        super().__init__()

        if enable_on is not None:
            self.params['enable_on'] = enable_on

        if mode is not None:
            self.params['mode'] = mode

        if tang_server is not None:
            self.params['tang_servers'] = tang_server

class IgnitionEndpoint(APIObject):
    def __init__(self,
                 ca_certificate: str = None,
                 url: str = None,
                 ) -> None:
        super().__init__()

        if ca_certificate is not None:
            self.params["ca_certificate"] = ca_certificate

        if url is not None:
            self.params["url"] = url


class IngressVIP(APIObject):
    def __init__(self,
                 cluster_id: str = None,
                 ip: str = None,
                 verification: str = None,
                 ) -> None:
        super().__init__()
        
        if cluster_id is not None:
            self.params['cluster_id'] = cluster_id

        if ip is not None:
            self.params['ip'] = ip

        if verification is not None:
            self.params['verification'] = verification

class MachineNetwork(APIObject):
    def __init__(self,
                 cidr: str = None,
                 cluster_id: str = None,
                 ) -> None:
        super().__init__()

        if cidr is not None:
            self.params['cidr'] = cidr

        if cluster_id is not None:
            self.params['cluster_id'] = cluster_id

class OLMOperator(APIObject):
    def __init__(self,
                 name: str = None,
                 properties: str = None,
                 ) -> None:
        super().__init__()

        if name is not None:
            self.params['name'] = name

        if properties is not None:
            self.params['properties'] = properties

class PlatformExternal(APIObject):
    def __init__(self,
                 cloud_controller_manager: str = None,
                 platform_name: str = None,
                 ) -> None:
        super().__init__()

        if cloud_controller_manager is not None:
            self.params['cloud_controller_manager'] = cloud_controller_manager

        if platform_name is not None:
            self.params['platform_name'] = platform_name

class Platform(APIObject):
    def __init__(self,
                 external: PlatformExternal = None,
                 type: str = None,
                 ) -> None:
        super().__init__()

        if external is not None:
            self.params['external'] = external.create_params()

        if type is not None:
            self.params['type'] = type

class ServiceNetwork(APIObject):
    def __init__(self,
                 cidr: str = None,
                 cluster_id: str = None, 
                ) -> None:
        super().__init__()

        if cidr is not None:
            self.params['cidr'] = cidr
        
        if cluster_id is not None:
            self.params['cluster_id'] = cluster_id

class Cluster(APIObject):
    def __init__(self, 
                 additional_ntp_sources: str = None,
                 api_vips: list[APIVIP] = None,
                 base_dns_domain: str = None,
                 cluster_networks: list[ClusterNetwork] = None,
                 cpu_architecture: str = None,
                 disk_encryption: DiskEncryption = None,     
                 high_availability_mode: str = None,
                 http_proxy: str = None,
                 https_proxy: str = None,
                 hyperthreading: str = None,
                 ignition_endpoint: IgnitionEndpoint = None,
                 ingress_vips: list[IngressVIP] = None,
                 machine_networks: list[MachineNetwork] = None,
                 name: str = None, 
                 network_type: str = None,
                 no_proxy: str = None,
                 ocp_release_image: str = None,
                 olm_operator: list[OLMOperator] = None,
                 openshift_version: str = None,
                 platform: Platform = None,
                 pull_secret: str = os.environ.get("REDHAT_PULL_SECRET"),
                 schedulable_masters: bool = None,
                 service_networks: list[ServiceNetwork] = None,
                 ssh_public_key: str = None,
                 tags: str = None,
                 user_managed_networking: bool = None,
                 vip_dhcp_allocation: bool = None,
                 cluster_id: str = None, 
                ):
        super().__init__()

        if additional_ntp_sources is not None:
            self.params['additional_ntp_source'] = additional_ntp_sources

        if api_vips is not None:
            vips = []
            for api_vip in api_vips:
                vips.append(api_vip.create_params())
            self.params['api_vips'] = vips

        if base_dns_domain is not None:
            self.params['base_dns_domain'] = base_dns_domain

        if cluster_id is not None:
            self.params['cluster_id'] = cluster_id

        if cluster_networks is not None:
            networks = []
            for network in cluster_networks:
                networks.append(network.create_params())
            self.params['cluster_networks'] = networks

        if cpu_architecture is not None:
            self.params['cpu_architecture'] = cpu_architecture

        if disk_encryption is not None:
            self.params['disk_encryption'] = disk_encryption.create_params()

        if high_availability_mode is not None:
            self.params['high_availability_mode'] = high_availability_mode

        if http_proxy is not None:
            self.params['http_proxy'] = http_proxy

        if https_proxy is not None:
            self.params['https_proxy'] = https_proxy

        if hyperthreading is not None:
            self.params['hyperthreading'] = hyperthreading

        if ignition_endpoint is not None:
            self.params['ignition_endpoint'] = ignition_endpoint

        if ingress_vips is not None:
            vips = []
            for vip in ingress_vips:
                vips.append(vip.create_params())
            self.params['ingress_vips'] = vips

        if machine_networks is not None:
            networks = []
            for network in machine_networks:
                networks.append(network.create_params())
            self.params['machine_networks'] = networks

        if name is not None:
            self.params['name'] = name

        if network_type is not None:
            self.params['network_type'] = network_type

        if no_proxy is not None:
            self.params['no_proxy'] = no_proxy
        
        if ocp_release_image is not None:
            self.params['ocp_release_image'] = ocp_release_image

        if olm_operator is not None:
            operators = []
            for operator in olm_operator:
                operators.append(operator.create_params())
            self.params['olm_operator'] = operators

        if openshift_version is not None:
            self.params['openshift_version'] = openshift_version

        if platform is not None:
            self.params['platform'] = platform.create_params()

        if pull_secret is not None:
            self.params['pull_secret'] = pull_secret

        if schedulable_masters is not None: 
            self.params['schedulable_masters'] = schedulable_masters

        if service_networks is not None:
            networks = []
            for network in service_networks:
                networks.append(network.create_params())
            self.params['service_networks'] = networks

        if ssh_public_key is not None:
            self.params['ssh_public_key'] = ssh_public_key

        if tags is not None:
            self.params['tags'] = tags

        if user_managed_networking is not None:
            self.params['user_managed_networking'] = user_managed_networking

        if vip_dhcp_allocation is not None:
            self.params['vip_dhcp_allocation'] = vip_dhcp_allocation


    def create_params(self):
        return {key: value for key, value in self.params.items() if value is not None}
    