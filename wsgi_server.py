import os
import socket
from enum import Enum
from socket import SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from typing import Callable, List, Tuple

from request import HttpRequest
from response import HttpResponse, HttpResponse404
from wsgi_application import WSGIApplication


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
                client_socket, _ = server_socket.accept()
                request = self.recv_request(client_socket)

                thread = HttpResponseThread(client_socket, request, self.application)
                thread.start()

    def recv_request(self, sock: socket):
        recv = sock.recv(4096)
        print(ServerMessage.CONNECTED.value)

        # 確認の為にRequestをファイルに書き出す
        with open("./resource/server/recv.txt", "wb") as f:
            f.write(recv)

        return HttpRequest(recv)


class HttpResponseThread(Thread):
    def __init__(self, sock, request: HttpRequest, wsgi_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = sock
        self.app = wsgi_app
        self.env = {}
        self.request = request
        self.response = {"line": b"", "header": {}, "body": b""}
        self.status_code = b""

    def get_env(self) -> dict:
        env = dict()
        env["REQUEST_METHOD"] = ""
        env["SCRIPT_NAME"] = ""
        env["PATH_INFO"] = self.request.request_line.path.decode("utf-8")
        env["QUERY_STRING"] = ""
        env["CONTENT_TYPE"] = ""
        env["CONTENT_LENGTH"] = ""
        env["SERVER_NAME"] = ""
        env["SERVER_PORT"] = ""
        env["SERVER_PROTOCOL"] = ""
        return env

    def create_response(self) -> bytes:
        self.response["body"] = b"".join(
            self.app.application(env=self.get_env(), start_response=self.start_response)
        )
        self.response["line"] = b"HTTP/1.1 " + self.status_code
        response_header = b"\n".join(
            [b"%s: %s" % (key, value) for key, value in self.response["header"].items()]
        )

        response = b"\n".join(
            [
                self.response["line"],
                response_header,
                b"",
                self.response["body"],
            ]
        )
        return response

    def run(self):
        self.socket.send(self.create_response())
        self.socket.close()
        print(ServerMessage.CONNECTION_CLOSED.value)

    def start_response(
        self, response_line: bytes, response_headers: List[Tuple[bytes]], exc_info=None
    ):
        self.response["line"] = b"HTTP/1.1 " + response_line
        for key, value in response_headers:
            self.response["header"][key] = value


if __name__ == "__main__":
    WSGIServer(WSGIApplication()).main()
