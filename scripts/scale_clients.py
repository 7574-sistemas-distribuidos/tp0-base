# Script to scale the number of client containers in docker-compose file
import sys
import argparse
import yaml

# Status
CODE_SUCCESS = 0
CODE_FAILURE = 1

# Docker Compose configuration
CONFIG_PARAM_CONTAINER_NAME = "container_name"
CONFIG_PARAM_ENVIRONMENT = "environment"
CLIENT_SERVICE_PREFIX = "client"
CLIENT_SERVICE_ENV_ID_NAME = "CLI_ID"
FILE_BEGIN_POSITION = 0


def get_service_client_config():
    return {
        CONFIG_PARAM_CONTAINER_NAME: "",
        "image": "client:latest",
        "entrypoint": "/client",
        CONFIG_PARAM_ENVIRONMENT: ["CLI_LOG_LEVEL=DEBUG"],
        "volumes": ["./client/config.yaml:/config.yaml"],
        "networks": ["testing_net"],
        "depends_on": ["server"],
    }


# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="Scale clients in a docker-compose file",
        usage="%(prog)s <file_path> <n_clients>",
    )
    parser.add_argument(
        "file_path", metavar="file_path", help="path to a docker-compose file"
    )
    parser.add_argument("n_clients", type=n_clients, help="number of clients to scale")
    args = parser.parse_args()
    return args


def n_clients(value):
    try:
        n_clients = int(value)
        if n_clients < 0:
            raise argparse.ArgumentTypeError(
                f"invalid value: '{value}' is not a positive integer"
            )
        return n_clients
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid type: '{value}' is not an integer")


# Entry point
def main():
    args = parse_args()
    file_path = args.file_path
    n_clients = args.n_clients

    try:
        with open(file_path, "r+") as docker_compose_file:
            docker_compose_file_as_yaml = yaml.safe_load(docker_compose_file)
            docker_services = docker_compose_file_as_yaml["services"]
            client_containers = [
                (service, config)
                for service, config in docker_services.items()
                if service.startswith(CLIENT_SERVICE_PREFIX)
            ]

            if n_clients > len(client_containers):
                for i in range(len(client_containers), n_clients):
                    new_client_service_name = f"{CLIENT_SERVICE_PREFIX}{i + 1}"
                    new_client_service_config = get_service_client_config()
                    new_client_service_config[
                        CONFIG_PARAM_CONTAINER_NAME
                    ] = new_client_service_name
                    new_client_service_config[CONFIG_PARAM_ENVIRONMENT].append(
                        f"{CLIENT_SERVICE_ENV_ID_NAME}={i + 1}"
                    )
                    docker_services[new_client_service_name] = new_client_service_config
            elif n_clients < len(client_containers):
                for i in range(len(client_containers), n_clients, -1):
                    client_service_name = f"{CLIENT_SERVICE_PREFIX}{i}"
                    del docker_services[client_service_name]
            else:
                sys.exit(CODE_SUCCESS)

            docker_compose_file.seek(FILE_BEGIN_POSITION)
            docker_compose_file.truncate()
            yaml.dump(docker_compose_file_as_yaml, docker_compose_file, sort_keys=False)
    except OSError as error:
        print(f"{error.__class__.__name__}: {error}")
        sys.exit(CODE_FAILURE)
    except Exception as error:
        print(f"Unexpected error occurred: {error}")
        sys.exit(CODE_FAILURE)


main()
