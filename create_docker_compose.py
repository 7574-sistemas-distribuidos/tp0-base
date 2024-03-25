import sys
import os


def create_client(file, number):
    file.write('  client' + str(number) + ':\n')
    file.write('    container_name: client' + str(number) + '\n')
    file.write('    image: client:latest\n')
    file.write('    volumes:\n')
    file.write('      - ./client/config.yaml:/config.yaml\n')
    file.write('      - .data/dataset/agency-'+ str(number) + '.csv:/agency-'+ str(number) +'.csv\n')
    file.write('    entrypoint: /client\n')
    file.write('    environment:\n')
    file.write('      - CLI_ID=' + str(number) + '\n')
    file.write('      - CLI_LOG_LEVEL=DEBUG\n')
    file.write('    networks:\n')
    file.write('      - testing_net\n')
    file.write('    depends_on:\n')
    file.write('      - server\n\n')


def main():
    argv = sys.argv
    amount = int(argv[1])
    with open('docker-compose-dev.yaml', 'r') as old:
        with open('new.yaml', 'w') as new:
            index = 0
            lines = old.readlines()
            while lines[index] != '  client1:\n':
                line = lines[index]
                new.write(line)
                index += 1
            
            for i in range(1,amount+1):
                create_client(new, i)

            while lines[index] != 'networks:\n':
                index += 1

            while index < len(lines):
                line = lines[index]
                new.write(line)
                index += 1
                
    os.remove('docker-compose-dev.yaml')
    os.rename('new.yaml', 'docker-compose-dev.yaml')

main()