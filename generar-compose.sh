#!/bin/bash

if [ $# -ne 2 ]; then
    BAD_REQUEST=$(python3 -c "from constants import BAD_REQUEST; print(BAD_REQUEST)")
    echo "$BAD_REQUEST: Two arguments must be included."
    exit 1
fi

python3 generar-compose.py $1 $2

