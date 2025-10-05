


class NoActiveDHCPLeasesError(Exception):
    """Exception raised when no active DHCP leases are found"""
    pass

class RouterConnectionError(Exception):
    """Exception raised for errors in connecting to the router"""
    pass

class RouterConfigurationError(Exception):
    """Exception raised for errors in router configuration"""
    pass