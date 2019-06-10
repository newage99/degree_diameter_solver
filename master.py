import socketserver
import threading
import requests
import time

server_on = True
length = 4
every = 1000
characters = "xyn+-*/%()1257"
beginning = "xxx"


def update_public_ip_thread():
    while server_on:
        try:
            requests.post("http://myaurea.es/wp-json/wp/v2/posts/12535",
                          headers={
                              "Content-Type": "application/json",
                              "Authorization": "Basic aWduYXNpOmpGQkkkSVJPdVNUaUZRJlB4YV5la1NZbA=="
                          },
                          data='{"title": "' + requests.get("https://api.ipify.org", timeout=10).text + '"}',
                          timeout=10)
        except Exception as e:
            print(e)
        time.sleep(3600)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global server_on, length, every, characters, beginning
        print("tcp_handler: New client connected! " + str(self.client_address))
        self.request.sendall(length.to_bytes(1, byteorder='big') +
                             every.to_bytes(2, byteorder='big') +
                             len(characters).to_bytes(1, byteorder='big') +
                             bytes(characters, 'utf-8') +
                             bytes(beginning, 'utf-8'))
        client_connected = True
        while client_connected and server_on:
            try:
                message, address = self.request.recvfrom(65536)
                message_size = len(message)
                if message_size <= 0:
                    print("tcp_handler: Client " + str(self.client_address) + " disconnected.")
                    client_connected = False
                else:
                    # TODO
                    a = 0
            except Exception as e:
                print("tcp_handler: " + str(e))
                print("tcp_handler: Closing connection with " + str(self.client_address) + " due to exception.")
                client_connected = False
        try:
            time.sleep(1)
            self.request.sendall(bytes([0]))
        except Exception as e:
            print("tcp_handler (sending close msg): " + str(e))


if __name__ == "__main__":
    # global characters, every, length, beginning
    print("Starting update public ip thread...")
    threading.Thread(target=update_public_ip_thread).start()
    tcp_server = None
    print("Server ON")
    while server_on:
        try:
            command = input('')
            if command.startswith('length'):
                length = int(command.split()[1])
            elif command.startswith('every'):
                every = int(command.split()[1])
            elif command.startswith('beginning'):
                start = command.split()[1]
            elif command.startswith('characters'):
                characters = command.split()[1]
            elif command == 'start':
                socketserver.TCPServer.allow_reuse_address = True
                tcp_server = ThreadedTCPServer(("localhost", 9999), ThreadedTCPRequestHandler)
                server_thread = threading.Thread(target=tcp_server.serve_forever)
                server_thread.daemon = True
                server_thread.start()
                print("TCP request handler started")
            elif command == 'exit':
                server_on = False
                if tcp_server is not None:
                    tcp_server.shutdown()
                    tcp_server.server_close()
                print("Server OFF")
        except Exception as e:
            print("Error parsing command: " + str(e))
