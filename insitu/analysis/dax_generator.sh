#!/bin/bash
DIR=$(dirname "$(readlink -f "$0")")
python ${DIR}/generate_dax.py ${DIR}/workflows/$1 $2 $3

