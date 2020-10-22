import os
import socket
from enum import Enum
from socket import SOL_SOCKET, SO_REUSEADDR
from threading import Thread

from request import HttpRequest
from response import HttpResponse, HttpResponse404

DOCUMENT_ROOT = "./resource/server"


class ServerMessage(Enum):
    WAITING_CONNECTION = "Waiting for connection from client."
    CONNECTED = "Client connected."
    CONNECTION_CLOSED = "Connection closed."


class TcpServer:
    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind(("localhost", 8090))
            server_socket.listen(1)
            print(ServerMessage.WAITING_CONNECTION.value)

            while True:
                client_socket, address = server_socket.accept()
                print(ServerMessage.CONNECTED.value)

                request = HttpRequest(client_socket.recv(4096))

                with open("./resource/server/recv.txt", "wb") as f:
                    f.write(request.as_bytes())

                print(f"requested resouce is {DOCUMENT_ROOT + request.path}")

                try:
                    with open(DOCUMENT_ROOT + request.path, "rb") as f:
                        content = f.read()
                except FileNotFoundError:
                    thread = HttpResponseThread(client_socket, HttpResponse404())

                else:
                    ext = request.path.split(".")[-1]
                    if ext == "html":
                        content_type = "text/html"
                    elif ext == "css":
                        content_type = "text/css"
                    elif ext == "js":
                        content_type = "text/javascript"

                    thread = HttpResponseThread(
                        client_socket, HttpResponse(content, content_type)
                    )

                thread.start()


class HttpResponseThread(Thread):
    def __init__(self, sock, response: HttpResponse, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = sock
        self.response = response

    def run(self):
        self.socket.send(self.response.as_bytes())
        self.socket.close()
        print(ServerMessage.CONNECTION_CLOSED.value)


if __name__ == "__main__":
    TcpServer().main()
