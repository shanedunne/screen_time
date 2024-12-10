import { deviceStore } from "../models/device-store.js";
import { accountsController } from "./account-controller.js";

export const dashboardController = {

    // renders the dashboard
    async index(request, response) {
        const loggedInUser = await accountsController.getLoggedInUser(request);
        const deviceInfo = await deviceStore.getDevicesByUserId(loggedInUser._id);

        const viewData = {
            title : "Device Dashboard",
            devices: deviceInfo
        }
        console.log("Device dashboard rendering");
        response.render("dashboard-view", viewData);

    },

    // add new device
    async addDevice(request, response) {
        const loggedInUser = await accountsController.getLoggedInUser(request);


        console.log(request.body)
        const newDevice = {
            device: request.body.nickname,
            mac: request.body.mac.toLowerCase(),
            ip: "",
            userid: loggedInUser._id
        }

        console.log("passing to device store...")
        await deviceStore.callAddDeviceAPI(newDevice)
        response.redirect("/dashboard")
    }
};