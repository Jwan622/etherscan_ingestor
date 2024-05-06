# Nascent Data Engineer Assignment

The provided assignment is meant to showcase how you approach a full-stack data engineering project.

### Contact Info

```
Name: `Jeffrey Wan`
Email: `Jwan622@gmail.com`
Github: `Jwan622`
```

## Overview

We have an ingestor and a Next.js frontend and a postgres container. Let's get up and running all 3 services.

## Other Docs

I took notes in the docs folder in each repo. Check them out if you'd like. Things I learned or discovered I noted here.

For example: [api notes on etherscan](./docs/notes_api.md) or [notes on code](./docs/notes_code.md).

Also, my todo list with some future features if I had more time.

[todo list](./docs/notes_todo.md)

You might be wondering why no Flask or Django server? Explanation here:
[architecture choices](docs/notes_project_design.md)

## Up and Running

Let's get the ingestor running first.

### Running the ingestor

First, get poetry installed. I stripped out pip for poetry (script files too). You should be able to install poetry if you run:
```bash
cd nascent_etherscan_ingestor
make build
```

which will attempt to install poetry for you.

Poetry will create a virtualenv for you (in a short, a folder with all of your dependencies)

Once you've done that, cd into `nascent_etherscan_ingestor` and run `poetry init` inside the repo, then you can do these commands.

Then run
```md
make
```

which will create the postgres image, install dependencies, run tests and get your postgres docker container running. Note the above `make` command needs you to have docker and docker-compose installed. 

Then to ingest data into the database:

```bash
make run 
```

That will populate the docker container's postgres tables (and create them too).

To run tests:

```bash
make test
```

### Running our Next.js frontend

I think you'll need node 18.17 and npx? More info here: https://nextjs.org/docs/getting-started/installation. But maybe not? Try this:

```bash
cd etherscan_frontend
```

and then run:

```bash
yarn
yarn dev
```

to run yarn tests:

```bash
yarn test
```

which should get the next.js project up and running on `localhost:3000` and it connects to the postgres database.

**(Sorry getting up and running with this might involve downloading node and npx and I'm unwilling to uninstall both on my machine lol)**

If you run the ingestor with `make run` in one terminal, it will ingest data to the docker container which is port-forwarded from `localhost:5434` (I changed the default port for the docker port forwarding to postgres, yes). The frontend can run against the postgres container as data is being ingested to it.




