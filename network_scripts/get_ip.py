import subprocess
import json

# data structure for devices to check
smart_devices = {
    "d8:e2:df:25:dc:c8": None, # XBOX
    "d8:e3:5e:eb:0e:50": None, # Smart TV
}

# interface for arp-scan command
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


# Test code
if __name__ == "__main__":

    print("Scanning network...")
    get_ip = find_ip_for_mac(interface, smart_devices)
    print(smart_devices)

    # write data to json file
    # Serializing json
    json_object = json.dumps(smart_devices, indent=4)
 
    # Writing to sample.json
    with open("../data/mac_ip.json", "w") as outfile:
        outfile.write(json_object)
