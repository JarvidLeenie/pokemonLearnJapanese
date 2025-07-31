#!/usr/bin/env python3
"""
Simple TTS Server that executes spd-say commands
Run this server to enable system TTS for the flashcards
"""

import json
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class TTSHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/speak':
            # Get the content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse JSON data
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                lang = data.get('lang', 'en-US')
                
                print(f"Received TTS request: '{text}' in {lang}")
                
                # Execute spd-say command
                try:
                    # Map language codes to spd-say language options
                    lang_map = {
                        'ja-JP': 'ja',
                        'en-US': 'en',
                        'en-GB': 'en',
                        'fr-FR': 'fr',
                        'de-DE': 'de',
                        'es-ES': 'es'
                    }
                    
                    spd_lang = lang_map.get(lang, 'en')
                    
                    # Execute spd-say command
                    cmd = ['spd-say', '-l', spd_lang, text]
                    print(f"Executing: {' '.join(cmd)}")
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0:
                        print("TTS command executed successfully")
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        response = {'status': 'success', 'message': 'TTS executed'}
                        self.wfile.write(json.dumps(response).encode())
                    else:
                        print(f"TTS command failed: {result.stderr}")
                        self.send_response(500)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        response = {'status': 'error', 'message': result.stderr}
                        self.wfile.write(json.dumps(response).encode())
                        
                except subprocess.TimeoutExpired:
                    print("TTS command timed out")
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {'status': 'error', 'message': 'TTS command timed out'}
                    self.wfile.write(json.dumps(response).encode())
                    
                except FileNotFoundError:
                    print("spd-say command not found")
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    response = {'status': 'error', 'message': 'spd-say command not found'}
                    self.wfile.write(json.dumps(response).encode())
                    
            except json.JSONDecodeError:
                print("Invalid JSON data received")
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {'status': 'error', 'message': 'Invalid JSON data'}
                self.wfile.write(json.dumps(response).encode())
                
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Custom logging to show requests
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 3000
    
    print(f"Starting TTS Server on port {port}")
    print("This server will execute spd-say commands for TTS requests")
    print("Make sure spd-say is installed and working")
    print("Press Ctrl+C to stop the server")
    
    try:
        server = HTTPServer(('localhost', port), TTSHandler)
        print(f"Server running at http://localhost:{port}")
        print("Ready to receive TTS requests...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Error: Port {port} is already in use")
            print("Try a different port: python tts_server.py 3001")
        else:
            print(f"Error starting server: {e}")

if __name__ == '__main__':
    main() 