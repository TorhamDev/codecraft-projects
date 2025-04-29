import socket
import threading
import argparse

from app.views import root, echo, user_agent, send_file, create_file
from app.tools import proccess_connection

path_bindings = {
    "GET": {
        r"^/$": root,
        r"^/echo/.*": echo,
        r"^/user-agent": user_agent,
        r"^/files/.*": send_file,
    },
    "POST": {
        r"^/files/.*": create_file,
    },
}


def main(directory=None):
    server_socket = socket.create_server(
        ("localhost", 4221), family=socket.AF_INET, reuse_port=True
    )

    while True:
        connection, _ = server_socket.accept()
        thread = threading.Thread(
            target=proccess_connection, args=(connection, path_bindings, directory)
        )
        thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Web server",
        description="Simple Web Server",
        epilog="",
    )
    parser.add_argument("-d", "--directory")
    args = parser.parse_args()
    main(args.directory)
