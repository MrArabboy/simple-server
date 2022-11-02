from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import contextlib

import env
from api.selector import get_all_incoming_alarms

hostName = env.SERVER_HOSTNAME
hostPort = env.SERVER_PORT


class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(get_all_incoming_alarms().encode())



myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), f"Server Starts - {hostName}:{hostPort}")

with contextlib.suppress(KeyboardInterrupt):
    myServer.serve_forever()
myServer.server_close()
print(time.asctime(), f"Server Stops - {hostName}:{hostPort}")
