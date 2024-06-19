import re

from ..module_utils.schema.cluster import *
from ..module_utils.schema.infra_env import *

def filter_dict_by_keys(data, valid_keys):
    """
    Filters a dictionary, removing any keys not in the valid_keys list.

    Parameters:
    data (dict): The dictionary to filter.
    valid_keys (list): The list of valid keys.

    Returns:
    dict: A new dictionary with only the valid keys.
    """
    return {key: value for key, value in data.items() if key in valid_keys}


def is_valid_http_proxy(proxy: str) -> bool:
    """
    Validates if the given string is a valid HTTP proxy.

    Args:
        proxy (str): The string to be validated.

    Returns:
        bool: True if the string matches the HTTP proxy pattern, False otherwise.
    """
    pattern = r'^http:\/\/(?:[a-zA-Z0-9\-_]+(?:\:[a-zA-Z0-9\-_]+)?@)?[a-zA-Z0-9\.\-]+(?:\:[0-9]{1,5})?$'
    
    return bool(re.match(pattern, proxy))


def is_valid_cidr(ip_address: str) -> bool:
    """
    Validates if the given string is a valid IPv4 or IPv6 address with a subnet mask using a regular expression.

    Args:
        ip_address (str): The string to be validated.

    Returns:
        bool: True if the string matches the IPv4 or IPv6 pattern with subnet mask, False otherwise.
    """
    # Regular expression pattern to match either an IPv4 or IPv6 address with subnet mask
    pattern = r'^(?:(?:(?:[0-9]{1,3}\.){3}[0-9]{1,3}\/(?:(?:[0-9])|(?:[1-2][0-9])|(?:3[0-2])))|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,})/(?:(?:[0-9])|(?:[1-9][0-9])|(?:1[0-1][0-9])|(?:12[0-8])))$'
    
    # Return the result of the match as a boolean
    return bool(re.match(pattern, ip_address))

def is_valid_kernel_value(kernel_value) -> bool:
    pattern = r'^(?:(?:[^\s\t\n\r"]+)|(?:"[^"]*"))+$'
    return bool(re.match(pattern, kernel_value))

    
def is_valid_openshift_version(version) -> bool:
    """
    Validate if the given value is a valid OpenShift version.

    Parameters:
    version (str): The OpenShift version to validate.

    Returns:
    bool: True if valid, False otherwise.
    """
    pattern = re.compile(r'^\d+\.\d+$')
    return bool(pattern.match(version))

    
def is_valid_ip(ip_address: str) -> bool:
    """
    Validates if the given string is a valid IPv4 or IPv6 address using a regular expression.

    Args:
        ip_address (str): The string to be validated.

    Returns:
        bool: True if the string matches the IPv4 or IPv6 pattern, False otherwise.
    """
    # Regular expression pattern to match either an IPv4 or IPv6 address
    pattern = r'^(?:(?:(?:[0-9]{1,3}\.){3}[0-9]{1,3})|(?:(?:[0-9a-fA-F]*:[0-9a-fA-F]*){2,}))?$'
    
    # Return the result of the match as a boolean
    return bool(re.match(pattern, ip_address))


def is_valid_base_domain(domain) -> bool:
    """
    Validate if the given string is a valid base domain (e.g., example.com).

    Parameters:
    domain (str): The base domain to validate.

    Returns:
    bool: True if valid, False otherwise.
    """
    pattern = re.compile(
        r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.'          # Domain
        r'[A-Za-z]{2,63}$'                           # Top-level domain (TLD)
    )
    return bool(pattern.match(domain))

def create_additional_ntp_sources_from_params(module_params: list) -> str:
    if module_params is None:
        return None
    additional_ntp_sources = ""
    for source in module_params:
        additional_ntp_sources += (source + ',')
    return additional_ntp_sources[:-1]

def create_api_vips_from_module_params(module_params: list) -> list[APIVIP]:
    if module_params is None:
        return None
    api_vips = []
    for api_vip in module_params:
        api_vips.append(APIVIP(
            cluster_id=api_vip['cluster_id'] if "cluster_id" in api_vip else None,
            ip=api_vip['ip'],
            verification=api_vip['verification'] if "verification" in api_vip else None,
        ))
    return api_vips

def create_cluster_networks_from_module_params(module_params: list) -> list[ClusterNetwork]:
    if module_params is None:
        return None
    cluster_networks = []
    for cluster_network in module_params:
        cluster_networks.append(ClusterNetwork(
            cidr=cluster_network['cidr'],
            cluster_id=cluster_network['cluster_id'] if "cluster_id" in cluster_network else None,
            host_prefix=cluster_network['host_prefix'] if "host_prefix" in cluster_network else None,
        ))
    return cluster_networks
        
def create_disk_encryption_from_module_params(module_params: dict) -> DiskEncryption:
    if module_params is None:
        return None
    return DiskEncryption(
        enable_on=module_params['enable_on'],
        mode=module_params['mode'],
        tang_server=module_params['tang_server'] if "tang_server" in module_params else None,
    )

def create_disk_encryption_from_module_params(module_params: dict) -> DiskEncryption:
    if module_params is None:
        return None
    return DiskEncryption(
        enable_on=module_params['enable_on'],
        mode=module_params['mode'],
        tang_server=module_params['tang_server'],
    )

def create_ignition_endpoint_from_module_params(module_params: dict) -> IgnitionEndpoint:
    if module_params is None:
        return None
    return IgnitionEndpoint(
        ca_certificate=module_params['ca_certificate'],
        url=module_params['url'],
    )

def create_ingress_vips_from_module_params(module_params: list) -> list[IngressVIP]:
    if module_params is None:
        return None
    ingress_vips = []
    for ingress_vip in module_params:
        ingress_vips.append(IngressVIP(
            ip=ingress_vip['ip'],
            cluster_id=ingress_vip['cluster_id'] if "cluster_id" in ingress_vip else None,
            verification=ingress_vip['verification'] if "verification" in ingress_vip else None,
        ))
    return ingress_vips


def create_machine_networks_from_module_params(module_params: list) -> list[MachineNetwork]:
    if module_params is None:
        return None
    machine_networks = []
    for machine_network in module_params:
        machine_networks.append(MachineNetwork(
            cidr=machine_network['cidr'],
            cluster_id=machine_network['cluster_id'] if "cluster_id" in machine_network else None,
        ))
    return machine_networks

def create_olm_operators_from_module_params(module_params: list) -> list[OLMOperator]:
    if module_params is None:
        return None
    olm_operators = []
    for olm_operator in module_params:
        olm_operators.append(OLMOperator(
            name=olm_operator['name'],
            properties=olm_operator['properties'] if "properties" in olm_operator else None,
        ))
    return olm_operators

def create_platform_from_module_params(module_params: dict) -> Platform:
    if module_params is None:
        return None
    platform_external = PlatformExternal(
        cloud_controller_manager=module_params['external']['cloud_controller_manager'],
        platform_name=module_params['external']['platform_name'],
        )
    return Platform(
        external=platform_external,
        type=module_params['type']
    )

def create_service_networks_from_module_params(module_params: list) -> list[ServiceNetwork]:
    if module_params is None:
        return None
    service_networks = []
    for service_network in module_params:
        service_networks.append(ServiceNetwork(
            cidr=service_network['cidr'],
            cluster_id=service_network['cluster_id'] if "cluster_id" in service_network else None,
        ))
    return service_networks


def create_proxy_from_module_params(module_params: dict) -> Proxy:
    if module_params is None or (module_params.get("http_proxy", None) is None and module_params.get("https_proxy") is None and module_params.get("no_proxy") is None):
        return None
    return Proxy(
        http_proxy=module_params['http_proxy'],
        https_proxy=module_params['https_proxy'],
        no_proxy=module_params['no_proxy'],
    )

def create_kernel_arguments_from_module_params(module_params: list) -> list[KernelArgument]:
    if module_params is None:
        return None
    kernel_arguments = []
    for kernel_argument in module_params:
        kernel_arguments.append(KernelArgument(
            operation=kernel_argument['operation'],
            value=kernel_argument['value'],
        ))
    return kernel_arguments


def create_static_network_config_from_module_params(module_params: list) -> list[StaticNetworkConfig]:
    if module_params is None:
        return None
    network_configs = []
    # for each static network config
    for network_config in module_params:
        # create an array of mac_interfaces
        mac_interfaces = []
        for mac_interface in network_config['mac_interface_map']:
            mac_interfaces.append(MacInterfaceMap(
                logical_nic_name=mac_interface['logical_nic_name'],
                mac_address=mac_interface['mac_address'],
            ))

        network_configs.append(StaticNetworkConfig(
            mac_interface_map=mac_interfaces,
            network_yaml=network_config['network_yaml'],
        ))
    return network_configs
    