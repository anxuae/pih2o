#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

export PYTHONPATH=$SCRIPTPATH/..:$SCRIPTPATH/mocks:$PYTHONPATH

python $SCRIPTPATH/../pih2o/h2o.py $@
