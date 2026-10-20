import sys

import socket_tcp

# SERVER
mode = "stop_and_wait" if "--stop-and-wait" in sys.argv else "go_back_n"
address = ("localhost", 8000)
server_socketTCP = socket_tcp.SocketTCP()
server_socketTCP.bind(address)
connection_socketTCP, new_address = server_socketTCP.accept()

# test 1
buff_size = 16
full_message = connection_socketTCP.recv(buff_size, mode=mode)
print("Test 1 received:", full_message)
if full_message == "Mensje de len=16".encode():
    print("Test 1: Passed")
else:
    print("Test 1: Failed")

# test 2
buff_size = 19
full_message = connection_socketTCP.recv(buff_size, mode=mode)
print("Test 2 received:", full_message)
if full_message == "Mensaje de largo 19".encode():
    print("Test 2: Passed")
else:
    print("Test 2: Failed")

# test 3
buff_size = 14
message_part_1 = connection_socketTCP.recv(buff_size, mode=mode)
message_part_2 = connection_socketTCP.recv(buff_size, mode=mode)
print("Test 3 received:", message_part_1 + message_part_2)
if (message_part_1 + message_part_2) == "Mensaje de largo 19".encode():
    print("Test 3: Passed")
else:
    print("Test 3: Failed")

# test 4: receive a file and save it to disk
connection_socketTCP.set_debug(True)
size_bytes = connection_socketTCP.recv(16, mode=mode)
file_size = int(size_bytes.decode())

received = b""
while len(received) < file_size:
    chunk = connection_socketTCP.recv(12, mode=mode)
    if not chunk:  # connection closed unexpectedly
        break
    received += chunk

with open("received_file.txt", "wb") as f:
    f.write(received)
print(
    f"Test 4: received {len(received)} of {file_size} bytes -> received_file.txt"
)

connection_socketTCP.recv_close()
print(
    "Cierre servidor: Passed"
    if connection_socketTCP._socket.fileno() == -1
    else "Cierre servidor: Failed"
)
server_socketTCP._socket.close()
