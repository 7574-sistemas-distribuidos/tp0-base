import yaml
import sys


def get_client_count():
    return 1 if len(sys.argv) <= 1 or not sys.argv[1].isdigit() else int(sys.argv[1])


def create_docker_compose(n):
    with open(f"docker-compose-dev-{n}-clients.yaml", "w") as file:
        config = {
            'version': '3.9',
            'name': 'tp0',
            'services': {
                'server': build_server(),

            },
            'networks': build_network()
        }

        for i in range(n):
            config['services'][f'client{i+1}'] = build_client(i+1)

        yaml.dump(config, file, sort_keys=False)


def build_network():
    return {
        "testing_net": {
            "ipam": {
                "driver": 'default',
                "config": [{
                    "subnet": '172.25.125.0/24'
                }]
            }
        }
    }


def build_client(i):
    return {
        'container_name': f'client{i}',
        'image': 'client:latest',
        'entrypoint': '/client',
        'environment': [
            f'CLI_ID={i}',
            'CLI_LOG_LEVEL=DEBUG'
        ],
        'networks': ['testing_net'],
        'depends_on': ['server'],

    }


def build_server():
    return {
        'container_name': 'server',
        'image': 'server:latest',
        'entrypoint': 'python3 /main.py',
        'environment': [
            'PYTHONUNBUFFERED=1',
            'LOGGING_LEVEL=DEBUG'
        ],
        'networks': [
            'testing_net'
        ],

    }


def main():
    n = get_client_count()
    create_docker_compose(n)


if __name__ == "__main__":
    main()
