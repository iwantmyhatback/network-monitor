# network-monitor
### LAN monitoring utility

**Can be used in 2 entrypoint methods:**
1. `shell/run.sh` which runs baremetial on the machine
2. `shell/run_docker.sh` which creates, maintains, and runs a container to then execute `shell/run.sh`


### Order of execution:
1. **Execute `shell/run_docker.sh` :**
    1. Check if `docker` is installed and fail out if not
    2. Export environment variables from `configuration/environment.properties` if `ALREADY_SOURCED` is not already in the environment
    3. if :
    * Docker image does not exist
    * Repository HEAD has changed
    * `FORCE_DOCKER_REBUILD` is set to "TRUE"
        
    4. **Execute `shell/build_image.sh` :**
        1. Export environment variables from `configuration/environment.properties` if `ALREADY_SOURCED` is not already in the environment
        2. Deactivate and delete any existing bare metal Python virtual environment
        3. Get Python base Docker image
        4. Delete old python-wrapper Docker image
        5. Create a new python-wrapper Docker image
    5. Otherwise : 
        1. Deactivate and delete any existing bare metal Python virtual environment
    6. **Execute `shell/run.sh` :**
        1. Export environment variables from `configuration/environment.properties` if `ALREADY_SOURCED` is not already in the environment
        2. Create, activate, and upgrade Python virtual environment if not already existing
        3. Install requirements from `requirements.txt`
        4. **Execute `python/main.py` :**
            1. Create Python log handler
            2. Run placeholder `network.main()`
            3. This will enter the network monitoring flow

### Network Monitoring Functionality

The network monitoring system (`python/network.py`) provides comprehensive device tracking and network monitoring capabilities for MikroTik router environments. Here's an overview of the main components and their functions:

#### Core Components:

1. **Network Device Discovery** (`network.py`)
   - Combines DHCP and ARP information for complete device visibility
   - Tracks active network devices and their status
   - Merges multiple data sources for comprehensive device profiles

2. **MikroTik Integration** (`python/mikrotik/`)
   - **Login Module** (`login.py`): Handles router authentication and connection management
   - **DHCP Module** (`dhcp.py`): Monitors and queries DHCP lease information
   - **ARP Module** (`arp.py`): Tracks ARP table entries and device presence
   - **Exception Handling** (`exceptions.py`): Custom exceptions for robust error management

#### Device Information Tracked:
- IP and MAC addresses
- Hostnames and device identifiers
- Network interface assignments
- DHCP lease status and history
- ARP table status
- Connection activity and timing
- Dynamic/static status
- Device comments and custom identifiers

#### Configuration:
- Router credentials stored in `configuration/config.json`
- Configurable logging levels
- Support for both Docker and bare metal deployment
- Virtual environment management for dependency isolation
