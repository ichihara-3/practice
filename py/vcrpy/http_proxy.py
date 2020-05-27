import argparse
from urllib.parse import urlparse, urlunparse, parse_qs
import wsgiref

from bottle import Bottle, run, request, HTTPResponse
import bottle
import requests
import vcr

bottle.debug(True)


class ProxyBottle(Bottle):
    def __call__(self, environ, start_response):
        """Wrapping start_response to filter headers,
        because hop-by-hop headers are not allowed in wsgi implementation.
        """

        def wrapped_start_response(status, headerlist, exc_info=None):
            headerlist = [
                (key, value)
                for key, value in headerlist
                if not wsgiref.util.is_hop_by_hop(key)
            ]
            return start_response(status, headerlist, exc_info)

        return self.wsgi(environ, wrapped_start_response)


app = ProxyBottle()


@app.route("<urlstring:re:.*>", method="ANY")
@vcr.use_cassette(record_mode="new_episodes")
def proxy(urlstring):
    headers = dict(**request.headers)
    headers["X-FORWARDED-FOR"] = request.remote_addr
    parsed = urlparse(urlstring)

    url = urlunparse(list(parsed)[:4] + ["", ""])
    query = parse_qs(parsed[4])

    req_params = {
        "method": request.method,
        "url": url,
        "params": query,
        "headers": headers,
        "data": request.body.read(),
    }

    res = requests.request(**req_params)
    response = HTTPResponse(
        body=res.text, status=res.status_code, headers=dict(res.headers)
    )
    return response


def main():
    args = get_arguments()
    port = args.port

    run(app, port=port)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", "-p", default=8000, type=int, help="port number to serve"
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
