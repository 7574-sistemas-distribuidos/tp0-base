NETWORK_NAME="tp0-base_testing_net"
SERVER_CONTAINER="tp0-base-server-1"  
SERVER_PORT=12345
TEST_MESSAGE="Hello, World!"

if [ ! "$(docker ps -q -f name=$SERVER_CONTAINER)" ]; then
    echo "Container not running."
    exit 1
fi

# Remember to build client image locally first: "docker buildx build --platform linux/amd64 -t client:latest -f client/Dockerfile ."
echo "Sending message..."
RESPONSE=$(echo "$TEST_MESSAGE" | docker run --pull never --rm --platform linux/amd64 --network "$NETWORK_NAME" -i client:latest sh -c "nc $SERVER_CONTAINER $SERVER_PORT")
echo "Received response: $RESPONSE"

if [ "$RESPONSE" == "$TEST_MESSAGE" ]; then
    printf "\033[32maction: test_echo_server | result: success\033[0m\n"
else
    printf "\033[31maction: test_echo_server | result: fail\033[0m\n"
fi

