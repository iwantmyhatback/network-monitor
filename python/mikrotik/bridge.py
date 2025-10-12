"""
MikroTik Bridge Host Module
Handles bridge host information queries
"""

from .login import RouterLogin
from mikrotik.exceptions import *
import logging as log
import json

class BridgeHostManager:
    def __init__(self, connection=None):
        log.debug(f"BridgeHostManager.__init__({self})")
        self.router = RouterLogin()
        self.connection = connection

    def connect(self):
        log.debug(f"BridgeHostManager.connect({self})")
        if not self.connection:
            self.connection = self.router.connect()
        if not self.connection:
            raise RouterConnectionError("Failed to connect to router for bridge host entries")
        return self.connection is not None

    def disconnect(self):
        log.debug(f"BridgeHostManager.disconnect({self})")
        self.router.disconnect()

    def get_all_bridge_hosts(self):
        """
        Get all bridge host entries from the router
        Returns:
            list: List of bridge host entries
        """
        log.debug(f"BridgeHostManager.get_all_bridge_hosts({self})")
        if not self.connection:
            log.debug("No active connection, attempting to connect...")
            if not self.connect():
                return []

        try:
            log.debug("Querying router for /interface/bridge/host resource")
            hosts = self.connection.get_resource('/interface/bridge/host')
            result = hosts.get()
            log.debug(f"Bridge hosts query result: {json.dumps(result, indent=2)}")
            return result
        except Exception as e:
            log.error(f"Error getting bridge hosts: {str(e)}")
            return []

    def get_bridge_host_by_mac(self, mac_address):
        """
        Get bridge host entry for a specific MAC address
        Args:
            mac_address (str): MAC address to search for
        Returns:
            dict: Bridge host entry if found, None otherwise
        """
        log.debug(f"BridgeHostManager.get_bridge_host_by_mac({self}, {mac_address})")
        if not self.connection:
            log.debug("No active connection, attempting to connect...")
            if not self.connect():
                return None

        try:
            log.debug("Querying router for /interface/bridge/host resource")
            hosts = self.connection.get_resource('/interface/bridge/host')
            log.debug(f"Executing bridge host query for MAC: {mac_address}")
            result = hosts.get(mac_address=mac_address)
            log.debug(f"Bridge host query result for MAC {mac_address}: {json.dumps(result, indent=2)}")
            return result[0] if result else None
        except Exception as e:
            log.error(f"Error getting bridge host for MAC {mac_address}: {str(e)}")
            return None