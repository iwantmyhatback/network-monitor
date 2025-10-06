# network-monitor
MikroTik router LAN monitoring utility

### Execution
- `shell/run.sh`: Runs directly on host machine
- `shell/run_docker.sh`: Runs containerized version

### Python Modules
- `network.py`: Main monitoring logic, combines DHCP/ARP data
- `mikrotik/`:
  - `network_device.py`: Device state representation
  - `login.py`: Router authentication
  - `dhcp.py`: DHCP lease monitoring
  - `arp.py`: ARP table monitoring
  - `bridge.py`: Bridge interface operations
  - `exceptions.py`: Error handling

### Device Tracking
- IP/MAC addresses
- Hostnames
- Interface assignments
- DHCP lease status
- Online/offline state
- Device comments

### Configuration
- `configuration/config.json`: Router credentials
- `configuration/environment.properties`: Environment variables
