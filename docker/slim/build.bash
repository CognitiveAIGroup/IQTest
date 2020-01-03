#!/bin/bash

pushd $(pwd)
SCRIPT_DIR="$(realpath "$(dirname "$BASH_SOURCE")")"
cd ${SCRIPT_DIR}
cp ../../dist/iqtestsdk-0.2.4.4.tar.gz sdk
docker rm model:v-slim
docker build -t model:v-slim .
popd
