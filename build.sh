#!/usr/bin/env bash

cd "$(dirname "$(readlink -f "$0")")"
cd ./tests

../bark.py record
../bark.py compare


