from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "message": "API funcionando!"}).encode())
            return
        
        if self.path == '/api/leads':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            leads = [{"id": 1, "name": "Test", "company": "Test Corp"}]
            self.wfile.write(json.dumps(leads).encode())
            return
        
        self.send_response(404)
        self.end_headers()