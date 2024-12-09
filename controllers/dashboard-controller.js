import { deviceStore } from "../models/device-store.js";

export const dashboardController = {

    // renders the dashboard
    async index(request, response) {
        console.log("commencing running of dashboard")
        const deviceInfo = await deviceStore.getDeviceInfo()

        const viewData = {
            title : "Device Dashboard",
            devices: deviceInfo
        }
        console.log("Device dashboard rendering");
        response.render("dashboard-view", viewData);

    },

    // add new device
    async addDevice(request, response) {

        console.log(request.body)
        const newDevice = {
            device: request.body.nickname,
            mac: request.body.mac.toLowerCase(),
            ip: ""
        }

        console.log("passing to device store...")
        await deviceStore.callAddDeviceAPI(newDevice)
        response.redirect("/")
    }
};