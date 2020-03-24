# Веб-приложение для информирования о потребностях стационаров и блок-постов в КР для борьбы с COVID-19

## Technology Stack

Keystone, Graphql, Mongodb, Nextjs

We have to be quick, so try using as much abstractions as possible.

## Running the Project.

To run this project first install dependencies with `yarn`.

Copy `.env.dev` to `.env`

Start the mongodb using `docker-compose up -d mongo`

After that run `yarn run dev`

Once running, the Keystone Admin UI is available via `localhost:3000/admin`.

## Next steps

This example has no front-end application but you can build your own using the GraphQL API (`http://localhost:3000/admin/graphiql`).

`index.js` contains everything for now, but we need a separate file called `schema.js` where our database schema will be located.

Keystone generates the admin UI automatically.

## Good luck!

