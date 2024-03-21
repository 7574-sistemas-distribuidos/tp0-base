import csv
import datetime
import time


""" Bets storage location. """
STORAGE_FILEPATH = "./bets.csv"
""" Simulated winner number in the lottery contest. """
LOTTERY_WINNER_NUMBER = 7574

AGENCY_BYTES = 2
DOCUMENT_BYTES = 4
NUMBER_BYTES = 4
DAY_BYTES = 1
MONTH_BYTES = 1
YEAR_BYTES = 2
DATE_BYTES = DAY_BYTES + MONTH_BYTES + YEAR_BYTES
NAME_LEN_BYTES = 1
HEADER_LEN = AGENCY_BYTES + DOCUMENT_BYTES + DATE_BYTES + NUMBER_BYTES + NAME_LEN_BYTES

AGENCY_BYTE_POSITION = 0
DAY_BYTE_POSITION = AGENCY_BYTE_POSITION + AGENCY_BYTES
MONTH_BYTE_POSITION = DAY_BYTE_POSITION + DAY_BYTES
YEAR_BYTE_POSITION = MONTH_BYTE_POSITION + MONTH_BYTES
DOCUMENT_BYTE_POSITION = YEAR_BYTE_POSITION + YEAR_BYTES
NUMBER_BYTE_POSITION = DOCUMENT_BYTE_POSITION + DOCUMENT_BYTES
NAME_LEN_BYTE_POSITION = NUMBER_BYTE_POSITION + NUMBER_BYTES



""" A lottery bet registry. """
class Bet:
    
    def __init__(self, agency: str, first_name: str, last_name: str, document: str, birthdate: str, number: str):
        """
        agency must be passed with integer format.
        birthdate must be passed with format: 'YYYY-MM-DD'.
        number must be passed with integer format.
        """

        self.agency = int(agency)
        self.first_name = first_name
        self.last_name = last_name
        self.document = document
        self.birthdate = datetime.date.fromisoformat(birthdate)
        self.number = int(number)

    @classmethod
    def from_bytes(cls, byte_array):
        if (len(byte_array) < HEADER_LEN) or (len(byte_array) != HEADER_LEN + byte_array[NAME_LEN_BYTE_POSITION]):
            print("Invalid bet bytes")
            return  None
        agency = byte_array_to_big_endian_integer(byte_array[AGENCY_BYTE_POSITION:DAY_BYTE_POSITION])
        day = byte_array[DAY_BYTE_POSITION]
        month = byte_array[MONTH_BYTE_POSITION]
        year = byte_array_to_big_endian_integer(byte_array[YEAR_BYTE_POSITION:DOCUMENT_BYTE_POSITION])
        date = datetime.date(year, month, day).isoformat()
        document = byte_array_to_big_endian_integer(byte_array[DOCUMENT_BYTE_POSITION:NUMBER_BYTE_POSITION])
        number = byte_array_to_big_endian_integer(byte_array[NUMBER_BYTE_POSITION:NAME_LEN_BYTE_POSITION])
        names = bytes(byte_array[NAME_LEN_BYTE_POSITION + 1:]).decode().split(';')
        if len(names) != 2:
            print("Invalid Name")
            return None
        name = names[0]
        last_name = names[1]
        return Bet(str(agency), name, last_name, str(document), date, str(number))


""" Checks whether a bet won the prize or not. """
def has_won(bet: Bet) -> bool:
    return bet.number == LOTTERY_WINNER_NUMBER

"""
Persist the information of each bet in the STORAGE_FILEPATH file.
Not thread-safe/process-safe.
"""
def store_bets(bets: list[Bet]) -> None:
    with open(STORAGE_FILEPATH, 'a+') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        for bet in bets:
            writer.writerow([bet.agency, bet.first_name, bet.last_name,
                             bet.document, bet.birthdate, bet.number])

"""
Loads the information all the bets in the STORAGE_FILEPATH file.
Not thread-safe/process-safe.
"""
def load_bets() -> list[Bet]:
    with open(STORAGE_FILEPATH, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            yield Bet(row[0], row[1], row[2], row[3], row[4], row[5])

def byte_array_to_big_endian_integer(bytes):
    number = 0
    for i in range(0, len(bytes)):
        number = number | bytes[i] << 8*(len(bytes)-1-i)
    return number

# Receives bytes until n bytes have been received. If cannot receive n bytes None is returned
def recv_exactly(socket, n):
    buffer = bytes()
    while n > 0:
        received = socket.recv(n)
        if len(received) == 0:
            return None
        buffer += received
        n -= len(received)
    return buffer 