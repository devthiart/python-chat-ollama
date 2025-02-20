import socket
import threading
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def send_message(message):
    response = llm.invoke(message)
    return response

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode('utf-8')

        if not request:
            break

        try:
            print(f"-Client request: {request}")
            result = send_message(request)
            print(f"-AI Response: {result}")
            client_socket.send(str(result).encode('utf-8'))
        except Exception as e:
            client_socket.send("Operation fail.".encode('utf-8'))
            print(e);

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # put your computers's IP address here:
    server.bind(('YOUR_IP_ADDRESS', 12345))
    server.listen(10)
    print("[*] Waiting for connections...")

    while True:
        client, addr = server.accept()
        print(f"[*] Accept connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()
