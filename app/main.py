from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import json
from datetime import datetime
import logging
from jinja2 import Environment, FileSystemLoader
import os

def build_logger():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger = logging.getLogger('WebServer')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    return logger

logger = build_logger()

class RequestHandler(BaseHTTPRequestHandler):

    file_path = 'storage/data.json'

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        elif pr_url.path == '/read':
            json_data = self.load_file()
            json_data_converted = [ {"datetime": dt, **details} for dt, details in json_data.items()]
            page = self.generate_message_list_page(json_data_converted)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(page.encode('utf-8'))
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)
    
    def generate_message_list_page(self, json_data):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template("message_list.html")
        return template.render(messages=json_data, )

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def load_file(self):
        json_data = {}
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as fd:
                json.dump(json_data, fd, indent=4)
            logger.info(f"Empty file '{self.file_path}' created.")
        else:
            with open(self.file_path, 'r') as fd:
                json_data = json.load(fd)
            logger.debug(f'Loaded data: {json_data}')
        return json_data
    
    def update_file(self, json_data):
        with open('storage/data.json', 'w') as fd:  
            json.dump(json_data, fd, indent=4)
        logger.debug(f'Save data: {json_data}')       
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        content = self.rfile.read(content_length)
        data_parse = urllib.parse.unquote_plus(content.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

        record_key = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        logger.debug(f'New record key: "{record_key}", data: {data_dict}')

        json_data: json = self.load_file()
        
        json_data[record_key] = data_dict
        self.update_file(json_data)

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

if __name__ == '__main__':
    run()