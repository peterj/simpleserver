# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "0.0.0.0"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Print out all the headers -- one per line
        print("--------HEADERS--------", flush=True)
        for line in self.headers:
            print(f"{line}: {self.headers[line]}", flush=True)
        print("-----------------------", flush=True)

        self.respond_OK(self.headers)

    def respond_OK(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(msg, "utf-8"))

try:
    print('Started http server', flush=True)
    server = HTTPServer((hostName, serverPort), MyServer)
    server.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    server.socket.close()

