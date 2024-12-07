import { deviceStore } from "../models/device-store.js";

export const deviceController = {
    async index(request, response) {
        const device = await deviceStore.getDeviceByMac(request.params.mac);
        const stats = await deviceStore.getDeviceSpecificStats(request.params.mac)

        const viewData = {
            title: "Device",
            device: device,
            stats: stats
        };
        console.log("rendering device view")
        response.render("device-view", viewData);
    }
}