import express, { Router } from "express";

import { dashboardController } from "./controllers/dashboard-controller.js";
import { deviceController } from "./controllers/device-controller.js";

export const router = express.Router();

router.get("/", dashboardController.index);

router.get("/device/:mac", deviceController.index);

router.post("/dashboard/adddevice", dashboardController.addDevice);