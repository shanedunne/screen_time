export const dashboardController = {

    // renders the dashboard
    async index(request, response) {
        

        const viewData = {
            title : "Device Dashboard",
        }
        console.log("Device dashboard rendering");
        response.render("dashboard-view", viewData);

    },
};