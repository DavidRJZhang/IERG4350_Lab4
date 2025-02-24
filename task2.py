"""Network Interface Information Analyzer

This module provides functionality to scan and analyze IPv4 addresses 
on local network interfaces, including netmask conversion and localhost detection.
"""

import json
import netifaces
from netaddr import IPAddress
from typing import Dict, Any, List

def get_ip_addresses() -> Dict[str, List[Dict[str, Any]]]:
    """Get network interfaces with their IPv4 addresses and metadata.
    
    Returns:
        A dictionary mapping interface names to lists of address information
        dictionaries containing 'addr', 'netmask' and 'broadcast' keys.
    """
    interface_ip_map = {}
    
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            interface_ip_map[interface] = addresses[netifaces.AF_INET]
    
    return interface_ip_map

def convert_netmask_to_cidr(ip_info: Dict[str, str]) -> Dict[str, Any]:
    """Convert dotted-decimal netmask to CIDR notation.
    
    Args:
        ip_info: Dictionary containing 'netmask' in dotted-decimal format
        
    Returns:
        Modified dictionary with 'netmask' replaced by integer CIDR value
    """
    try:
        cidr_bits = int(IPAddress(ip_info['netmask']).netmask_bits())
        return {**ip_info, 'netmask': cidr_bits}
    except ValueError:
        return {**ip_info, 'netmask': 'invalid'}

def is_localhost(ip_info: Dict[str, str]) -> bool:
    """Check if an IP address is localhost.
    
    Args:
        ip_info: Dictionary containing 'addr' key
        
    Returns:
        True if address is 127.0.0.1, False otherwise
    """
    return ip_info.get('addr') == '127.0.0.1'

def main() -> None:
    """Main execution flow"""
    interfaces = get_ip_addresses()
    result = {}
    
    for interface, addresses in interfaces.items():
        processed = []
        for addr_info in addresses:
            processed.append({
                **convert_netmask_to_cidr(addr_info),
                'is_localhost': is_localhost(addr_info)
            })
        result[interface] = processed
    
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()