import socket
import threading
from pyftdi.ftdi import Ftdi
from pyftdi.gpio import GpioAsyncController

gpio1 = GpioAsyncController()
gpio2 = GpioAsyncController()
gpio3 = GpioAsyncController()
gpio4 = GpioAsyncController()
gpio1.configure('ftdi://ftdi:4232:1:6/1', direction=0xFF)
gpio2.configure('ftdi://ftdi:4232:1:6/2', direction=0x00)
gpio3.configure('ftdi://ftdi:4232:1:6/3', direction=0x00)
gpio4.configure('ftdi://ftdi:4232:1:6/4', direction=0x00)

HOST = "0.0.0.0"
#socket.gethostbyname(socket.gethostname())
PORT = 9571

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

def handle_client(conn, addr):
    print(f"[Connected] Connected to {addr[0]}")
    while True:
        message_length = conn.recv(1024).decode('utf-8')
        if(message_length):
            message_length = int(message_length)
            message = conn.recv(message_length).decode('utf-8')
            if(message == "Disconnect!"):
                break
            print(f"[{addr[0]}] {message}")
            gpio1.write(int(message, 2))
            read_data = gpio4.read()
            read_data = bin(read_data)[2::].zfill(8)
            print(f"[Read Data] {read_data}")
            send(conn, read_data)
    print(f"[Disconnected] {addr[0]}")
    conn.close()

def send(conn, message):
    message = message.encode('utf-8')
    message_length = len(message)
    send_length = str(message_length).encode('utf-8')
    send_length += b' ' * (1024 - len(send_length))
    conn.send(send_length)
    conn.send(message)

def start():
    server.listen()
    print(f"[Listening] Listening on {HOST}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[Active Connections] {threading.active_count() - 1}")
        
print("[Starting] Starting server")
start()
