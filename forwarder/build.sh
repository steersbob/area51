#! /bin/bash
set -e

# Only need to create builder once
if [[ $(docker buildx inspect | grep 'linux/arm/v7') == '' ]]; then
    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
    docker buildx rm bricklayer || true
    docker buildx create --use --name bricklayer
    docker buildx inspect --bootstrap
fi

docker buildx build \
    --tag kargathia/area51:forwarder \
    --push \
    --platform linux/amd64,linux/arm/v7 \
    .
