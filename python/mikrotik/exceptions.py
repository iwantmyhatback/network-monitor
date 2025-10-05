


class NoDHCPLeasesError(Exception):
    """Exception raised when no DHCP leases are found"""
    pass

class RouterConnectionError(Exception):
    """Exception raised for errors in connecting to the router"""
    pass

class RouterConfigurationError(Exception):
    """Exception raised for errors in router configuration"""
    pass

class NoValidIPAddressError(Exception):
    """Exception raised when a device has no valid IP address from DHCP or ARP data"""
    pass

class NoValidMacAddressError(Exception):
    """Exception raised when a device has no valid MAC address from DHCP or ARP data"""
    pass