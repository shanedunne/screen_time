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
};