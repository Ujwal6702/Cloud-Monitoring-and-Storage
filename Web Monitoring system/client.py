import socket
import pickle

server_address = str(input("Enter server address: "))
server_port = int(input("Enter server port: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((server_address, server_port))
    print("Connected to server "+server_address+":"+str(server_port))
    
    while True:
        try:

            data = client_socket.recv(1024).decode()

            tup=data.split()
            
            print(f"Time: {tup[0]} {tup[1]}, Ip: {tup[2]}, Website: {tup[3]}")
        except:
            pass
    