import { v4 } from "uuid";
import { initStore } from "../utils/store-utils.js";

const db = initStore("users");

export const userStore = {

  // gets all users
  async getAllUsers() {
    await db.read();
    return db.data.users;
  },

  // adds a user to the user.json file
  async addUser(user) {
    await db.read();
    user._id = v4();
    db.data.users.push(user);
    await db.write();
    return user;
  },

  // gets a users data by its id
  async getUserById(id) {
    await db.read();
    return db.data.users.find((user) => user._id === id);
  },

  // gets a users data by its email
  async getUserByEmail(email) {
    await db.read();
    return db.data.users.find((user) => user.email === email);
  },

  // deletes a user from the json file by its id
  async deleteUserById(id) {
    await db.read();
    const index = db.data.users.findIndex((user) => user._id === id);
    db.data.users.splice(index, 1);
    await db.write();
  },

  // deletes all users
  async deleteAll() {
    db.data.users = [];
    await db.write();
  },

  // updates a user found by their id with new information
  async updateUser(userId, updatedUser) {
    const user = await this.getUserById(userId);
    user.firstName = updatedUser.firstName;
    user.lastName = updatedUser.lastName;
    user.email = updatedUser.email;
    user.password = updatedUser.password;
    db.write();
  }
};