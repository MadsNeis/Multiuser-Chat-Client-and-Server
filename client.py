# Madison Neiswonger
# CS 372 -> Final Project: Multiuser Chat Server and Client.
# Client File

#  When the client is launched, the user specifies their nickname on the command line along with server information.

# The very first packet it sends is a "hello" packet that had the nickname in it.
# This will be how the server associates a connection with a "nick" and rebroadcasts the connection.

# Each line the user types into the client gets sent to the server as a chat packet.
# Each chat packet the client gets from the server is shown on the output


# The client has a text user interface

# The client will be multithreaded and there will be two thread of execution
    # The main sending thread will:
        # Read keyboard input
        # Send chat messages from the user to the server

    # The receiving thread will:
        # Receive packets from the server
        # Display those results on-screen


# Special User Input: /q , if the user enters this, the client should exit and nothing will be sent to the server.


# Functions needed for the client TUI
# init_windows(): call this first before doing any other UI-Oriented I/O of any kind.
# end_windows(): call this when your program completes to clean everything up
# read_command(): this prints a prompt out at the bottom of the screen and accepts user input.
# print_message(): prints a message to the output portion of the screen. This handles scrolling and makes sure the output doesn't interfere with the input from read_command()

from chatui import init_windows, read_command, print_message, end_windows

import sys
import socket
import json
import threading

if len(sys.argv) !=4:
    print("Usage: python client.py <nickname> <server_address> <port>")
    sys.exit(1)

nickname = sys.argv[1]
server_address = sys.argv[2]
port = int(sys.argv[3])

# connect to server
s = socket.socket()

try:
    s.connect((server_address, port))
    print("Connected to server")
except:
    print("Failed to connect to server")
    sys.exit(1)


# initializing the UI
init_windows()

receive_buffer = b''

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

def send_packet(message_dict):
    #dict to json

    json_string = json.dumps(message_dict)
    json_bytes = json_string.encode('utf-8')

    payload_length = len(json_bytes)
    length_bytes = payload_length.to_bytes(2, byteorder='big')

    packet = length_bytes + json_bytes

    s.sendall(packet)

def receiver():
    global receive_buffer

    while True:
        try:
            data = s.recv(4096)

            if not data:
                print_message("Server disconnected")
                break

            receive_buffer += data

            while True:
                packet_data, receive_buffer = get_next_packet(receive_buffer)

                if packet_data is None:
                    break

                try:
                    json_string = packet_data.decode('utf-8')
                    message = json.loads(json_string)
                except:
                    print_message("Parsing error")
                    continue

                message_type = message.get("type")

                if message_type == "chat":
                    nick = message.get("nick", "unknown")
                    text = message.get("message", "")
                    print_message(f"{nick}: {text}")

                elif message_type == "join":
                    nick = message.get("nick", "unknown")
                    print_message(f"*** {nick} has joined the chat")

                elif message_type == "leave":
                    nick = message.get("nick", "unknown")
                    print_message(f"{nick} has left the chat")

        except Exception as e:
            print_message("Disconnected")
            break


# Hello Packet

hello_packet = {
    "type": "hello",
    "nick": nickname,
}
send_packet(hello_packet)

receiver = threading.Thread(target=receiver, daemon=True)
receiver.start()

try:
    while True:
        # reading user input
        user_input = read_command(f"{nickname}> ")

        #"/q" quit handling
        if user_input.strip() == "/q":
            break

        #sending chat message
        if user_input.strip():
            chat_packet = {
                "type": "chat",
                "message": user_input
            }
            send_packet(chat_packet)

except KeyboardInterrupt:
    pass

#cleaning on exit
end_windows()
s.close()
print("Hope you had fun chatting! Goodbye, good morning, and good night!")
