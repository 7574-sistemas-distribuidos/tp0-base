class BetContent:
    _valueSeparator = ", "
    
    def __init__(self, name, lastname, id_number, birthdate, bet_number):
        self.name = name
        self.lastname = lastname
        self.id_number = id_number
        self.birthdate = birthdate
        self.bet_number = bet_number

    def deserialize(serializedBetContent):
        name, lastname, id_number, birthdate, bet_number = serializedBetContent.split(BetContent._valueSeparator)
        return BetContent(name, lastname, id_number, birthdate, bet_number)
