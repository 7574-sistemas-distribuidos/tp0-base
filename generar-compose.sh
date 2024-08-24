if [ $# -ne 2 ]; then
    echo "Error: $0 needs 2 parameters to run <name_of_target_file> <clients_amount>"
    exit 1
fi

OUTPUT_FILE=$1
NUM_CLIENTS=$2

echo "version: '3'" > $OUTPUT_FILE
echo "services:" >> $OUTPUT_FILE
echo "  tp_0:" >> $OUTPUT_FILE
echo "    image: tp_0:latest" >> $OUTPUT_FILE
echo "    ports:" >> $OUTPUT_FILE
echo "      - \"8081:80\"" >> $OUTPUT_FILE
echo "" >> $OUTPUT_FILE

python3 helpers/create_clients.py $OUTPUT_FILE $NUM_CLIENTS

echo "Succesfully modified file $OUTPUT_FILE with $NUM_CLIENTS clients."
