import subprocess
import os
import time

smart_devices = {
    "d8:e2:df:25:dc:c8": None, # XBOX
    "d8:e3:5e:eb:0e:50": None, # Smart TV
}

interface = "wlan0"

# Find Mac Addresses Function
def find_ip_for_mac(interface, smart_devices):
    result = subprocess.check_output(f"sudo arp-scan -q --interface={interface} --localnet", shell=True)
    decoded_result = result.decode("utf-8")
    
    for line in decoded_result.splitlines():
        data_piece = line.split()
        if len(data_piece) >= 2:
            ip, mac = data_piece[0], data_piece[1]
            if mac in smart_devices:
                smart_devices[mac] = ip
        
    return smart_devices

    
    
    return decoded_result


# Test code
if __name__ == "__main__":

    print("Scanning network...")
    get_ip = find_ip_for_mac(interface, smart_devices)
    print(smart_devices)
