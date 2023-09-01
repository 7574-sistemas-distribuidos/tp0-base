import sys
import yaml

def generate_docker_compose(client_count):
    docker_compose = {
        'version': '3.9',
        'name': 'tp0',
        'services': {
            'server': {
                'container_name': 'server',
                'image': 'server:latest',
                'entrypoint': 'python3 /main.py',
                'environment': [
                    'PYTHONUNBUFFERED=1',
                    'LOGGING_LEVEL=DEBUG'
                ],
                'networks': ['testing_net']
            }
        },
        'networks': {
            'testing_net': {
                'ipam': {
                    'driver': 'default',
                    'config': [
                        {'subnet': '172.25.125.0/24'}
                    ]
                }
            }
        }
    }

    for i in range(1, client_count + 1):
        client_name = f'client{i}'
        docker_compose['services'][client_name] = {
            'container_name': client_name,
            'image': 'client:latest',
            'entrypoint': '/client',
            'environment': [
                f'CLI_ID={i}',
                'CLI_LOG_LEVEL=DEBUG'
            ],
            'networks': ['testing_net'],
            'depends_on': ['server']
        }

    return docker_compose

def write_docker_compose_yaml(docker_compose, filename='docker-compose-dev.yaml'):
    with open(filename, 'w') as yaml_file:
        yaml.dump(docker_compose, yaml_file, default_flow_style=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <numero_de_clientes>")
        sys.exit(1)

    try:
        client_count = int(sys.argv[1])
        if client_count < 0:
            print("El número de clientes debe ser un número positivo.")
            sys.exit(1)

        docker_compose = generate_docker_compose(client_count)
        write_docker_compose_yaml(docker_compose)
        print(f"Se ha creado o actualizado el archivo 'docker-compose-dev.yaml' con {client_count} clientes.")
    except ValueError:
        print("El número de clientes debe ser un número entero.")
        sys.exit(1)
