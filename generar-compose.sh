if [ $# -ne 2 ]; then
    echo "Error: $0 needs 2 parameters to run <name_of_target_file> <clients_amount>"
    exit 1
fi

OUTPUT_FILE=$1
NUM_CLIENTS=$2

echo "version: '3'"                              > $OUTPUT_FILE
echo "services:"                                >> $OUTPUT_FILE
echo "  server:"                                >> $OUTPUT_FILE
echo "    image: server:latest"                 >> $OUTPUT_FILE
echo "    ports:"                               >> $OUTPUT_FILE
echo "      - \"8081:80\""                      >> $OUTPUT_FILE
echo "    entrypoint: python3 /main.py"         >> $OUTPUT_FILE
echo "    environment:"                         >> $OUTPUT_FILE
echo "      - PYTHONUNBUFFERED=1"               >> $OUTPUT_FILE
echo "      - LOGGING_LEVEL=DEBUG"              >> $OUTPUT_FILE
echo "    networks:"                            >> $OUTPUT_FILE
echo "      - testing_net"                      >> $OUTPUT_FILE
echo "    volumes:"                             >> $OUTPUT_FILE
echo "      - ./server/config.ini:/config.ini"  >> $OUTPUT_FILE
echo ""                                         >> $OUTPUT_FILE

python3 helpers/create_clients.py $OUTPUT_FILE $NUM_CLIENTS

echo "networks:"                                >> $OUTPUT_FILE
echo "  testing_net:"                           >> $OUTPUT_FILE
echo "    ipam:"                                >> $OUTPUT_FILE
echo "      driver: default"                    >> $OUTPUT_FILE
echo "      config:"                            >> $OUTPUT_FILE
echo "        - subnet: 172.25.125.0/24"        >> $OUTPUT_FILE

echo "Succesfully modified file $OUTPUT_FILE with $NUM_CLIENTS clients."
