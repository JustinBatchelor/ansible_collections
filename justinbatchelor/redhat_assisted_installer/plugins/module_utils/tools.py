import ipaddress

def is_valid_ip(ip):
    """
    Validate if the provided IP address is valid.
    
    Args:
        ip (str): The IP address to validate.
    
    Returns:
        bool: True if the IP address is valid, False otherwise.
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    

