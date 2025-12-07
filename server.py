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

