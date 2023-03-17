import time
import datetime


""" Bets storage location. """
STORAGE = "./bets.csv"
""" Simulated winner number in the lottery contest. """
LOTTERY_WINNER_NUMBER = 7574


""" A lottery bet registry. """
class Bet:
    def __init__(self, first_name, last_name, document, birthdate, number):
        """ Birthdate must be passed with format: 'YYYY-MM-DD'. """
        self.first_name = first_name
        self.last_name = last_name
        self.document = document
        self.birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
        self.number = number

""" Checks whether a contestant is a winner or not. """
def has_won(bet: Bet) -> bool:
    return bet.number == LOTTERY_WINNER_NUMBER

""" Persist the information of each bet in the STORAGE file. Not thread-safe/process-safe. """
def store_bets(bets: list[Bet]) -> None:
    with open(STORAGE, 'a+') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        for bet in bets:
            writer.writerow([bet.first_name, bet.last_name, bet.document, bet.birthdate, bet.number])

""" Loads the information all the bets in the STORAGE file. Not thread-safe/process-safe. """
def load_bets() -> list[Bet]:
    with open(STORAGE, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            yield Bet(row[0], row[1], row[2], row[3], row[4], row[5])

