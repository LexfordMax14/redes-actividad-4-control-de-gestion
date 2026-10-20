import sys

import socket_tcp

# CLIENT
mode = "stop_and_wait" if "--stop-and-wait" in sys.argv else "go_back_n"
address = ("localhost", 8000)
bind_address = ("localhost", 8001)
client_socketTCP = socket_tcp.SocketTCP()
client_socketTCP.set_congestion_control("--sin-control" not in sys.argv)
client_socketTCP.set_debug("--debug" in sys.argv)
client_socketTCP.connect(address)
# test 1
message = "Mensje de len=16".encode()
client_socketTCP.send(message, mode=mode)
# test 2
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message, mode=mode)
# test 3
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message, mode=mode)

# test 4: send a file read from standard input
# Linux: python3 client.py < lorem-ipsum.txt
file_data = sys.stdin.buffer.read()

# First message: file size, so the server knows when to stop reading
client_socketTCP.send(str(len(file_data)).encode(), mode=mode)
# Second message: the file content itself
if file_data:
    client_socketTCP.send(file_data, mode=mode)
print(f"Test 4: sent file of {len(file_data)} bytes")

client_socketTCP.close()
print(
    "Cierre cliente: Passed"
    if client_socketTCP._socket.fileno() == -1
    else "Cierre cliente: Failed"
)
