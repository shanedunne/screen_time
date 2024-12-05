import express from "express";
import bodyParser from "body-parser";
import cookieParser from "cookie-parser";
import fileUpload from "express-fileupload";
import { engine } from "express-handlebars";
import { router } from "./routes.js";
import "dotenv/config";

const app = express();
app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static("public"));
app.use(fileUpload());

// added json helper to read js objects in hbs files when sending info for the map
// https://stackoverflow.com/questions/10232574/need-handlebars-js-to-render-object-data-instead-of-object-object
app.engine(
  ".hbs",
  engine({
    extname: ".hbs",
    helpers: {
      json: function (context) {
        return JSON.stringify(context);
      },
    },
  })
);
app.set("view engine", ".hbs");
app.set("views", "./views");
app.use("/", router);

const listener = app.listen(process.env.PORT || 4000, function () {
  console.log(
    `Weather station site started on http://localhost:${
      listener.address().port
    }`
  );
});