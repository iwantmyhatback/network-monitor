from datetime import datetime
from .login import RouterLogin
from mikrotik.exceptions import *
import json
import logging as log

class DHCPLeaseManager:
    def __init__(self):
        log.debug(f"DHCPLeaseManager.__init__({self})")
        self.router = RouterLogin()
        self.connection = None

    def connect(self):
        log.debug(f"DHCPLeaseManager.connect({self})")
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