# Nascent Data Engineer Assignment

The provided assignment is meant to showcase how you approach a full-stack data engineering project.

### Contact Info

```
Name: `Jeffrey Wan`
Email: `Jwan622@gmail.com`
Github: `Jwan622`
```

## Overview

We have an ingestor and a Next.js frontend. Let's get up and running

## Up and Running

Let's get the ingestor running first.

### Running the ingestor

First, get poetry installed. I stripped out pip for poetry. You should be able to install poetry if you run:
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

```bash
cd etherscan_frontend
```

and then run:

```bash
yarn
yarn dev
```

which should get the next.js project up and running on `localhost:3000` and it connects to the postgres database.

If you run the ingestor with `make run` in one terminal, it will ingest data to the docker container which is port-forwarded from `localhost:5434` (I changed default port, yes). The frontend can run against the postgres container as data is being ingested to it.

# Other Docs

I took notes in the docs folder in each repo. Check them out if you'd like. Things I learned or discovered

For example: [api notes on etherscan](./docs/notes_api.md) or [notes on code](./docs/notes_code.md)

Also my todo list with some future features if I had more time.

[todo list](./docs/notes_todo.md)


