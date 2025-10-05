from mikrotik.dhcp import DHCPLeaseManager
from mikrotik.arp import ARPManager
from mikrotik.exceptions import *
import logging as log
import json

def merge_device_info(lease_data, arp_data):
    log.debug(f"Merging DHCP lease data and ARP data for device: {lease_data.get('host-name', lease_data.get('mac-address', 'UNKNOWN'))}")
    device_info = {
        'ip_address': lease_data.get('address', 'N/A'),
        'mac_address': lease_data.get('mac-address', 'N/A'),
        'hostname': lease_data.get('host-name', 'N/A'),
        'dhcp_status': lease_data.get('status', 'N/A'),
        'last_seen': lease_data.get('last-seen', 'N/A'),
        'comment': lease_data.get('comment', ''),
        'client_id': lease_data.get('client-id', 'N/A'),
        'dhcp_server': lease_data.get('server', 'N/A'),
        'active': lease_data.get('active-address', 'false') == 'true'
    }
    
    if arp_data:
        device_info.update({
            'interface': arp_data.get('interface', 'N/A'),
            'arp_status': arp_data.get('status', 'N/A'),
            'published': arp_data.get('published', 'N/A'),
            'invalid': arp_data.get('invalid', 'false') == 'true',
            'dynamic': arp_data.get('dynamic', 'false') == 'true'
        })
    
    log.debug(f"Merged device info: {json.dumps(device_info, indent=2)}")
    return device_info

def main():
    log.debug("Starting network device information gathering...")
    dhcp_manager = DHCPLeaseManager()
    arp_manager = ARPManager()
    devices = []

    log.debug("Compiling device information")
    try:
        active_leases = dhcp_manager.get_active_leases()
        log.debug(f"Found {len(active_leases)} active DHCP leases:\n {json.dumps(active_leases, indent=2)}")
        if not active_leases:
            raise NoActiveDHCPLeasesError("No active DHCP leases found in the network. This might indicate a DHCP server issue or network connectivity problem.")

        for lease in active_leases:
            ip_address = lease.get('address')
            if not ip_address:
                log.warning(f"Lease with missing IP address: {json.dumps(lease, indent=2)}")
            arp_entry = arp_manager.get_arp_by_ip(ip_address)
            device_info = merge_device_info(lease, arp_entry)
            devices.append(device_info)

        log.info(f"Compiled information for {len(devices)} devices.")
        log.debug(f"\n{("=" * 80)}\nNetwork Devices Information: \n{("=" * 80)}")
        for device in devices:
            log.debug(f"Device Details:\n{("-" * 40)}\nIP Address:\t{device['ip_address']}\nMAC Address:\t{device['mac_address']}\nHostname:\t{device['hostname']}\nInterface:\t{device.get('interface', 'N/A')}\nDHCP Status:\t{device['dhcp_status']}\nARP Status:\t{device.get('arp_status', 'N/A')}\nLast Seen:\t{device['last_seen']}\nDynamic:\t{device.get('dynamic', 'N/A')}\nActive:\t\t{device['active']}\nComment:\t{device['comment']}\n{("-" * 40)}")
            

    except Exception as e:
        log.error(f"{str(e)}")
    finally:
        dhcp_manager.disconnect()
        arp_manager.disconnect()

if __name__ == "__main__":
    main()