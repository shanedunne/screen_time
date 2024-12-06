import { initStore } from "../utils/store_utils.js";

const db = initStore("devices")

export const deviceStore = {
    
    // get the device mac and ip
    async getDeviceInfo() {
        await db.read()
        
        return db.data.devices;

    },

    // get device by mac
    async getDeviceByMac(mac) {
        await db.read()
        const deviceByMac = db.data.devices.find((device) => device.mac === mac);
        return deviceByMac
    },

    // get device data from api
    async getStats() {
        const url = "http://localhost:5001/api/devices/stats"
        try {
            const response = await fetch(url)
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`)
            }

            const json = await response.json();
            console.log(json);
            return json
        } catch (error) {
            console.error(error.message)
        }
    },

    /*
    async getDeviceSpecificStats(mac) {
        const stats = await this.getStats()
        console.log(typeof(stats))
        // const deviceStats = stats.find((stat) => stat.device === mac);
        return deviceStats;
    }
    */
}