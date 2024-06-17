import ipaddress, re

def is_valid_cidr(cidr):
    """
    Validate if the given string is a valid CIDR notation.

    Parameters:
    cidr (str): The CIDR notation to validate.

    Returns:
    bool: True if valid, False otherwise.
    """
    # Regular expression to match valid IPv4 addresses and prefix lengths
    cidr_regex = re.compile(
        r'^(([0-9]{1,3}\.){3}[0-9]{1,3})/([0-9]|[1-2][0-9]|3[0-2])$'
    )
    match = cidr_regex.match(cidr)
    
    if not match:
        return False
    # Validate each octet of the IP address
    ip_parts = match.group(1).split('.')
    for part in ip_parts:
        if not 0 <= int(part) <= 255:
            return False

    return True

    
def is_valid_openshift_version(version):
    """
    Validate if the given value is a valid OpenShift version.

    Parameters:
    version (str): The OpenShift version to validate.

    Returns:
    bool: True if valid, False otherwise.
    """
    pattern = re.compile(r'^\d+\.\d+$')
    return bool(pattern.match(version))

    
def is_valid_ip(ip):
    """
    Validate if the given string is a valid IP address (IPv4 or IPv6).

    Parameters:
    ip (str): The IP address to validate.

    Returns:
    bool: True if valid, False otherwise.
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_valid_base_domain(domain):
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

def is_valid_cpu_architecture(cpu_architecture):
    VALID_VALUES = ["x86_64", "aarch64", "arm64", "ppc64le", "s390x", "multi"]
    return cpu_architecture in VALID_VALUES

def is_valid_ha_mode(ha_mode):
    VALID_VALUES = ["None", "Full"]
    return ha_mode in VALID_VALUES

def is_valid_hyperthread(hyperthreading):
    VALID_VALUES = ["masters", "workers", "none", "all"]
    return hyperthreading in VALID_VALUES

def is_valid_network_type(network_type):
    VALID_VALUES = ["OpenShiftSDN", "OVNKubernetes"]
    return network_type in VALID_VALUES
