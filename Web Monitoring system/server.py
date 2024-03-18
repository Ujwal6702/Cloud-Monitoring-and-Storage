import psutil
import queue
import threading
from queue import Queue
import pyshark
import socket
from threading import Thread
from pyngrok import ngrok



def get_active_interface():
    connections = psutil.net_connections()
    for c in connections:
        if c.status == "ESTABLISHED":
            local_addr, local_port = c.laddr
            if local_addr != "127.0.0.1":
                for iface, addrs in psutil.net_if_addrs().items():
                    for addr in addrs:
                        if addr.address == local_addr:
                            return iface
    return None


interface = get_active_interface()

data_queue = queue.Queue()


class ClientThread(Thread):
    def __init__(self, client_socket, client_address):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address
        print("[+] New thread started for "+str(client_address))
    
    def run(self):
        while True:
            try:
                website_ip, website_url, timestamp = data_queue.get()
                data = f"{str(timestamp)} {str(website_ip)} {str(website_url)}"
                print(data)
                self.client_socket.sendall(data.encode())
                
            except:
                pass

def process_data():
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

def tls_packet_callback(pkt):
    try:
        # Check if the packet has an IP layer and a TLS layer
        if 'IP' in pkt and 'TLS' in pkt:
            website_ip = pkt['IP'].dst
            try:
                website_url = pkt['TLS'].get('tls.handshake.extensions_server_name')
            except:
                website_url = pkt['TLS'].get('tls.handshake.extensions_client_hello_server_name')
            if website_url is None:
                website_url = pkt['TLS'].get('tls.handshake.extensions_client_hello_server_name')
                
            timestamp = pkt.sniff_time.strftime('%Y-%m-%d %H:%M:%S')
            # Add the extracted data to the queue
            if website_url:
                data_queue.put((website_ip, website_url, timestamp))
    except:
        pass

# Define a callback function to extract the required data for HTTP packets
def http_packet_callback(pkt):
    try:
        # Check if the packet has an IP layer and an HTTP layer
        if 'IP' in pkt and 'HTTP' in pkt:
            website_ip = pkt['IP'].dst
            try:
                website_url = pkt['HTTP'].get('request.full_uri')
            except:
                website_url = pkt['HTTP'].get('host')
            if website_url is None:
                website_url = pkt['HTTP'].get('host')
            timestamp = pkt.sniff_time.strftime('%Y-%m-%d %H:%M:%S')
            # Add the extracted data to the queue
            if website_url and 'host' in website_url.lower():
                data_queue.put((website_ip, website_url, timestamp))
    except:
        pass

process_thread = threading.Thread(target=process_data)
process_thread.start()


tls_capture = pyshark.LiveCapture(interface=interface, bpf_filter='tcp')
for packet in tls_capture.sniff_continuously():
    tls_packet_callback(packet)
    http_packet_callback(packet)

