from src.communication.register_bets_command import RegisterBetsCommand
from src.communication.unknown_command import UnknownCommand

class CommandDispatcher:
    def dispatch(packet):
        commandType = packet.command
        command = None
        if commandType == 'REGISTER_BETS':
            command = RegisterBetsCommand(packet)
        else:
            command = UnknownCommand(packet)
        return command.execute()
