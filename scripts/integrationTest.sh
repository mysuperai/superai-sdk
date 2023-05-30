#!/bin/bash

set -x

mkdir -p test_data # create test_data directory if it doesn't exist

trap 'kill $BGPID; exit' INT
superai ai local-deploy --config-file config.yml --skip-build --log -ncl &
BGPID=$!
superai ai predictor-test -ifo test_data --config-file config.yml --wait-seconds ${1-"60"}