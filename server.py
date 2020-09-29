#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from convert import convert
from urllib.request import Request, urlopen
import os, shutil


def clean_temp():
    folder = "temp"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def download_pdf(url):
    print(url)
    name = "temp/" + url.split("/")[-1]
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urlopen(req)
    if resp.getcode() == 200:
        open(name, "wb").write(resp.read())
        return name
    else:
        return None


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        pass

    # GET sends back a Hello world message
    def do_GET(self):
        if self.path[-4:] == ".pdf":
            clean_temp()
            pdf_name = self.path[1:]
            if pdf_name[:4] == "http":
                pdf_name = download_pdf(pdf_name[pdf_name.index("http"):])
            if not pdf_name:
                self.send_response(404)
                self.end_headers()
                return 0

            mp3_name = convert(pdf_name)
            self.send_response(301)
            self.send_header('Location', URL+"/mp3/"+mp3_name)
            self.end_headers()
        elif self.path[:4] == "/mp3":
            self.send_response(200)
            self.send_header('Content-type', 'application/mp3')
            self.end_headers()

            mp3_name = self.path[5:]
            with open(mp3_name, 'rb') as mp3:
                mp3_content = mp3.read()
                self.wfile.write(mp3_content)

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('charset', 'utf-8')
            self.end_headers()
            self.wfile.write("Hello World\nPaste url to pdf after /".encode('utf-8'))


#HOST_NAME = 'localhost'
HOST_NAME = "192.168.1.34"
PORT_NUMBER = 80
URL = f"http://{HOST_NAME}:{PORT_NUMBER}"

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))
