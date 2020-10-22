import os
import socket
from enum import Enum
from socket import SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from typing import Callable, List, Tuple

from request import HttpRequest
from response import HttpResponse, HttpResponse404
from wsgi_application import WSGIApplication

DOCUMENT_ROOT = "./resource/server"


class ServerMessage(Enum):
    WAITING_CONNECTION = "Waiting for connection from client."
    CONNECTED = "Client connected."
    CONNECTION_CLOSED = "Connection closed."


class WSGIServer:
    def __init__(self, application):
        self.env: dict = {}
        self.application = application

    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind(("localhost", 8090))
            server_socket.listen(1)
            print(ServerMessage.WAITING_CONNECTION.value)

            while True:
              client_socket, _ = client_socket.accept()
              request = self.recv_request(client_socket)

              # 今は固定のレスポンスを返す
              response = self.create_response()
              thread = HttpResponseThread(client_socket, response)
              thread.start()

    def recv_request(self, sock: socket):
        recv = sock.recv(4096)
        print(ServerMessage.CONNECTED.value)

        # 確認の為にRequestをファイルに書き出す
        with open("./resource/server/recv.txt", "wb") as f:
            f.write(recv)

        request = HttpRequest(recv)

        print(f"requested resource is {DOCUMENT_ROOT} {request.path}")
        return HttpRequest(recv)

    def start_response(
        self, response_line: bytes, response_headers: List[Tuple[bytes]], exc_info=None
    ):
        self.status_code = response_line
        for env in response_headers:
            key, value = env
            self.env[key] = value

    def create_response(self) -> bytes:
        response_body = b"".join(
            self.application.application(self.env, self.start_response)
        )
        response_line = b"HTTP/1.1 " + self.status_code
        response_header = b"\n".join(
            [b"%s: %s" % (key, value) for key, value in self.env.items()]
        )

        response = b"\n".join(
            [
                response_line,
                response_header,
                b"",
                response_body,
            ]
        )
        return response


class HttpResponseThread(Thread):
    def __init__(self, sock, response: HttpResponse, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = sock
        self.response = response

    def run(self):
        self.socket.send(self.response)
        self.socket.close()
        print(ServerMessage.CONNECTION_CLOSED.value)


if __name__ == "__main__":
    WSGIServer(WSGIApplication()).main()
