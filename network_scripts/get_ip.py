import subprocess
import json



# Find Mac Addresses Function
def find_ip_for_mac():

    # check json for existing devices
    with open("./data/devices.json", 'r') as infile:
        data = json.load(infile)

    devices = data["devices"]

    # interface for arp-scan command
    interface = "wlan0"
    result = subprocess.check_output(f"sudo arp-scan -q --interface={interface} --localnet", shell=True)
    decoded_result = result.decode("utf-8")
    
    for line in decoded_result.splitlines():
        data_piece = line.split()
        if len(data_piece) >= 2:
            ip, mac = data_piece[0], data_piece[1]
            for device in devices:
                if device["mac"] == mac:
                    device["ip"] = ip
    
    # write data to json file
    # Serializing json
    json_object = json.dumps(smart_devices, indent=4)
 
    # Writing to sample.json
    with open("./data/devices.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
        
    return devices

    
