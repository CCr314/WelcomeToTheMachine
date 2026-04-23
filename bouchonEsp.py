import requests

from http.server import HTTPServer, BaseHTTPRequestHandler

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type','text/plain; charset=utf-8')
        self.end_headers()
        if self.path=="/info":
            self.wfile.write(b"Sequence 5 (Photo - intro) equipe 1")
        else:
            self.wfile.write(b"OK")
        if self.path == '/quit':
            exit()

# lancement serveur HTTP bouchon

httpd = HTTPServer(('localhost',8080),Serv)
print("Serveur HTTP sur 8080")
httpd.serve_forever()
