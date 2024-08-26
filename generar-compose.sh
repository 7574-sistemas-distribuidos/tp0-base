#!/bin/bash

file_name=$1
nclients=$2
echo "Docker Compose file name: '${file_name}'"
echo "Number of clients: '${nclients}'"
poetry run -C scripts python scripts/scale_clients.py ${file_name} ${nclients}

exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "Docker Compose file generated with ${nclients} clients"
fi
