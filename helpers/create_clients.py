import sys

def generate_clients(filename, num_clients):
    with open(filename, 'a') as f:
        for i in range(1, int(num_clients) + 1):
            f.write(f"  client{i}:\n")
            f.write(f"    image: client:latest\n")
            f.write(f"    depends_on:\n")
            f.write(f"      - server\n")
            f.write(f"    volumes:\n")
            f.write(f"      - ./client/config.yaml:/config.yaml\n")
            f.write(f"    environment:\n")
            f.write(f"      - CLIENT_ID={i}\n")

if __name__ == "__main__":
    output_file = sys.argv[1]
    num_clients = sys.argv[2]
    generate_clients(output_file, num_clients)
