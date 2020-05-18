from wsgiref.simple_server import make_server, demo_app


with make_server('', 8000, demo_app) as httpd:
    httpd.serve_forever()
    httpd.handle_request()
