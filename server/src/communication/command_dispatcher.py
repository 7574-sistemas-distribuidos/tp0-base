from src.communication.register_bet_command import RegisterBetCommand
from src.communication.unknown_command import UnknownCommand

class CommandDispatcher:
    def dispatch(packet):
        commandType = packet.command
        command = None
        if commandType == 'REGISTER_BET':
            command = RegisterBetCommand(packet)
        else:
            command = UnknownCommand(packet)
        return command.execute()
