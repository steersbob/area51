#! /usr/bin/env bash
set -euo pipefail

if [[ $(docker buildx inspect | grep 'linux/arm/v7') == '' ]]; then
    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
    docker buildx rm bricklayer || true
    docker buildx create --use --name bricklayer
    docker buildx inspect --bootstrap
fi

docker buildx build \
    --tag brewblox/brewblox-misc:mdns-browser \
    --push \
    --platform linux/amd64,linux/arm/v7,linux/arm64/v8 \
    .
