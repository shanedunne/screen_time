import { userStore } from "../models/user-store.js";

export const accountsController = {

  // render the index view which prompts users to login or signup
  index(request, response) {
    const viewData = {
      title: "Login or Signup",
    };
    response.render("index", viewData);
  },

  // renders the login view where a user with an account can login
  login(request, response) {
    const viewData = {
      title: "Login to your account",
    };
    response.render("login-view", viewData);
  },

  // clears the user cookie and redirects to the login or signup page. Logs user out
  logout(request, response) {
    response.cookie("user", "");
    response.redirect("/");
  },

  // renders the sign up view where users can sign up
  signup(request, response) {
    const viewData = {
      title: "Signup for an account",
    };
    response.render("signup-view", viewData);
  },

  // registers the user and redirects to login / signup view where the user can now login
  async register(request, response) {
    const user = request.body;
    await userStore.addUser(user);
    console.log(`registering ${user.email}`);
    response.redirect("/");
  },

  // gets the user and creates a cookie to store their logged in status.
  // redirects to the dashboard for logged in users, login page if no user.
  async authenticate(request, response) {
    const user = await userStore.getUserByEmail(request.body.email);
    if (user) {
      response.cookie("user", user._id);
      console.log(`logging in ${user.email}`);
      response.redirect("/dashboard");
    } else {
      response.redirect("/login");
    }
  },

  // gets the users ID from the cookie and returns the user
  async getLoggedInUser(request) {
    const userId = request.cookies.user;
    return await userStore.getUserById(userId);
  },

  // renders the account view which displays user details
  async getAccountInfo(request, response) {
    const user = await accountsController.getLoggedInUser(request);

    const viewData = {
      title: "Account Information",
      user: user,
    };
    response.render("account-view", viewData);
  },

  // renders the edit account view where users can edit their information
  async accountEditor(request, response) {
    const user = await accountsController.getLoggedInUser(request);
    const userId = user._id;

    console.log(userId + "is logged in")

    const viewData = {
      title: "Edit Account Information",
      user: user,
    };
    response.render("edit-account-view", viewData);
  },

  // passes new user information to the user store and updates the user
  async updateAccount(request, response) {
    const userId = request.params.userid;
    const updatedAccount = {
      firstName: request.body.firstName,
      lastName: request.body.lastName,
      email: request.body.email,
      password: request.body.password,
    };
    console.log(`Updating user ${userId}`);
    await userStore.updateUser(userId, updatedAccount);
    response.redirect("/account")
  },
};