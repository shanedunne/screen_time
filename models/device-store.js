import { initStore } from "../utils/store_utils.js";
import { getStats, addDevice } from "../utils/api_requests.js";

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

    // deletes a device by its id
    async deleteDeviceByMac(mac) {
        await db.read();
        const index = db.data.devices.findIndex((device) => device.mac === mac);
        db.data.devices.splice(index, 1);
        await db.write();
    },


    // get stats specific to the provided mac address
    async getDeviceSpecificStats(mac) {
        const stats = await getStats()
        const deviceStats = stats[mac]
        return deviceStats;
    },

    // pass the new device api details to python
    async callAddDeviceAPI(device) {
        console.log("calling api...")
        addDevice(device)
    },

    // gets the devices associated to a specific user
    async getDevicesByUserId(userid) {
        await db.read();
        return db.data.devices.filter((device) => device.userid === userid);
      },


}