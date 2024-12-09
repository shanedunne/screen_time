import axios from "axios";

export async function getStats() {
    const api = "http://127.0.0.1:5001/api/devices/stats";
    try {
        let response = await axios.get(api);

        const result = response.data;

        return result;

    } catch (error) {
        if (error.response && error.response.status === 404) {
            return { error: "Device not found in api database" }
        }
        console.error(error.message);
        return { error: "there was an issue accessing the data" }
    }
}

// post new device data to back end
export async function addDevice(device) {
    const api = "http://127.0.0.1:5001/api/devices/newDevice"
    try {
        console.log("sending to backend...")
        const response = await axios.post(api, device)
        console.log(response.data)
        
    } catch (error) {
        if (error.response && error.response.status === 404) {
            return { error: "Device not found in api database" }
        }
        console.error(error.message);
        return { error: "there was an issue accessing the data" }
    }
}