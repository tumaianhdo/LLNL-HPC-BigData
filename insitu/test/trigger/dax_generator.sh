#!/bin/bash

DIR=$(cd $(dirname $0) && pwd)
python ${DIR}/generate_dax.py ${DIR}/workflows/$1 $2 $3

