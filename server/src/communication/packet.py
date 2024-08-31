class Packet:
    _tagValueSeparator = ": "
    _headerOptions_separator = "\n"
    _header_end = "\n\n"

    def __init__(self, command, client_id, message_id, data):
        self.command = command
        self.client_id = client_id
        self.message_id = message_id
        self.data = data

    def deserialize(serializedPacket):
        occurrences = 1
        header, content = serializedPacket.split(Packet._header_end, occurrences)
        headerOptions = header.split(Packet._headerOptions_separator)

        command = None
        client_id = None
        message_id = None
        for option in headerOptions:
            tag, value = option.split(Packet._tagValueSeparator, occurrences)
            if tag == "COMMAND":
                command = value
            elif tag == "CLIENT_ID":
                client_id = value
            elif tag == "MESSAGE_ID":
                message_id = value

        return Packet(command, client_id, message_id, content)

class PacketResponse:
    status_ok = "OK"
    status_ko = "KO"

    def __init__(self, status):
        self.status = status

    def serialize(packetResponse):
        return f"STATUS: {packetResponse.status}"
