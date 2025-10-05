import json
import logging as log
from mikrotik.exceptions import *

class Device:
    def __init__(self, identifier):
        log.debug(f"Device.__init__({self}) with identifier: {identifier}")
        # Indending for this to be a MAC Address
        self.identifier = identifier
        self.dhcp_data = {
            'comment': None,
            'address': None,
            'mac-address': None,
            'status': None,
            'host-name': None,
            'last-seen': None,
            'client-id': None,
            'server': None,
            'dynamic': None,
        }
        self.arp_data = {
            'comment': None,
            'address': None,
            'mac-address': None,
            'status': None,
            'interface': None,
            'published': None,
            'invalid': None,
            'dynamic': None,
        }

        self._has_conflicts = False
        self._conflict_details = {}

    def add_dhcp_data(self, lease_data):
        log.debug(f"Device.add_dhcp_data({self}) with lease data: {json.dumps(lease_data, indent=2)}")
        self.dhcp_data.update(lease_data)
        log.debug(f"Updated DHCP data: {json.dumps(self.dhcp_data, indent=2)}")
        self._check_conflicts()

    def add_arp_data(self, arp_data):
        log.debug(f"Device.add_arp_data({self}) with ARP data: {json.dumps(arp_data, indent=2)}")
        self.arp_data.update(arp_data)
        self._check_conflicts()

    def _check_conflicts(self):
        log.debug(f"Device._check_conflicts({self})")
        self._has_conflicts = False
        self._conflict_details = {}

        if not all(self.dhcp_data.values()) and not all(self.arp_data.values()):
            return

        dhcp_ip = self.dhcp_data.get('address')
        arp_ip = self.arp_data.get('address')
        if dhcp_ip and arp_ip and dhcp_ip != arp_ip:
            self._has_conflicts = True
            self._conflict_details['ip_mismatch'] = {
                'dhcp_ip': dhcp_ip,
                'arp_ip': arp_ip
            }

        dhcp_mac = self.dhcp_data.get('mac-address')
        arp_mac = self.arp_data.get('mac-address')
        if dhcp_mac and arp_mac and dhcp_mac.upper() != arp_mac.upper():
            self._has_conflicts = True
            self._conflict_details['mac_mismatch'] = {
                'dhcp_mac': dhcp_mac,
                'arp_mac': arp_mac
            }

    def get_merged_data(self):
        log.debug(f"Device.get_merged_data({self})")
        log.debug(f"Device.get_merged_data Current DHCP data: {self.dhcp_data}")
        log.debug(f"Device.get_merged_data Current ARP data: {self.arp_data}")
                                                  
        device_info = {
            'conflicts': self._has_conflicts,
            'conflict_details': self._conflict_details
        }

        device_ip_address = self.dhcp_data.get('address') or self.arp_data.get('address') or None
        if device_ip_address is None:
            log.error(f"Device {self.identifier} has no valid IP address from DHCP or ARP data.")
            raise NoValidIPAddressError(f"Device {self.identifier} has no valid IP address from DHCP or ARP data.")
        device_info.update({'ip_address': device_ip_address})

        device_mac_address = self.dhcp_data.get('mac-address') or self.arp_data.get('mac-address') or None
        if device_mac_address is None:
            log.error(f"Device {self.identifier} has no valid MAC address from DHCP or ARP data.")
            raise NoValidMacAddressError(f"Device {self.identifier} has no valid MAC address from DHCP or ARP data.")
        device_info.update({'mac_address': device_mac_address})

        device_info.update({
            'hostname': self.dhcp_data.get('host-name') or 'N/A',
            'dhcp_status': self.dhcp_data.get('status') or 'noDHCP',
            'last_seen': self.dhcp_data.get('last-seen') or 'noDHCP',
            'comment': self.dhcp_data.get('comment') or '',
            'client_id': self.dhcp_data.get('client-id') or 'noDHCP',
            'dhcp_server': self.dhcp_data.get('server') or 'noDHCP',
            'static_lease': self.dhcp_data.get('dynamic', 'true') == 'false'
        })

        device_info.update({
            'interface': self.arp_data.get('interface') or 'noARP',
            'arp_status': self.arp_data.get('status') or 'noARP',
            'published': self.arp_data.get('published') or 'noARP',
            'invalid': self.arp_data.get('invalid', 'false') == 'true',
            'dynamic': self.arp_data.get('dynamic', 'false') == 'true'
        })

        log.debug(f"Merged device info for {self.identifier}: {json.dumps(device_info, indent=2)}")
        return device_info

    def has_conflicts(self):
        log.debug(f"Device.has_conflicts({self}) => {self._has_conflicts}")
        return self._has_conflicts

    def get_conflict_details(self):
        log.debug(f"Device.get_conflict_details({self}) => {json.dumps(self._conflict_details, indent=2)}")
        return self._conflict_details

    def get_dhcp_data(self):
        log.debug(f"Device.get_dhcp_data({self}) => {json.dumps(self.dhcp_data, indent=2)}")
        return self.dhcp_data

    def get_arp_data(self):
        log.debug(f"Device.get_arp_data({self}) => {json.dumps(self.arp_data, indent=2)}")
        return self.arp_data
