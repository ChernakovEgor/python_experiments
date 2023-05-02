import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = self.command
        print(response)
        
        content = ''
        with open('index.html', 'r') as f:
            content = f.read()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(content, 'utf-8'))


server = HTTPServer(server_address=('localhost', 8000), RequestHandlerClass=HTTPHandler)
server.serve_forever()
