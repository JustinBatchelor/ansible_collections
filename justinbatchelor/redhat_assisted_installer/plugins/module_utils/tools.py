import re, jmespath, base64, textwrap, json
from ..module_utils.schema.cluster import *
from ..module_utils.schema.infra_env import *
from collections.abc import Mapping, Iterable


def is_base64(base64_content: str):
    # Define the regular expression for valid base64 characters
    base64_pattern = re.compile(r'^[A-Za-z0-9+/=\n]+$')
    
    # Validate the base64 content
    if not base64_pattern.match(base64_content):
        return False
    
    return True

def is_pem_format(cert_string: str):
    # Define the PEM format header and footer
    pem_header = "-----BEGIN CERTIFICATE-----"
    pem_footer = "-----END CERTIFICATE-----"
    
    # Check if the certificate contains the header and footer
    if not cert_string.startswith(pem_header):
        return False
    if not cert_string.endswith(pem_footer):
        return False
    
    # Extract the base64 encoded content between the header and footer
    base64_content = cert_string[len(pem_header):-len(pem_footer)].strip()

    return is_base64(base64_content)

def deep_equal(val1, val2):
    """
    Recursively check for equality between two complex data structures.
    """
    if isinstance(val1, Mapping) and isinstance(val2, Mapping):
        return (val1.keys() == val2.keys() and 
                all(deep_equal(val1[k], val2[k]) for k in val1))
    elif isinstance(val1, Iterable) and isinstance(val2, Iterable) and not isinstance(val1, (str, bytes)):
        return all(deep_equal(v1, v2) for v1, v2 in zip(val1, val2))
    else:
        return val1 == val2

def remove_matching_pairs(dict1, dict2):
    """
    Removes key-value pairs from dict1 if they match in both dictionaries, handling complex structures.
    
    Args:
    dict1 (dict): The first dictionary to be modified.
    dict2 (dict): The second dictionary to compare against.

    Returns:
    dict: The modified dict1.
    """
    keys_to_remove = [key for key in dict1 if key in dict2 and deep_equal(dict1[key], dict2[key])]

    for key in keys_to_remove:
        del dict1[key]

    return dict1

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


def jmespath_name_validator(name: str, data: list):
    """
    Filters lists of objects and returns a list of objects where []data.name == name
    Parameters:
    name (str): Name to filter json list 
    data (list): The list of objects returned from api request

    Returns:
    dict: A new dictionary with only the valid keys.
    """
    # JMESPath expression to filter objects by name
    expression = f"[?name=='{name}']"
    # Search the API response using the JMESPath expression
    return jmespath.search(expression, data)

def jmespath_id_validator(id: str, data: list):
    """
    Filters lists of objects and returns a list of objects where []data.id == id

    Parameters:
    id (str): The dictionary to filter.
    data (list): The list of objects returned from api request

    Returns:
    dict: A new dictionary with only the valid keys.
    """
    # JMESPath expression to filter objects by id
    expression = f"[?id=='{id}']"
    # Search the API response using the JMESPath expression
    return jmespath.search(expression, data)


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

def create_api_vips_from_module_params(module_params: list[dict]) -> list[APIVIP]:
    if module_params is None:
        return None
    api_vips = []
    for api_vip in module_params:
        api_vips.append(APIVIP(
            cluster_id=api_vip.get('cluster_id', None),
            ip=api_vip.get('ip', None),
            verification=api_vip.get('verification', None),
        ))
    return api_vips

def create_cluster_networks_from_module_params(module_params: list[dict]) -> list[ClusterNetwork]:
    if module_params is None:
        return None
    cluster_networks = []
    for cluster_network in module_params:
        cluster_networks.append(ClusterNetwork(
            cidr=cluster_network.get('cidr', None),
            cluster_id=cluster_network.get('cluster_id', None),
            host_prefix=cluster_network.get('host_prefix', None),
        ))
    return cluster_networks
        
def create_disk_encryption_from_module_params(module_params: dict) -> DiskEncryption:
    if module_params is None:
        return None
    return DiskEncryption(
        enable_on=module_params.get('enable_on', None),
        mode=module_params.get('mode', None),
        tang_server=module_params.get('tang_server', None),
    )

def create_disk_encryption_from_module_params(module_params: dict) -> DiskEncryption:
    if module_params is None:
        return None
    return DiskEncryption(
        enable_on=module_params.get('enable_on', None),
        mode=module_params.get('mode', None),
        tang_server=module_params.get('tang_server', None),
    )

def create_ignition_endpoint_from_module_params(module_params: dict) -> IgnitionEndpoint:
    if module_params is None:
        return None
    return IgnitionEndpoint(
        ca_certificate=module_params.get('ca_certificate', None),
        url=module_params.get('url', None),
    )

def create_ingress_vips_from_module_params(module_params: list[dict]) -> list[IngressVIP]:
    if module_params is None:
        return None
    ingress_vips = []
    for ingress_vip in module_params:
        ingress_vips.append(IngressVIP(
            ip=ingress_vip.get('ip', None),
            cluster_id=ingress_vip.get('cluster_id', None),
            verification=ingress_vip.get('verification', None),
        ))
    return ingress_vips


def create_machine_networks_from_module_params(module_params: list[dict]) -> list[MachineNetwork]:
    if module_params is None:
        return None
    machine_networks = []
    for machine_network in module_params:
        machine_networks.append(MachineNetwork(
            cidr=machine_network.get('cidr', None),
            cluster_id=machine_network.get('cluster_id', None),
        ))
    return machine_networks

def create_olm_operators_from_module_params(module_params: list[dict]) -> list[OLMOperator]:
    if module_params is None:
        return None
    olm_operators = []
    for olm_operator in module_params:
        olm_operators.append(OLMOperator(
            name=olm_operator.get('name', None),
            properties=olm_operator.get("properties", None),
        ))
    return olm_operators

def create_platform_external_from_module_params(module_params: dict) -> PlatformExternal:
    if module_params is None:
        return None

    return PlatformExternal(
        cloud_controller_manager=module_params.get('cloud_controller_manager', None),
        platform_name=module_params.get("platform_name", None),
        )

def create_platform_from_module_params(module_params: dict) -> Platform:
    if module_params is None:
        return None
    
    return Platform(
        external=create_platform_external_from_module_params(module_params.get("external", None)),
        type=module_params.get("type", None),
    )

def create_service_networks_from_module_params(module_params: list[dict]) -> list[ServiceNetwork]:
    if module_params is None:
        return None
    service_networks = []
    for service_network in module_params:
        service_networks.append(ServiceNetwork(
            cidr=service_network.get('cidr', None),
            cluster_id=service_network.get('cluster_id', None),
        ))
    return service_networks


def create_proxy_from_module_params(module_params: dict) -> Proxy:
    if module_params is None or (module_params.get("http_proxy", None) is None and module_params.get("https_proxy") is None and module_params.get("no_proxy") is None):
        return None
    return Proxy(
        http_proxy=module_params.get('http_proxy', None),
        https_proxy=module_params.get('https_proxy', None),
        no_proxy=module_params.get('no_proxy', None),
    )

def create_kernel_arguments_from_module_params(module_params: list[dict]) -> list[KernelArgument]:
    if module_params is None:
        return None
    kernel_arguments = []
    for kernel_argument in module_params:
        kernel_arguments.append(KernelArgument(
            operation=kernel_argument.get('operation', None),
            value=kernel_argument.get('value', None),
        ))
    return kernel_arguments


def create_static_network_config_from_module_params(module_params: list[dict]) -> list[StaticNetworkConfig]:
    if module_params is None:
        return None
    network_configs = []
    # for each static network config
    for network_config in module_params:
        # create an array of mac_interfaces
        mac_interfaces = []
        for mac_interface in network_config.get('mac_interface_map', None):
            mac_interfaces.append(MacInterfaceMap(
                logical_nic_name=mac_interface.get('logical_nic_name', None),
                mac_address=mac_interface.get('mac_address', None),
            ))

        network_configs.append(StaticNetworkConfig(
            mac_interface_map=mac_interfaces,
            network_yaml=network_config.get('network_yaml', None),
        ))
    return network_configs
    


