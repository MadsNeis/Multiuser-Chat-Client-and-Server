# Madison Neiswonger
# CS 372 -> Final Project: Multiuser Chat Server and Client
# Server File


# The server will run using select() to handle multiple connections to see which ones are ready to read

# The listener socket itself will also be included in this set.

# When it shows ready to ready, it means there's a new connection to be accept() ed.

# If any other already-accepted sockets show ready to read, it means the client has sent some data that needs to be handled.

# When the server gets a chat packet from one client, it rebroadcasts that chat message to every connected client. (Not talking about IP or Ethernet here)

# When a client connects or disconnects, the server broadcasts that to all clients as well.

# With multiple client, the server needs to maintain a packet buffer for EACH client. (put this in a python dict that uses the client's socket itself aas the key so it maps from a socket to a buffer)

# The server will be launched by specifying a port number on the command line. This is mandatory THERE IS NO DEFAULT PORT.

import socket
import sys
import select
import json

if len(sys.argv) != 2:
    print("Usage: python server.py <port>")
    sys.exit(1)

port = int(sys.argv[1])

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
s.listen()

print("Listening on port", port)

# Dict to store incomplete packets
client_buffers = {}
client_nicknames = {}

# select() loop
read_sockets = [s]

def get_next_packet(buffer):
    if len(buffer) < 2:
        return None, buffer

    payload_length = int.from_bytes(buffer[0:2], byteorder='big')

    total_length = 2 + payload_length
    if len(buffer) < total_length:
        return None, buffer

    packet = buffer[2:total_length]

    remaining = buffer[total_length:]
    return packet, remaining

def broadcast(message_dict, exclude_socket=None):

    #convert dict to json
    json_string = json.dumps(message_dict)

    json_bytes = json_string.encode('utf-8')

    payload_length = len(json_bytes)
    length_bytes = payload_length.to_bytes(2, byteorder='big')

    packet = length_bytes + json_bytes

    for client_socket in list(client_nicknames.keys()):
        if client_socket != exclude_socket:
            try:
                client_socket.sendall(packet)
            except:
                pass

while True:
    # call select()
    ready_to_read, _, _ = select.select(read_sockets, [], [])

# handle socket listener
    for ready_socket in ready_to_read:
        if ready_socket == s:
            client_socket, client_address = s.accept()

            read_sockets.append(client_socket)
            client_buffers[client_socket] = b''

        else:
            #ready to read
            data = ready_socket.recv(4096)

            if not data:
                nick = client_nicknames.get(ready_socket, "unknown")
                print(nick,"disconnected")

                nick = client_nicknames.get(ready_socket, "unknown")

                if ready_socket in client_nicknames:
                    leave_message = {
                        "type": "leave",
                        "nick": nick
                    }
                    broadcast(leave_message, exclude_socket=ready_socket)

                read_sockets.remove(ready_socket)
                del client_buffers[ready_socket]
                if ready_socket in client_nicknames:
                    del client_nicknames[ready_socket]

                ready_socket.close()
                continue

            client_buffers[ready_socket] += data


            # extract complete packets from buffers
            while True:
                packet_data, client_buffers[ready_socket] = get_next_packet(client_buffers[ready_socket])

                if packet_data is None:
                    break

                # Parse JSON
                try:
                    json_string = packet_data.decode('utf-8')
                    message = json.loads(json_string)

                except:
                    print("Error parsing JSON")
                    continue

                message_type = message.get("type")

                if message_type == "hello":
                    nick = message.get("nick", "unknown")
                    client_nicknames[ready_socket] = nick

                    print(f"***{nick} has joined the chat!")

                    join_message = {
                        "type": "join",
                        "nick": nick
                    }
                    broadcast(join_message)

                # Chat Packets
                elif message_type == "chat":
                    chat_text = message.get("message", "")
                    sender_nick = client_nicknames.get(ready_socket, "unknown")

                    print(f"{sender_nick}: {chat_text}")

                    chat_message = {
                        "type": "chat",
                        "nick": sender_nick,
                        "message": chat_text
                    }
                    broadcast(chat_message)




