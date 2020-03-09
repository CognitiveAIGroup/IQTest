#!/bin/bash

pushd $(pwd)
SCRIPT_DIR="$(realpath "$(dirname "$BASH_SOURCE")")"
cd ${SCRIPT_DIR}

docker rm model-base:v-slim
docker build -t model-base:v-slim .
popd