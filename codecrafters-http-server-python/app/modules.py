from app.status_codes import status_codes
import gzip


class Request:
    def __init__(self, connection, buffer, directory=None):
        self.connection = connection
        self.buffer = buffer
        self.directory = directory
        self.response_headers = {}
        self._excract_request(self.buffer.decode())
        self._set_reqiust_utilities()

    def __repr__(self):
        return f"Request(path={self.path}, method={self.method}, httpv={self.httpv}"

    def _prccess_headers(self, headers_list: list) -> dict:
        headers = {}
        for header in headers_list:
            header = header.split(":", 1)
            if len(header) == 2:
                title, value = header[0], str(header[1]).strip()
                headers[title] = value

        return headers

    def _get_headers_string(self, headers: dict):
        headers_str = ""

        for header, value in headers.items():
            headers_str += f"{header}: {value}\r\n"

        return headers_str

    def _excract_request(self, buffer: str):
        data = buffer.split("\r\n")
        req_line = data[0].split(" ")
        method, path, httpv = req_line[0], req_line[1], req_line[2]
        headers = self._prccess_headers(data[1:-1])
        self.path = path
        self.method = method
        self.httpv = httpv
        self.headers = headers
        self.body = data[-1]

    def _set_reqiust_utilities(self):
        self.encoding = None

        if "Accept-Encoding" in self.headers.keys():
            self.encoding = self.headers["Accept-Encoding"].replace(" ", "").split(",")

    def _status_code(self, status_code):
        return status_codes[status_code]["message"]

    def _prepare_response_body(self, body):
        if body is None:
            return "".encode()
        if self.encoding:
            if "gzip" in self.encoding:
                return gzip.compress(body.encode())

            return body.encode()

        else:
            return body.encode()

    def update_headers(self, headers: dict):
        self.response_headers.update(headers)

    def response(self, body, headers, status_code):
        status_code = str(status_code)
        request_line = f"HTTP/1.1 {status_code} {self._status_code(status_code)}"
        body = self._prepare_response_body(body)
        self.update_headers({"Content-Length": len(body) if body else 0})
        self.update_headers(headers)
        headers = self._get_headers_string(self.response_headers)
        response = f"{request_line}\r\n{headers}\r\n".encode()
        response += body
        self.connection.sendall(response)
