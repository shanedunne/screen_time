import { initStore } from "../utils/store_utils.js";
import { getStats } from "../utils/get_stats.js";

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
    

    
    async getDeviceSpecificStats(mac) {
        const stats = await getStats()
        const deviceStats = stats[mac]
        return deviceStats;
    }
    
}