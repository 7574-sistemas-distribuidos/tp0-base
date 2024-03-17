import sys 
SERVICES = """
services:
    server:
        container_name: server
        image: server:latest
        entrypoint: python3 /main.py
        environment:
        - PYTHONUNBUFFERED=1
        - LOGGING_LEVEL=DEBUG
        networks:
        - testing_net
"""

VERSION = """
version: '3.9'
name: tp0 
"""

NETWORK = """ 
networks:
    testing_net:
        ipam:
            driver: default
            config:
                - subnet: 172.25.125.0/24
"""

def generate_yaml(clients):
    services = SERVICES
    for client_id in range(0,clients):
        client_id = client_id + 1
        services += f'''
    client{client_id}:
        container_name: client{client_id}
        image: client:latest
        entrypoint: /client
        environment:
        - CLI_ID={client_id}
        - CLI_LOG_LEVEL=DEBUG
        networks:
        - testing_net
        depends_on:
        - server
        ''' 
    return VERSION + services + NETWORK



if __name__ == '__main__':
    yaml_file = "docker-compose-dev.yaml"
    try:
        if sys.argv[1] == "-h" or  sys.argv[1] == "--help":
            print("--------------------------------") 
            print("Usage: python generate_compose.py n")
            print("Generates a Docker Compose YAML file with n client services.")
            print("Arguments:")
            print("  - n: Number of client services to include in the YAML file.")
            print("Example:")
            print("  - python generate_compose.py 5 [0m")
            print("--------------------------------")
            sys.exit(0)
            
        clients = int (sys.argv[1])
        if clients <= 0:
            print(f"\033[91m[ERROR]\033[0m - Numbre of clients must be greater than 0")
            print(f"\033[92m[INFO]\033[0m - usage : python generate_compose.py n")
            print(f"\033[92m[INFO]\033[0m - Type -h or --help for more information")
            sys.exit(1)
        
        print(f"\033[92m[INFO]\033[0m  - clients: {clients}")
        print(f"\033[92m[INFO]\033[0m  - generating yaml file: {yaml_file}")
        with open(yaml_file, 'w') as f:
            f.write(generate_yaml(clients))
        
    except Exception as e:
        print(f"\033[91m[ERROR]\033[0m - {e}")
        print(f"\033[92m[INFO]\033[0m - Usage : python generate_compose.py n")
        sys.exit(1)