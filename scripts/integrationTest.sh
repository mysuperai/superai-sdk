#!/bin/bash

set -ex

mkdir -p test # create test_data directory if it doesn't exist

trap 'kill $BGPID; exit' INT
superai ai local-deploy --config-file config.yml --skip-build --log -ncl &
BGPID=$!
sleep 5 # wait for the predictor config to be created in the deploy command
superai ai predictor-test -ifo test --config-file config.yml --wait-seconds ${1-"60"}