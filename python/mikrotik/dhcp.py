from datetime import datetime
from .login import RouterLogin
from mikrotik.exceptions import *
import json
import logging as log

class DHCPLeaseManager:
    def __init__(self, connection=None):
        log.debug(f"DHCPLeaseManager.__init__({self})")
        self.router = RouterLogin()
        self.connection = connection

    def connect(self):
        log.debug(f"DHCPLeaseManager.connect({self})")
        if not self.connection:
            self.connection = self.router.connect()
        if not self.connection:
            raise RouterConnectionError("Failed to connect to router for ARP entries")
        return self.connection is not None

    def disconnect(self):
        log.debug(f"DHCPLeaseManager.disconnect({self})")
        self.router.disconnect()

    def get_all_leases(self):
        log.debug(f"DHCPLeaseManager.get_all_leases({self})")
        if not self.connection:
            log.debug("No active connection, attempting to connect...")
            if not self.connect():
                return []

        try:
            log.debug("Querying router for /ip/dhcp-server/lease resource")
            leases = self.connection.get_resource('/ip/dhcp-server/lease')
            log.debug(f"Successfully retrieved DHCP leases: {leases}")
            return leases.get()
        except Exception as e:
            log.error(f"Error getting DHCP leases: {str(e)}")
            return []

    def get_active_leases(self):
        log.debug(f"DHCPLeaseManager.get_active_leases({self})")
        if not self.connection:
            log.debug("No active connection, attempting to connect...")
            if not self.connect():
                return []

        try:
            log.debug("Querying router for /ip/dhcp-server/lease resource")
            leases = self.connection.get_resource('/ip/dhcp-server/lease')
            log.debug(f"Successfully retrieved DHCP leases: {leases}")
            return leases.get(status='bound')
        except Exception as e:
            log.error(f"Error getting active leases: {str(e)}")
            return []

    def get_lease_by_mac(self, mac_address):
        log.debug(f"DHCPLeaseManager.get_lease_by_mac({self}, {mac_address})")
        if not self.connection:
            log.debug("No active connection, attempting to connect...")
            if not self.connect():
                return None

        try:
            log.debug("Querying router for /ip/dhcp-server/lease resource")
            leases = self.connection.get_resource('/ip/dhcp-server/lease')
            log.debug(f"Executing DHCP lease query for MAC: {mac_address}")
            result = leases.get(mac_address=mac_address)
            log.debug(f"DHCP lease query result for MAC {mac_address}: {json.dumps(result, indent=2)}")
            return result[0] if result else None
        except Exception as e:
            log.error(f"Error getting lease for MAC {mac_address}: {str(e)}")
            return None

    def get_lease_by_ip(self, ip_address):
        log.debug(f"DHCPLeaseManager.get_lease_by_ip({self}, {ip_address})")
        if not self.connection:
            log.debug("No active connection, attempting to connect...")
            if not self.connect():
                return None

        try:
            log.debug("Querying router for /ip/dhcp-server/lease resource")
            leases = self.connection.get_resource('/ip/dhcp-server/lease')
            log.debug(f"Executing DHCP lease query for IP: {ip_address}")
            result = leases.get(address=ip_address)
            log.debug(f"DHCP lease query result for IP {ip_address}: {json.dumps(result, indent=2)}")
            return result[0] if result else None
        except Exception as e:
            log.error(f"Error getting lease for IP {ip_address}: {str(e)}")
            return None
        


#####################
# DHCP Lease Data Sample
#####################
'''
{
    "id":                 "*D",                     # Unique identifier for the lease entry
    "address":            "123.123.123.123",        # IP address assigned to the client by the lease
    "mac-address":        "12:34:56:AB:CD:EF",      # MAC address of the client device
    "client-id":          "1:12:34:56:AB:CD:EF",    # Client identifier, often derived from the MAC address
    "address-lists":      "",                       # ???
    "server":             "myDhcpServer",           # DHCP server that issued the lease
    "dhcp-option":        "",                       # DHCP options associated with the lease
    "status":             "bound",                  # Status of the lease [bound|waiting|expired]
    "expires-after":      "15m48s",                 # Time remaining before the lease expires
    "last-seen":          "14m12s",                 # Time since the lease was last active (this seems to be periodically updated rather than live)
    "active-address":     "123.123.123.123",        # Currently active IP address for the lease (I KNOW -- If you change the lease address this will not update until the client renews)
    "active-mac-address": 12:34:56:AB:CD:EF",       # Currently active MAC address for the lease (I ASSUME -- If you change the lease MAC this will not update until the client renews)
    "active-client-id":   "1:12:34:56:AB:CD:EF",    # Currently active client identifier for the lease (I ASSUME -- If you change the lease client-id this will not update until the client renews)
    "active-server":      "defconf",                # Currently active DHCP server for the lease (I ASSUME -- If you change the lease server this will not update until the client renews)    
    "host-name":          "advertisedHostnameHere", # Hostname reported by the client during DHCP negotiation
    "radius":             "false",                  # Indicates if RADIUS auth is used for this lease
    "dynamic":            "false",                  # Indicates if the lease is dynamically assigned (by the server) or statically set (by admin)
    "blocked":            "false",                  # ???
    "disabled":           "false",                  # Indicates if the lease is disabled (prevents assignment)
    "comment": "          "                         # Admin comment for the lease
}
'''