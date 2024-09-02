from src.communication.register_bets_command import RegisterBetsCommand
from src.communication.unknown_command import UnknownCommand
from src.communication.get_winners_command import GetWinnersCommand
from src.communication.close_load_of_bets_command import CloseLoadOfBetsCommand

class CommandDispatcher:
    def dispatch(packet):
        command_type = packet.command
        command = None
        if command_type == 'REGISTER_BETS':
            command = RegisterBetsCommand(packet)
        elif command_type == 'GET_WINNERS':
            command = GetWinnersCommand(packet)
        elif command_type == 'CLOSE_LOAD_OF_BETS':
            command = CloseLoadOfBetsCommand(packet)
        else:
            command = UnknownCommand(packet)
        return command.execute()
