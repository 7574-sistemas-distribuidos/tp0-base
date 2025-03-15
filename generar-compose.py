import sys

from constants import BAD_REQUEST, WRITE_MODE


def get_arguments():
    return sys.argv[1], sys.argv[2]

def create_file(name, clients):
    print("Creating", name, "file for", clients, "clients") # todo COMO LOGUEARLO?


def main():
    output_file_name, clients = get_arguments()
    create_file(output_file_name, clients)

if __name__ == "__main__":
    main()
