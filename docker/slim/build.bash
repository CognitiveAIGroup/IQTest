#!/bin/bash

pushd $(pwd)
SCRIPT_DIR="$(realpath "$(dirname "$BASH_SOURCE")")"
cd ${SCRIPT_DIR}
if [ ! -d sdk ]
then
mkdir sdk
fi
cp ../../dist/iqtestsdk-0.2.5.0.tar.gz sdk
docker rm iqtest/model
docker build -t iqtest/model .
popd
