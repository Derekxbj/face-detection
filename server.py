import socket
import sys
from detect_smile_simple import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
# The server address is the computer running CNN 
server_address = ('161.253.126.129', 10023)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()
    try:

        print ('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            data = str(data)
            # print ('received "%s"'  + data)
            if data:
                print ('sending data back to the client')

                print(data)
                print(data[2])
                print(len(data))
                print(type(data))

                seconds = int(data[2])

                counts = detect_smile(seconds)

                if counts > 0:

                    print("The patient is positive")
                    result = '1'
                    result_b = result.encode()

                else:
                    result = '0'
                    result_b = result.encode()

                connection.sendall(result_b)
            # else:
            #     print ('no more data from', client_address)
            #     break

    finally:
        # Clean up the connection
        connection.close()
