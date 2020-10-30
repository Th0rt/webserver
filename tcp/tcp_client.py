import socket


class TcpClient:
    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                print("try connect to host...")
                sock.connect(("localhost", 8090))
            except Exception as e:
                print("connection failed.", e)
            else:
                print("connection established.")

            with open("resource/client/send.txt", mode="rb") as f:
                for line in f.readlines():
                    sock.send(line)

            with open("resource/client/recv.txt", mode="wb") as f:
                res = sock.recv(4096)
                f.write(res)

        print("connection closed.")


if __name__ == "__main__":
    TcpClient().main()
