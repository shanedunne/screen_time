import express, { Router } from "express";

import { dashboardController } from "./controllers/dashboard-controller.js";
import { deviceController } from "./controllers/device-controller.js";
import { accountsController } from "./controllers/account-controller.js";

export const router = express.Router();

router.get("/", accountsController.index);

router.get("/login", accountsController.login);
router.get("/signup", accountsController.signup);
router.get("/logout", accountsController.logout);
router.post("/register", accountsController.register);
router.post("/authenticate", accountsController.authenticate);

router.post("/dashboard/adddevice", dashboardController.addDevice);
router.get("/dashboard", dashboardController.index);

router.get("/device/deletedevice/:mac", deviceController.deleteDevice);
router.get("/device/:mac", deviceController.index);


router.get("/account", accountsController.getAccountInfo);
router.get("/account/:userid/editInfo", accountsController.accountEditor);
router.post("/account/:userid/updateaccount", accountsController.updateAccount);