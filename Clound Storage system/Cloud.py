import socket
import os
from threading import Thread
from pyngrok import ngrok
import time


class ClientThread(Thread):
    def __init__(self, client_socket, client_address):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        print("[+] New thread started for "+str(client_address))
    
    def run(self):
        while True:
            message = self.client_socket.recv(1024).decode()
            if not message:
                break
            print("Received message from "+str(self.client_address)+": "+message)
            print(message)
            if message == "upload":
                filename = self.client_socket.recv(1024).decode()
                filename=filename.split("//")[0]
                file_size = self.client_socket.recv(1024).decode()
                file_size=file_size.split("//")[0]
                file_size=int(file_size)
                print("Received upload request for "+filename+", "+str(file_size)+" bytes")
                file_path = os.path.join(os.getcwd(), filename)
                with open(file_path, "wb") as f:
                    while file_size > 0:
                        data = self.client_socket.recv(1024)
                        f.write(data)
                        file_size -= len(data)
                print("File "+filename+" uploaded successfully")
            elif message == "download":
                filename = self.client_socket.recv(1024).decode()
                if os.path.isfile(filename):
                    file_size = os.path.getsize(filename)
                    print("Sending file "+filename+", "+str(file_size)+" bytes")
                    self.client_socket.send(str(file_size).encode())
                    time.sleep(0.5)
                    with open(filename, "rb") as f:
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            self.client_socket.sendall(data)
                            time.sleep(0.5)
                    print("File "+filename+" sent successfully")
                else:
                    print("File "+filename+" not found")
                    self.client_socket.send("error".encode())
                    time.sleep(0.5)
            elif message == "list":
                files = [f for f in os.listdir('.') if os.path.isfile(f)]
                print("Sending file list: "+str(files))
                self.client_socket.send(str(files).encode())
            else:
                print("Invalid message")
        self.client_socket.close()
        print("[-] Thread closed for "+str(self.client_address))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))
server_socket.listen(5)
print("[*] Server started")

public_url = ngrok.connect(8000, "tcp").public_url
port_number=public_url.split(":")[-1]
print(f"[*] Ngrok tunnel is live at: {public_url}")

public_url=public_url.replace("tcp://", "").split(":")[0]
ip_address = socket.gethostbyname(public_url)

print(f"The IP address is {ip_address}")

print(f"The Port number is {port_number}")





while True:
    client_socket, client_address = server_socket.accept()
    new_thread = ClientThread(client_socket, client_address)
    new_thread.run()
