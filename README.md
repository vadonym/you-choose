# YouChoose
Anonymous voting system

## Getting Started

### Prerequisites

Create your secret files:

```bash
mkdir secrets
echo my_super_db       > secrets/database_db
echo my_super_user     > secrets/database_user
echo my_super_password > secrets/database_password
```

You can also run ```secrets.sh``` script to generate those files:

```bash
./secrets.sh
```

In order to run this project, you must have installed [docker-compose](https://docs.docker.com/compose/install/).

### Run

To run the project on a local environment, use:
```bash
# run
docker-compose up

# run in detached mode (background)
docker-compose up -d

# rebuild images
docker-compose up -build
```

### Stop

To run the the docker stack, use:
```bash
# stop
docker-compose down

# stop and remove created volumes
docker-compose down -v
```


## Deployment

WIP

## Built With

WIP

## Authors

WIP
