import logging
from bottle import Bottle, run, request
import requests


app = Bottle()


@app.route("<url:re:.*>", method="ANY")
def proxy(url):
    headers = dict(**request.headers)
    headers["X-FORWARDED-FOR"] = request.remote_addr

    req_params = {
        "method": request.method,
        "url": url,
        "headers": headers,
    }
    req_params['data'] = request.body.read()

    res = requests.request(**req_params)
    return res.text


def main():
    port = 8000
    run(app, port=port)


if __name__ == "__main__":
    main()
