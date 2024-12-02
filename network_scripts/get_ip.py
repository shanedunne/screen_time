import subprocess
import json



# Find Mac Addresses Function
def find_ip_for_mac():

    # data structure for devices to check
    smart_devices = {
        "d8:e2:df:25:dc:c8": None, # XBOX
        "d8:e3:5e:eb:0e:50": None, # Smart TV
    }

    # interface for arp-scan command
    interface = "wlan0"
    result = subprocess.check_output(f"sudo arp-scan -q --interface={interface} --localnet", shell=True)
    decoded_result = result.decode("utf-8")
    
    for line in decoded_result.splitlines():
        data_piece = line.split()
        if len(data_piece) >= 2:
            ip, mac = data_piece[0], data_piece[1]
            if mac in smart_devices:
                smart_devices[mac] = ip
    
    # write data to json file
    # Serializing json
    json_object = json.dumps(smart_devices, indent=4)
 
    # Writing to sample.json
    with open("../data/mac_ip.json", "w") as outfile:
        outfile.write(json_object)
        
    return smart_devices

    
