
from sys import argv
import yaml

if len(argv) !=2 or not argv[1].isdigit() or not (0 < int(argv[1]) <= 10) :
    print(argv[1].isdigit())
    print("se debe ingresar un número natural menor o igual a 10")
    exit(1)

docker_compose_file = "docker-compose-dev.yaml"

content=""
with open(docker_compose_file,"+r") as file:
    config = yaml.safe_load(file)


config["services"]["client"]["deploy"]["replicas"] = argv[1]

print(config)

# Write YAML file
with open(docker_compose_file, 'w', encoding='utf8') as outfile:
    yaml.dump(config, outfile, default_flow_style=False, allow_unicode=True)