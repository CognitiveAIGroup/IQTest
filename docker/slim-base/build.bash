#!/bin/bash

pushd $(pwd)
SCRIPT_DIR="$(realpath "$(dirname "$BASH_SOURCE")")"
cd ${SCRIPT_DIR}

docker rm iqtest/model-base
docker build -t iqtest/model-base .
popd