import argparse
import asynchat
import asyncore
import logging
import mimetypes
import multiprocessing
import os
import socket
# urllib?
# from urlparse import parse_qs
import urllib  
from time import gmtime, strftime


def url_normalize(path):
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1+3:]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = path.replace("/.", "")
    return path


class FileProducer(object):

    def __init__(self, file, chunk_size=4096):
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""


class AsyncServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=9000):
        pass

    def handle_accepted(self):
        pass

    def serve_forever(self):
        #create an INET, STREAMing socket
        sock = socket.socket(
            socket.AF_INET, 
            socket.SOCK_STREAM)
        #
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        #bind the socket to a public host,
        # and a well-known port
        sock.bind(("127.0.0.1", 9000))
        #become a server socket
        sock.listen(128)
        print("Starting TCP Server")
        try:
            while True:
                clientsocket, _ = sock.accept()
                #take care about users data
                # why 1024?
                data = clientsocket.recv(16384)
                #send result to user
                clientsocket.sendall(data)
                print(data)
                
                #for close sock uncomment this 
                #clientsocket.close()
        except KeyboardInterrupt:
            
            print("Shutting down")
        finally:
            sock.close()


class AsyncHTTPRequestHandler(asynchat.async_chat):

    def __init__(self, sock):
        pass

    def collect_incoming_data(self, data):
        pass

    def found_terminator(self):
        pass

    def parse_request(self):
        pass

    def parse_headers(self):
        pass

    def handle_request(self):
        pass

    def send_header(self, keyword, value):
        pass

    def send_error(self, code, message=None):
        pass

    def send_response(self, code, message=None):
        pass

    def end_headers(self):
        pass

    def date_time_string(self):
        pass

    def send_head(self):
        pass

    def translate_path(self, path):
        pass

    def do_GET(self):
        pass

    def do_HEAD(self):
        pass

    responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        400: ('Bad Request',
            'Bad request syntax or unsupported method'),
        403: ('Forbidden',
            'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
            'Specified method is invalid for this resource.'),
    }


def parse_args():
    parser = argparse.ArgumentParser("Simple asynchronous web-server")
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=9000)
    parser.add_argument("--log", dest="loglevel", default="info")
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    parser.add_argument("-r", dest="document_root", default=".")
    return parser.parse_args()

def run():
    server = AsyncServer(host=args.host, port=args.port)
    server.serve_forever()

def client_handler(sock, address, port):
    while True:
        try:
            message = sock.recv(1024)
            logging.debug(f"Recv: {message} from {address}:{port}")
        except OSError:
            break

        if len(message) == 0:
            break

        sent_message = message
        while True:
            sent_len = sock.send(sent_message)
            if sent_len == len(sent_message):
                break
            sent_message = sent_message[sent_len:]
        logging.debug(f"Send: {message} to {address}:{port}")
    sock.close()
    logging.debug(f"Bye-bye: {address}:{port}")

if __name__ == "__main__":
    args = parse_args()
    logging.basicConfig(
        filename=args.logfile,
        level=getattr(logging, args.loglevel.upper()),
        format="%(name)s: %(process)d %(message)s")
    log = logging.getLogger(__name__)

    DOCUMENT_ROOT = args.document_root
    for _ in range(args.nworkers):
        p = multiprocessing.Process(target=run)
        p.start()
