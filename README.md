# you-choose
Anonymous voting system

## Getting Started

### Prerequisites

Create your secret files:

```console
mkdir secrets
echo my_super_db > secrets/database_db
echo my_super_user > secrets/database_user
echo my_super_password > secrets/database_password
```

You can also run ```secrets.sh``` script to generate those files:

```console
./secrets.sh
```

In order to run this project, you must have installed [docker-compose](https://docs.docker.com/compose/install/).

### Run

To run the project on a local environment, use:
```console
docker-compose up
# OR
docker-compose up -d # detached mode
```

### Stop

To run the the docker stack, use:
```console
docker-compose down
# OR
docker-compose down -v # to remove created volumes
```


## Deployment

WIP

## Built With

WIP

## Authors

WIP
