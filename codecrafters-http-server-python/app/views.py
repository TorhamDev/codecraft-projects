def root(req):
    return "", 200


def echo(req):
    echo = req.path.split("/")[-1]
    return echo, 200


def user_agent(req):
    return req.headers["User-Agent"], 200


def send_file(req):
    req.update_headers({"Content-Type": "application/octet-stream"})
    file_path = req.directory + req.path.split("/")[-1]

    try:
        with open(file_path, "rb") as f:
            return f.read().decode(), 200
    except FileNotFoundError:
        return None, 404


def create_file(req):
    req.update_headers({"Content-Type": "application/octet-stream"})
    file_path = req.directory + req.path.split("/")[-1]

    try:
        with open(file_path, "wb") as f:
            f.write(req.body.encode())
            return req.body, 201

    except FileNotFoundError:
        None, 404
