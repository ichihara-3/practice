from bottle import Bottle, run, request, get, post
import requests


app = Bottle()


@app.route("/")
def proxy():
    lines = []
    for k, v in request.headers.items():
        lines.append(f'{k}={v}')
    return '<br>'.join(lines)




def main():
    port = 8000
    host = "localhost"
    run(app, host=host, port=port)


if __name__ == "__main__":
    main()
