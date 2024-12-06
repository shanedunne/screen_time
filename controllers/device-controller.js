import { deviceStore } from "../models/device-store.js";

export const deviceController = {
    async index(request, response) {
        const device = await deviceStore.getDeviceByMac(request.params.mac);
        const stats = await deviceStore.getStats()

        const viewData = {
            title: "Device",
            device: device,
        };

        console.log(stats)
        console.log("rendering device view")
        response.render("device-view", viewData);
    }
}