from mikrotik.dhcp import DHCPLeaseManager
from mikrotik.arp import ARPManager
from mikrotik.bridge import BridgeHostManager
from mikrotik.network_device import NetworkDevice
from mikrotik.exceptions import *
from mikrotik.login import RouterLogin
import logging as log
import json

def main():
    log.debug("Starting network device information gathering...")
    router = RouterLogin().connect()
    dhcp_manager = DHCPLeaseManager(router)
    arp_manager = ARPManager(router)
    bridge_manager = BridgeHostManager(router)
    devices_dict = {}

    log.debug("Compiling device information")
    try:
        log.debug("Fetching DHCP leases from router...")
        dhcp_leases = dhcp_manager.get_all_leases()
        log.debug(f"Found {len(dhcp_leases)} DHCP leases:\n {json.dumps(dhcp_leases, indent=2)}")
        if not dhcp_leases:
            log.error("No DHCP leases found in the network.")
            raise NoDHCPLeasesError("No DHCP leases found in the network. This might indicate a DHCP server issue or network connectivity problem...")

        log.debug("Processing DHCP leases...")
        for lease in dhcp_leases:
            ip_address = lease.get('address')
            mac_address = lease.get('mac-address')
            if not ip_address or not mac_address:
                log.warning(f"Lease with missing IP or MAC address: {json.dumps(lease, indent=2)}")
                continue

            if mac_address not in devices_dict:
                log.debug(f"Creating new device entry for MAC: {mac_address}")
                devices_dict[mac_address] = NetworkDevice(mac_address)
            log.debug(f"Adding DHCP data to device with MAC: {mac_address}")
            devices_dict[mac_address].add_dhcp_data(lease)

            log.debug(f"Fetching ARP entry for MAC: {mac_address}")
            arp_entry = arp_manager.get_arp_by_mac(mac_address)
            if arp_entry:
                log.debug(f"Adding ARP data to device with MAC: {mac_address}")
                devices_dict[mac_address].add_arp_data(arp_entry)
            else:
                log.warning(f"No ARP entry found for MAC: {mac_address}")

            log.debug(f"Fetching bridge data for MAC: {mac_address}")
            bridge_entry = bridge_manager.get_bridge_host_by_mac(mac_address)
            if bridge_entry:
                log.debug(f"Adding bridge data to device with MAC: {mac_address}")
                devices_dict[mac_address].add_bridge_data(bridge_entry)
            else:
                log.warning(f"No bridge entry found for MAC: {mac_address}")


        log.info(f"Compiled information for {len(devices_dict)} devices.")
        log.info(f"\n{("=" * 80)}\nNetwork Devices Information: \n{("=" * 80)}\n")
        
        for ip, device in devices_dict.items():
            device_info = device.get_merged_data()
            log.info(
                f"Device Details:\n{("-" * 40)}\n"
                f"IP Address:\t{device_info.get('ip_address')}\n"
                f"MAC Address:\t{device_info.get('mac_address')}\n"
                f"Hostname:\t{device_info.get('hostname')}\n"
                f"Interface:\t{device_info.get('interface')}\n"
                f"DHCP Status:\t{device_info.get('dhcp_status')}\n"
                f"ARP Status:\t{device_info.get('arp_status')}\n"
                f"Last Seen:\t{device_info.get('last_seen')}\n"
                f"Dynamic:\t{device_info.get('dynamic')}\n"
                f"Static Lease:\t{device_info.get('static_lease')}\n"
                f"Bridge:\t\t{device_info.get('bridge')}\n"
                f"Bridge Port:\t{device_info.get('bridge_interface')}\n"
                f"Bridge Status:\t{device_info.get('bridge_status')}\n"
                f"On Bridge:\t{device_info.get('on_bridge')}\n"
                f"Bridge Local:\t{device_info.get('bridge_local')}\n"
                f"Comment:\t{device_info.get('comment')}"
            )
            
            if device_info.get('conflicts'):
                log.warning(
                    f"Conflicts detected:\n"
                    f"{json.dumps(device_info.get('conflict_details'), indent=2)}"
                )
            log.info(f"\n{"-"*40}")

    except Exception as e:
        log.error(f"{str(e)}")
    finally:
        router.disconnect()
        # Just in case any manager opened its own connection (which they shouldn't now)
        dhcp_manager.disconnect()
        arp_manager.disconnect()
        bridge_manager.disconnect()

if __name__ == "__main__":
    main()