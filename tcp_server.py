import socket
import os

DOCUMENT_ROOT = "./resource/server"


class TcpServer:
    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("localhost", 8090))
            server_socket.listen(1)
            print("waiting for connection from client.")

            client_socket, address = server_socket.accept()
            print("client connected.")

            msg = client_socket.recv(4096)

            with open("./resource/server/recv.txt", "wb") as f:
                f.write(msg)

            with open(os.path.join(DOCUMENT_ROOT, "send.txt"), "rb") as f:
                http_header = b"\n".join([
                    b"HTTP/ 1.1 200 OK",
                    b"Server: Modoki / 0.1",
                    b"Date: Thu, 24 Sep 2020 06: 24:35 GMT",
                    b"Content - Type: text / html",
                    b"Connection: Close",
                ])

                msg = http_header + b"\n\n" + f.read()

            client_socket.send(msg)

        print("connection closed.")


if __name__ == "__main__":
    TcpServer().main()
