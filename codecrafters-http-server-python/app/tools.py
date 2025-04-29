import socket
import re
from app.modules import Request


def proccess_connection(
    connection: socket.socket, path_bindings: dict, directory: str = None
):
    while True:
        buf = connection.recv(1024)

        if len(buf) <= 0:
            continue

        if buf.decode() == "close":
            break
        request = Request(connection, buf, directory)

        request.update_headers(
            {"Content-Type": "text/plain"}
        )  # by defualt all are text

        paths = path_bindings[request.method]

        if request.encoding and "gzip" in request.encoding:
            request.update_headers({"Content-Encoding": "gzip"})

        for path in paths.keys():
            search_path = re.search(path, request.path)
            if search_path:
                search_path = path
                break

        
        if search_path:
            result, status_code = paths[search_path](req=request)
            headers = {}
            if "Connection" in request.headers.keys():
                headers = {"Connection": "close"}

            request.response(body=result, headers=headers, status_code=status_code)

            if "Connection" in headers.keys():
                if request.headers["Connection"] == "close":
                    break

        else:
            connection.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())

    connection.close()
