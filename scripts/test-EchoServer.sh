make docker-compose-up-clients CLIENTS=1
docker network connect tp0_testing_net client1
sudo docker start client1
docker cp ./scripts/test-EchoServer-Client1.sh client1:/
docker exec -it client1 sh test-EchoServer-Client1.sh
echo
echo
sleep 2
make docker-compose-down