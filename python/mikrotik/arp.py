import json
import logging as log
from mikrotik.exceptions import *
from .login import RouterLogin

class ARPManager:
    def __init__(self):
        log.debug(f"ARPManager.__init__({self})")
        self.router = RouterLogin()
        self.connection = None

    def connect(self):
        log.debug(f"ARPManager.connect({self})")
        self.connection = self.router.connect()
        if not self.connection:
            raise RouterConnectionError("Failed to connect to router for ARP entries")
        return self.connection is not None

    def disconnect(self):
        log.debug(f"ARPManager.disconnect({self})")
        self.router.disconnect()

    def get_arp_entries(self):
        log.debug(f"ARPManager.get_arp_entries({self})")
        if not self.connection:
            log.debug("No active connection, attempting to connect...")
            if not self.connect():
                return []

        try:
            log.debug("Querying router for /ip/arp resource")
            arp = self.connection.get_resource('/ip/arp')
            log.debug(f"Successfully retrieved ARP entries: {json.dumps(arp, indent=2)}")
            return arp.get()
        except Exception as e:
            log.error(f"Error getting ARP entries: {str(e)}")
            return []

    def get_arp_by_mac(self, mac_address):
        log.debug(f"ARPManager.get_arp_by_mac({self}, {mac_address})")
        if not self.connection:
            log.debug("No active connection, attempting to connect...")
            if not self.connect():
                return None
            
        try:
            log.debug(f"Querying router for /ip/arp resource")
            arp = self.connection.get_resource('/ip/arp')
            log.debug(f"Executing ARP query for MAC: {mac_address}")
            result = arp.get(mac_address=mac_address)
            log.debug(f"ARP query result for MAC {mac_address}: {json.dumps(result, indent=2)}")
            return result[0] if result else None
        except Exception as e:
            log.error(f"Error getting ARP entry for MAC {mac_address}: {str(e)}")
            return None

    def get_arp_by_ip(self, ip_address):
        log.debug(f"ARPManager.get_arp_by_ip({self}, {ip_address})")
        if not self.connection:
            log.debug("No active connection, attempting to connect...")
            if not self.connect():
                return None

        try:
            log.debug(f"Querying router for /ip/arp resource")
            arp = self.connection.get_resource('/ip/arp')
            log.debug(f"Executing ARP query for IP: {ip_address}")
            result = arp.get(address=ip_address)
            log.debug(f"ARP query result for IP {ip_address}: {json.dumps(result, indent=2)}")
            return result[0] if result else None
        except Exception as e:
            log.error(f"Error getting ARP entry for IP {ip_address}: {str(e)}")
            return None