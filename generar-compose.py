import sys
from constants import BAD_REQUEST, WRITE_MODE, YAML_TAB


def write_server(file):
    file.write(YAML_TAB + "server:\n")
    file.write(YAML_TAB + YAML_TAB + "container_name: server\n")
    file.write(YAML_TAB + YAML_TAB + "image: server:latest\n")
    file.write(YAML_TAB + YAML_TAB + "entrypoint: python3 /main.py\n")
    file.write(YAML_TAB + YAML_TAB + "environment:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- PYTHONUNBUFFERED=1\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- LOGGING_LEVEL=DEBUG\n")
    file.write(YAML_TAB + YAML_TAB + "networks:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- testing_net\n")
    file.write("\n")

def write_client(id, file):
    file.write(YAML_TAB + "client" + str(id) + ":\n")
    file.write(YAML_TAB + YAML_TAB + "container_name: client" + str(id) + "\n")
    file.write(YAML_TAB + YAML_TAB + "image: client:latest\n")
    file.write(YAML_TAB + YAML_TAB + "entrypoint: /client\n")
    file.write(YAML_TAB + YAML_TAB + "environment:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- CLI_ID=" + str(id) + "\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- CLI_LOG_LEVEL=DEBUG\n")
    file.write(YAML_TAB + YAML_TAB + "networks:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- testing_net\n")
    file.write(YAML_TAB + YAML_TAB + "depends_on:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "- server\n")
    file.write("\n")

def write_clients(file, clients):
    for id, _ in enumerate(clients):
        write_client(id+1, file)

def write_services(file, clients):
    file.write("services:\n")
    write_server(file)
    write_clients(file, clients)

def write_networks(file):
    file.write("networks:\n")
    file.write(YAML_TAB + "testing_net:\n")
    file.write(YAML_TAB + YAML_TAB + "ipam:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "driver: default\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + "config:\n")
    file.write(YAML_TAB + YAML_TAB + YAML_TAB + YAML_TAB + "- subnet: 172.25.125.0/24\n")

def write_file(file, clients):
    file.write("name: tp0\n")
    write_services(file, clients)
    write_networks(file)

def create_file(name, clients):
    print("Creating", name, "file for", clients, "clients") # todo COMO LOGUEARLO?
    file = open(name, WRITE_MODE)
    write_file(file, clients)
    file.close()

def main():
    output_file_name, clients = sys.argv[1], sys.argv[2]
    create_file(output_file_name, clients)

if __name__ == "__main__":
    main()
