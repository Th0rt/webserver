import os
import socket
from datetime import datetime
from enum import Enum

DOCUMENT_ROOT = "./resource/server"


class ServerMessage(Enum):
    WAITING_CONNECTION = "Waiting for connection from client."
    CONNECTED = "Client connected."
    CONNECTION_CLOSED = "Connection closed."


class TcpServer:
    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("localhost", 8090))
            server_socket.listen(1)
            print(ServerMessage.WAITING_CONNECTION.value)

            client_socket, address = server_socket.accept()
            print(ServerMessage.CONNECTED.value)

            request = HttpRequest(client_socket.recv(4096))

            with open("./resource/server/recv.txt", "wb") as f:
                f.write(request.as_bytes())

            with open(DOCUMENT_ROOT + request.header.path, "rb") as f:
                response = HttpResponse(body=f.read())

            client_socket.send(response.as_bytes())

        print(ServerMessage.CONNECTION_CLOSED.value)


class HttpRequest:
    def __init__(self, raw: bytes):
        self.raw = raw.decode('utf-8')
        s = self.raw.split("\n")
        self.header = HttpRequestHeader(s[0])
        self.body = s[1]

    def __str__(self):
        return self.raw

    def as_bytes(self):
        return self.raw.encode("utf-8")


class HttpRequestHeader:
    def __init__(self, raw: str):
        self.raw = raw
        self.method, self._path, self.protocol = self.raw.split(" ")

    @property
    def path(self) -> str:
        if self._path == "/":
            return "/index.html"
        return self._path

    def __str__(self):
        return self.raw


class HttpResponse:
    server_name = "Modoki"
    server_version = 1

    def __init__(self, body: bytes):
        self.header = HttpResponseHeader(self.server_name, self.server_version)
        self.body = body

    def as_bytes(self) -> bytes:
        return self.header.as_bytes() + b"\n\n" + self.body


class HttpResponseHeader:
    def __init__(self, server_name, server_version):
        self.server_name = f"{server_name}/{server_version}"

    @property
    def http_method(self) -> str:
        return "HTTP/1.1"

    @property
    def status_code(self) -> str:
        return "200 OK"

    @property
    def content_type(self) -> str:
        return "text/html"

    @property
    def connection(self) -> str:
        return "Close"

    @property
    def response_datetime(self) -> str:
        return datetime.now().strftime("%a, %d %b %Y %H:%M:%S")

    def __str__(self) -> str:
        return "\n".join([
            f"{self.http_method} {self.status_code}",
            f"Server: {self.server_name}",
            f"Date: {self.response_datetime} GMT",
            f"Content-Type: {self.content_type}",
            f"Connection: {self.connection}",
        ])

    def as_bytes(self) -> bytes:
        return str(self).encode("utf-8")


if __name__ == "__main__":
    TcpServer().main()
