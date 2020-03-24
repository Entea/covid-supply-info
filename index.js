const { config } = require('dotenv');
const { Keystone } = require('@keystonejs/keystone');
const { PasswordAuthStrategy } = require('@keystonejs/auth-password');
const { Text, Checkbox, Password } = require('@keystonejs/fields');
const { GraphQLApp } = require('@keystonejs/app-graphql');
const { AdminUIApp } = require('@keystonejs/app-admin-ui');
const { NextApp } = require('@keystonejs/app-next');
const session = require('express-session');
const MongoStore = require('connect-mongo')(session);
const initialiseData = require('./initial-data');

config();
const { MongooseAdapter: Adapter } = require('@keystonejs/adapter-mongoose');

// require our schema.js

const { ClinicSchema, OtherSchema, AddressNodeSchema } = require('./schema');

const PROJECT_NAME = "covid-supply-info";

let parameters = {
    name: PROJECT_NAME,
    adapter: new Adapter(),
    onConnect: initialiseData
};
if (process.env.NODE_ENV === 'production') {
    parameters.sessionStore = new MongoStore({url: process.env.MONGO_URI});
}
const keystone = new Keystone(parameters);

// Access control functions
const userIsAdmin = ({ authentication: { item: user } }) => Boolean(user && user.isAdmin);
const userOwnsItem = ({ authentication: { item: user } }) => {
  if (!user) {
    return false;
  }
  return { id: user.id };
};

const userIsAdminOrOwner = auth => {
  const isAdmin = access.userIsAdmin(auth);
  const isOwner = access.userOwnsItem(auth);
  return isAdmin ? isAdmin : isOwner;
};

const access = { userIsAdmin, userOwnsItem, userIsAdminOrOwner };

keystone.createList('User', {
  fields: {
    name: { type: Text },
    email: {
      type: Text,
      isUnique: true,
    },
    isAdmin: {
      type: Checkbox,
      // Field-level access controls
      // Here, we set more restrictive field access so a non-admin cannot make themselves admin.
      access: {
        update: access.userIsAdmin,
      },
    },
    password: {
      type: Password,
    },
  },
  // List-level access controls
  access: {
    read: access.userIsAdminOrOwner,
    update: access.userIsAdminOrOwner,
    create: access.userIsAdmin,
    delete: access.userIsAdmin,
    auth: true,
  },
});

// Put your schemas here

keystone.createList('Clinic', ClinicSchema);
keystone.createList('AddressNode', AddressNodeSchema);


const authStrategy = keystone.createAuthStrategy({
  type: PasswordAuthStrategy,
  list: 'User',
});

module.exports = {
  keystone,
  apps: [
    new GraphQLApp(),
    new AdminUIApp({
      authStrategy,
    }),
    new NextApp({dir: 'client-app'})
  ],
};
