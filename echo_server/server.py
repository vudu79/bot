import os
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

#
class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b'Hello, world!')

        # self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        # self.wfile.write('<title>Простой HTTP-сервер.</title></head>'.encode())
        # self.wfile.write('<body>Был получен GET-запрос.</body></html>'.encode())


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    host = '0.0.0.0'
    # port = os.getenv('PORT', default="8000")
    server_address = ("https://aiogram-bot-gifs.herokuapp.com", 50000)
    httpd = server_class(server_address, handler_class)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("Сервер не запустился!!!!!!!!!!!!!!!!!!")


