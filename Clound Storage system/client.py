import socket
import os
import time

server_address = str(input("Enter server address: "))
server_port = int(input("Enter server port: "))


def upload_file(client_socket, filename):
    if not os.path.isfile(filename):
        print("File "+filename+" not found")
        return
    file_size = os.path.getsize(filename)
    client_socket.send("upload".encode())
    client_socket.send((str(filename)+"//").encode())
    time.sleep(0.5)
    client_socket.send((str(file_size)+"//").encode())
    with open(filename, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            client_socket.sendall(data)
            time.sleep(0.5)
    print("File "+filename+" uploaded successfully")

def download_file(client_socket, filename):
    client_socket.send("download".encode())
    client_socket.send(filename.encode())
    file_size = client_socket.recv(1024).decode()
    if file_size == "error":
        print("File "+filename+" not found")
        return
    file_size = int(file_size)
    print("Receiving file "+filename+", "+str(file_size)+" bytes")
    file_path = os.path.join(os.getcwd(), filename)
    with open(file_path, "wb") as f:
        while file_size > 0:
            data = client_socket.recv(1024)
            f.write(data)
            file_size -= len(data)
    print("File "+filename+" received successfully")

def list_files(client_socket):
    client_socket.send("list".encode())
    files = eval(client_socket.recv(1024).decode())
    print("Files on server:")
    for file in files:
        print(file)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((server_address, server_port))
    print("Connected to server "+server_address+":"+str(server_port))
    while True:
        command = input("Enter command (upload, download, list, exit): ")
        if command == "upload":
            filename = input("Enter filename: ")
            
            upload_file(client_socket, filename)
        elif command == "download":
            filename = input("Enter filename: ")
            download_file(client_socket, filename)
        elif command == "list":
            list_files(client_socket)
        elif command == "exit":
            break
        else:
            print("Invalid command")    
    client_socket.close()
    print("Connection closed")
