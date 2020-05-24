import logging
from bottle import Bottle, run, request, HTTPResponse
import requests
import vcr


app = Bottle()


@app.route("<url:re:.*>", method="ANY")
@vcr.use_cassette(record_mode="new_episodes")
def proxy(url):
    headers = dict(**request.headers)
    headers["X-FORWARDED-FOR"] = request.remote_addr

    req_params = {
        "method": request.method,
        "url": url,
        "headers": headers,
    }
    req_params["data"] = request.body.read()

    res = requests.request(**req_params)
    response = HTTPResponse(
        body=res.text, status=res.status_code, headers=dict(res.headers)
    )
    return response


def main():
    port = 8000
    run(app, port=port)


if __name__ == "__main__":
    main()
