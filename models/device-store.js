import { initStore } from "../utils/store_utils.js";

const db = initStore("devices")

export const deviceStore = {
    
    // get the device mac and ip
    async getDeviceInfo() {
        await db.read()
        
        return db.data.devices;

    }
}