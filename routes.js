import express from "express";

import { dashboardController } from "./controllers/dashboard-controller.js";

export const router = express.Router();

router.get("/", dashboardController.index);