import sys

import socket_tcp

# CLIENT
address = ("localhost", 8000)
bind_address = ("localhost", 8001)
client_socketTCP = socket_tcp.SocketTCP()
client_socketTCP.connect(address)
# test 1
message = "Mensje de len=16".encode()
client_socketTCP.send(message)
# test 2
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message)
# test 3
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message)

# test 4: send a file read from standard input
# Usage: python client.py < lorem_ipsum.txt
file_data = sys.stdin.buffer.read()

# First message: file size, so the server knows when to stop reading
client_socketTCP.send(str(len(file_data)).encode())
# Second message: the file content itself
if file_data:
    client_socketTCP.send(file_data)
print(f"Test 4: sent file of {len(file_data)} bytes")

client_socketTCP.close()
print(
    "Cierre cliente: Passed"
    if client_socketTCP._socket.fileno() == -1
    else "Cierre cliente: Failed"
)
