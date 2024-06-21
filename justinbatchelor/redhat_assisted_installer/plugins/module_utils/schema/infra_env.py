import os, yaml

from .schema import APIObject


"""
{
  "additional_ntp_sources": {
    "type": "string",
    "description": "A comma-separated list of NTP sources (name or IP) going to be added to all the hosts."
  },
  "additional_trust_bundle": {
    "type": "string",
    "maxLength": 65535,
    "description": "PEM-encoded X.509 certificate bundle. Hosts discovered by this infra-env will trust the certificates in this bundle. Clusters formed from the hosts discovered by this infra-env will also trust the certificates in this bundle."
  },
  "cluster_id": {
    "type": "string",
    "format": "uuid",
    "description": "If set, all hosts that register will be associated with the specified cluster."
  },
  "cpu_architecture": {
    "type": "string",
    "default": "x86_64",
    "description": "The CPU architecture of the image (x86_64/arm64/etc).",
    "enum": ["x86_64", "aarch64", "arm64", "ppc64le", "s390x"]
  },
  "ignition_config_override": {
    "type": "string",
    "description": "JSON formatted string containing the user overrides for the initial ignition config."
  },
  "image_type": {
    "type": "string",
    "description": "Type of the image.",
    "enum": ["full-iso", "minimal-iso"]
  },
  "kernel_arguments": {
    "type": "array",
    "description": "List of kernel argument objects that define the operations and values to be applied.",
    "items": {
      "type": "object",
      "properties": {
        "description": {
          "type": "string",
          "description": "Pair of [operation, argument] specifying the argument and what operation should be applied on it."
        },
        "operation": {
          "type": "string",
          "description": "The operation to apply on the kernel argument.",
          "enum": ["append", "replace", "delete"]
        },
        "value": {
          "type": "string",
          "pattern": "^(?:(?:[^ \\t\\n\\r\"]+)|(?:\"[^\"]*\"))+?$",
          "description": "Kernel argument can have the form or =. The following examples should be supported: rd.net.timeout.carrier=60, isolcpus=1,2,10-20,100-2000:2/25, quiet. The parsing by the command line parser in linux kernel is much looser and this pattern follows it."
        }
      }
    }
  },
  "name": {
    "type": "string",
    "description": "Name of the infra-env."
  },
  "openshift_version": {
    "type": "string",
    "description": "Version of the OpenShift cluster (used to infer the RHCOS version - temporary until generic logic implemented)."
  },
  "proxy": {
    "type": "object",
    "properties": {
      "http_proxy": {
        "type": "string",
        "description": "A proxy URL to use for creating HTTP connections outside the cluster. http://<username>:<pswd>@<ip>:<port>"
      },
      "https_proxy": {
        "type": "string",
        "description": "A proxy URL to use for creating HTTPS connections outside the cluster. http://<username>:<pswd>@<ip>:<port>"
      },
      "no_proxy": {
        "type": "string",
        "description": "An \"*\" or a comma-separated list of destination domain names, domains, IP addresses, or other network CIDRs to exclude from proxying."
      }
    }
  },
  "pull_secret": {
    "type": "string",
    "description": "The pull secret obtained from Red Hat OpenShift Cluster Manager at console.redhat.com/openshift/install/pull-secret."
  },
  "ssh_authorized_key": {
    "type": "string",
    "description": "SSH public key for debugging the installation."
  },
  "static_network_config": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "mac_interface_map": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "logical_nic_name": {
                "type": "string",
                "description": "NIC name used in the yaml, which relates 1:1 to the MAC address."
              },
              "mac_address": {
                "type": "string",
                "pattern": "^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$",
                "description": "MAC address present on the host."
              }
            }
          }
        },
        "network_yaml": {
          "type": "string",
          "description": "YAML string that can be processed by nmstate."
        }
      }
    }
  }
}
"""


class Proxy(APIObject):
    def __init__(self, 
                 http_proxy: str = None,
                 https_proxy: str = None,
                 no_proxy: str = None,
                 ) -> None:
        super().__init__()

        if http_proxy is not None:
            self.params['http_proxy'] = http_proxy
        
        if https_proxy is not None:
            self.params['https_proxy'] = https_proxy

        if no_proxy is not None:
            self.params['no_proxy'] = no_proxy
        
class MacInterfaceMap(APIObject):
    def __init__(self,
                 logical_nic_name: str = None,
                 mac_address: str = None,
                 ) -> None:
        
        super().__init__()

        if logical_nic_name is not None:
            self.params['logical_nic_name'] = logical_nic_name
        
        if mac_address is not None:
            self.params['mac_address'] = mac_address

class StaticNetworkConfig(APIObject):
    def __init__(self, 
                 mac_interface_map: list[MacInterfaceMap] = None,
                 network_yaml: str = None,
                 ) -> None:
        
        super().__init__()

        if mac_interface_map is not None:
            maps = []
            for interface_map in mac_interface_map:
                maps.append(interface_map.create_params())
            self.params['mac_interface_map'] = maps

        if network_yaml is not None:
            # Convert the escaped YAML string into a proper YAML string
            proper_yaml_str = self.convert_escaped_yaml_to_proper_yaml(network_yaml)
            self.params['network_yaml'] = proper_yaml_str

    @staticmethod
    def convert_escaped_yaml_to_proper_yaml(escaped_yaml_str: str) -> str:
        """
        Converts an escaped YAML string into a properly formatted YAML string.

        Args:
            escaped_yaml_str (str): The escaped YAML string.

        Returns:
            str: The properly formatted YAML string.
        """
        # Replace escaped newlines with actual newlines and remove unnecessary escape characters
        proper_yaml_str = escaped_yaml_str.replace('\\n', '\n').replace('\\', '')

        # Load the YAML string to ensure it's valid and then dump it back to a string
        yaml_data = yaml.safe_load(proper_yaml_str)
        proper_yaml_str = yaml.dump(yaml_data, default_flow_style=False)

        return proper_yaml_str

class KernelArgument(APIObject):
    def __init__(self, 
                 operation: str = None,
                 value: str = None,
                 ) -> None:
        
        super().__init__()

        if operation is not None:
            self.params['operation'] = operation

        if value is not None:
            self.params['value'] = value


class InfraEnv(APIObject):
    def __init__(self,
                 infra_env_id: str = None,
                 additional_ntp_sources: str = None, 
                 additional_trust_bundle: str = None, 
                 cluster_id: str = None,
                 cpu_architecture: str = None,
                 ignition_config_override: str = None,
                 image_type: str = None,
                 kernel_arguments: list[KernelArgument] = None,
                 name: str = None,
                 openshift_version: str = None,
                 proxy: Proxy = None,
                 pull_secret: str = os.environ.get("REDHAT_PULL_SECRET"),
                 ssh_authorized_key: str = None,
                 static_network_config: list[StaticNetworkConfig] = None,
                 ):
        
        super().__init__()

        if name is not None:
            self.params['name'] = name

        if infra_env_id is not None:
            self.params['infra_env_id'] = infra_env_id

        if openshift_version is not None:
            self.params['openshift_version'] = openshift_version

        if cluster_id is not None:
            self.params['cluster_id'] = cluster_id

        if pull_secret is not None:
            self.params['pull_secret'] = pull_secret

        if additional_ntp_sources is not None:
            self.params['additional_ntp_sources'] = additional_ntp_sources

        if additional_trust_bundle is not None:
            self.params['additional_trust_bundle'] = additional_trust_bundle

        if image_type is not None and (image_type):
            self.params['image_type'] = image_type

        if cpu_architecture is not None:
            self.params['cpu_architecture'] = cpu_architecture

        if ssh_authorized_key is not None :
            self.params['ssh_authorized_key'] = ssh_authorized_key

        if kernel_arguments is not None:
            arguments = []
            for kernel in kernel_arguments:  
              arguments.append(kernel.create_params())
            self.params['kernel_arguments'] = arguments

        if static_network_config is not None:
            network_configs = []
            for config in static_network_config:
                network_configs.append(config.create_params())
            self.params['static_network_config'] = network_configs

        if proxy is not None:
            self.params['proxy'] = proxy.create_params()

        if ignition_config_override is not None:
            self.params["ignition_config_override"] = ignition_config_override

    