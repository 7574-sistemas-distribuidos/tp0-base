import time
import datetime


""" Winners storage location. """
STORAGE = "./winners"


""" Contestant data model. """
class Contestant:
	def __init__(self, first_name, last_name, document, birthdate):
		""" Birthdate must be passed with format: 'YYYY-MM-DD'. """
		self.first_name = first_name
		self.last_name = last_name
		self.document = document
		self.birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
		
	def __hash__(self):
		return hash((self.first_name, self.last_name, self.document, self.birthdate))


""" Checks whether a contestant is a winner or not. """
def is_winner(contestant: Contestant) -> bool:
	# Simulate strong computation requirements using a sleep to increase function retention and force concurrency.
	time.sleep(0.001)
	return hash(contestant) % 17 == 0


""" Persist the information of each winner in the STORAGE file. Not thread-safe/process-safe. """
def persist_winners(winners: list[Contestant]) -> None:
	with open(STORAGE, 'a+') as file:
		for winner in winners:
			file.write(f'Full name: {winner.first_name} {winner.last_name} | Document: {winner.document} | Date of Birth: {winner.birthdate.strftime("%d/%m/%Y")}\n')

