import socket
from urllib.parse import urlsplit

def make_upstream_call(host, port, data, client):
    try:
        # upstream connection to the destination server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as upstream_socket:
            upstream_socket.connect((host, port))
            upstream_socket.sendall(data)
            
            while True:
                resp = upstream_socket.recv(4096)
                if not resp:
                    break
                client.sendall(resp)

    except Exception as e:
        print(f"Upstream error: {e}")


def handle_client(client, addr):
    with client:
        print(f"Connection from client:{addr}")
    
        while True:
            # Receive data
            received_data = client.recv(4096)
            if not received_data:
                break

            data = received_data.decode()
            print(f"Received data from client: {data}")

            split = data.split()
            url = split[1]
            print(f"url: {url}")

            parsed = urlsplit(url)

            host = parsed.hostname
            print(f"host: {host}")

            dest_port = parsed.port
            if dest_port is None:
                if parsed.scheme == "http":
                    dest_port = 80
                if parsed.scheme == "https":
                    dest_port = 443
            print(f"destination port: {dest_port}")

            make_upstream_call(host, dest_port, received_data, client)
            

def run_proxy_server(host = '127.0.0.1', port = 8888):
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # bind socket to host and port
        server_socket.bind((host, port))

        #listen for incoming connections
        server_socket.listen()

        print(f"Proxy server listening on {host}:{port}")

        while True:
            client_socket, addr = server_socket.accept()
            handle_client(client_socket, addr)
        

if __name__ == "__main__":
    run_proxy_server()