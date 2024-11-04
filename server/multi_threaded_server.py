""""
CH4ESE - Conversion Helper 4 Easy Serialization of EXI
Copyright 2024, Battelle Energy Alliance, LLC
"""

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from time import time
from exi_conversions.conversions import decode_exi, encode_xml
import log


class RequestHandler(BaseHTTPRequestHandler):
    def log_request(self, code="200", size=None):
        """overrides the http server's request logging to prevent console cluttering"""
        return

    def _set_response(self, data):
        """writes the data back to the client"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        """Handle GET requests to check server status"""
        response = "Server is up!"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", len(response))
        self.end_headers()
        self.wfile.write(bytes(response, encoding="utf-8"))

    def do_POST(self):
        """Handles POST Requests"""
        mode = self.headers.get("Format")

        if mode is None:
            self._set_response(bytes("Error: Format Header Required", encoding="utf-8"))
            return

        user_data = self.rfile.read(int(self.headers.get("content-length"))).decode("utf-8")

        log.logger.info("=============================New Request=============================")
        log.logger.info(f"Client Message: {user_data}\n")
        
        start = time()
        if mode.upper() == "EXI":
            # encodes user input into XML format and sends it back to the client
            result = decode_exi(bytes.fromhex(user_data), grammar, gateway)
            self._set_response(bytes(result, encoding="utf-8"))
            log.logger.info(f"Server Response: {result}\n")
        elif mode.upper() == "XML":
            # encodes XML input into an EXI message and sends it back to the client
            result = encode_xml(user_data, grammar, gateway)
            self._set_response(bytes(result, encoding="utf-8"))
            log.logger.info(f"Server Response: {result}\n")
        else:
            self._set_response(bytes("Invalid Format Header. Use 'EXI' or 'XML'", encoding="utf-8"))
        end = time()

        log.logger.info(f"Client Address: {self.client_address[0]}:{self.client_address[1]}")
        log.logger.info(f"Conversion Time: {end-start}")
        log.logger.info("=============================End Request=============================\n")

def run(port, gramm, gate):
    """Starts the Multi-Threaded Python Web Server"""

    global grammar
    global gateway

    grammar = gramm
    gateway = gate
    
    server = ThreadingHTTPServer(("0.0.0.0", port), RequestHandler)
    log.logger.info(f"Web Server accessible at http://localhost:{port}\n")
    server.serve_forever()
