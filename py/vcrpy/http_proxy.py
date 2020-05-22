from bottle import Bottle, run, request
import requests


app = Bottle()


@app.route("/", method="ANY")
def proxy():
    lines = []
    for k, v in request.headers.items():
        lines.append(f"{k}={v}")
    body = "<br>".join(lines)

    body += request.body.read().decode()
    return body


def main():
    port = 8000
    host = "localhost"
    run(app, host=host, port=port)


if __name__ == "__main__":
    main()
