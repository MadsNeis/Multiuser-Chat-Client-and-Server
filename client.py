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

