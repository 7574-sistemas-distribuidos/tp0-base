#!/bin/bash
docker build -t server_test .
docker run -it -d --name server_test --network tp0_testing_net server_test #runs dockerfile

docker exec -it server_test bash -c "echo 'joe biden' | nc -v 172.25.125.2 22222" > test.txt