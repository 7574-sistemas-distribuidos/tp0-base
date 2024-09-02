class Packet:
    _tag_value_separator = ": "
    _new_line_separator = "\n"
    _header_content_separator = "\n\n"

    def __init__(self, command, client_id, message_id, data):
        self.command = command
        self.client_id = client_id
        self.message_id = message_id
        self.data = data

    def deserialize(serializedPacket):
        occurrences = 1
        header, content = serializedPacket.split(Packet._header_content_separator, occurrences)
        header_options = header.split(Packet._new_line_separator)

        command = None
        client_id = None
        message_id = None
        for option in header_options:
            tag, value = option.split(Packet._tag_value_separator, occurrences)
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

    def __init__(self, status, data):
        self.status = status
        self.data = data

    def serialize(packetResponse):
        return f"STATUS: {packetResponse.status}\n\n{packetResponse.data}"
