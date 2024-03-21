import yaml

TOT_CLIENTS = 3

def generate_doccomp(tot_clients):
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

    for i in range(1, tot_clients + 1):
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

    return yaml.dump(docker_compose, sort_keys=False)

doccomp_variable_clientes = generate_doccomp(TOT_CLIENTS)
with open('docker-compose.yaml', 'w') as file:
    file.write(doccomp_variable_clientes)
