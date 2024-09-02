import logging
from src.utils import load_bets, has_won

class ResultsRegistryMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ResultsRegistry(metaclass=ResultsRegistryMeta):
    def __init__(self):
        self._agencies = {
            "1": False,
            "2": False,
            "3": False,
            "4": False,
            "5": False,
        }

    def close_agency(self, agency):
        self._agencies[agency] = True
        log = True
        for key in self._agencies.keys():
            if not self._agencies[key]:
                log = False
                break
        if log:
            logging.info("action: sorteo | result: success")

    def get_winners(self, agency):
        for key in self._agencies.keys():
            if not self._agencies[key]:
                raise Exception("Cannot retrieve results until all agencies are closed")
        bets = load_bets()
        winners = [bet for bet in bets if (bet.agency == int(agency) and has_won(bet))]
        return winners

    