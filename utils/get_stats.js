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