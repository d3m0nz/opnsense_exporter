#!/usr/bin/env python3

import json
import argparse
import requests
import logging
import datetime
import time
from io import StringIO
from flask import Flask
from flask import Response

app = Flask(__name__)

version = 0.1
# define endpoint and credentials
api_key = "bPEbUX9EIVjszp6pgWmePjK0hOhl0X72n5KW9xNEPXaMHAcCnoEiIfEaXxjfK4PJ9/8QZ+6TbaoW8+PI"
api_secret = "NatiQQZyLYD3HNXkrEESvFcZv2yJ9kvvUive22SHSLOqRd9sWOlBPGgA56WmiO5zMMU+oMC3LykaHX3w"
api_url = "https://home.dadoss.com/api/"


def get_json(url):
    response = requests.get(url,
        auth=(api_key, api_secret))
    data = response.text
    io = StringIO(data)
    json_text = json.load(io)
    return response

def convert_json(json_data, name, option):
    items = str()
    for i in json_data:
        items += "opnsense_%s{%s=\"%s\"} %s\n" % (name, option, i, json_data[i])
    return items

def get_status(url):
    status_raw = get_json(url)
    status = "opnsense_exporter_version %s\n" % (version)
    for i in status_raw:
        if i != "status":
            status += "opnsense_%s %s\n" % (i, status_raw[i])
        elif status_raw[i] == 'ok':
            status += "opnsense_status 1\n"
        else:
            status += "opnsense_status 0\n"

    return status	
	
	
@app.route('/')
def index():
    return '''
<html>
    <head><title>OPNSense Exporter</title></head>
             <body>
             <h1>OPNSense Exporter</h1>
             <p><a href='/metrics'>Metrics</a></p>
             </body>
             </html>'''

@app.route('/metrics', methods=['GET'])
def metrics():
    status_raw_url = api_url + 'core/firmware/info'
    items = get_status(status_raw_url)
    return Response(items, mimetype="text/plain")

def main():
    parser = argparse.ArgumentParser(
        description='opnsense_exporter')    
    parser.add_argument('-p', '--port', type=int,
        help='port opnsense_exporter is listening on',
        default=9311)
    parser.add_argument('-i', '--interface',
        help='interface opnsense_exporter will listen on',
        default='0.0.0.0')    
    args = parser.parse_args()


    port = args.port
    interface = args.interface
    
    # Disable werkzeug logging to avoid syslog spam
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.INFO)

    print("* Listening on %s:%s" % (interface, port))
    app.run(host=interface, port=port)





    
if __name__ == '__main__':
    main()

