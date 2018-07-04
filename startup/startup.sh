#! /bin/bash

docker run \
    --rm \
    --detach \
    --volume $(pwd):/workdir \
    --workdir /workdir \
    --publish 5000:5000 \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    brewblox/docker-compose-ui
