# coffee-t-t-c

## Description

Coffee Shop.

## Index

- [Wake up the all the stack](#wake-up-the-all-the-stack)
- [How to](#how-to)
    - [How to manipulate the "cli" service](#how-to-manipulate-the-cli-service)
- [Checking services](#checking-services)
    - [Check if rest-api service is live](#check-if-rest-api-service-is-live)
    - [Check if postgres service is live](#check-if-postgres-service-is-live)
- [Tools used for this stack](#tools-used-for-this-stack)

## Wake up the all the stack

```bash
git clone x

# Copy and fill up the environment variables.
cp .docker/.env.dist .docker/.env

docker compose -f .docker/compose.yml build

# Ref: https://docs.docker.com/engine/reference/commandline/compose_up/
docker compose -f .docker/compose.yml up

# Starts the containers in the background and leaves them running.
docker compose -f .docker/compose.yml up --detach

# Get the name of the existing container (exited and running services)
docker ps -a

# Instance a bash shell in the container
docker exec -it <container name> [ /bin/bash | bash | sh ]

# Turn off the all the services, make sure to run this to release the resources provisioned into the host.
docker compose -f .docker/compose.yml down
```

## How to

### How to manipulate the cli service

```bash
# You should require a new bash if the containers are running on live mode instead of detach.

# If the "build" already was executed, just go the `run` stage.
docker compose -f .docker/compose.yml build

docker compose -f .docker/compose.yml run --rm cli <your-command>

docker compose -f .docker/compose.yml down
```

## Checking services

### Check if rest-api service is live

```bash
# Run the next command on the host machine, not inside containers.
export ENDPOINT="http://127.0.0.1:8004/"

# Check if the endpoint `ENDPOINT` it is listening inbound requests.
wget --spider --server-response ${ENDPOINT} 2>&1 | grep 'HTTP/1.1 200 OK'

# Alternative use `curl`.
curl ${ENDPOINT}

# Got the object defined by the endpoint.
> {"Hello":"World"}
```

### Check if postgres service is live

```bash
# Instance a bash session into the `cli` service.
docker compose -f .docker/compose.yml run --rm cli bash

# Previously, install `postgres` in order to check if is ready for accepting connections.
pg_isready --host=$POSTGRES_HOST --username=$POSTGRES_USER --port=$POSTGRES_PORT
> host:5432 - accepting connections

# Connect into the db from the `cli` container
psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB
```

## Tools used for this stack

```bash
docker compose version
> Docker Compose version v2.15.1

docker version
> Client:
 Cloud integration: v1.0.29
 Version:           20.10.22
 API version:       1.41
 Go version:        go1.18.9
 Git commit:        3a2c30b
 Built:             Thu Dec 15 22:28:41 2022
 OS/Arch:           darwin/arm64
 Context:           default
 Experimental:      true
```

## TODO:

Some activities need to be done before fully release this project:

- Set unit testing along core logic flows;
- Apply a more concise MVC pattern in order to decouple logic from the endpoints;
- Apply a small CI pipeline related with QA and static typing ("autopep8", "isort", "pydocstyle", "pylint", "radon");
- Add a more readable documentation about the entire app;
- Add a Postman collection in order to fully replicate the REST API in a more easier way.


🇺🇾 | 🇻🇪
