import daemon_ids_creator
import daemon
import threading
import requests
import socket
import jsons
import time


class MsgId:
    COMPUTE = 0


def init():
    threading.Thread(target=tcp_thread).start()


def get_master_ip():
    return jsons.loads(requests.get("http://myaurea.es/wp-json/wp/v2/posts?id=12535").text)[0]["title"]["rendered"]


def connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.connect((get_master_ip(), 9999))
        s.connect(("localhost", 9999))
        return s
    except Exception as e:
        print("tcp_thread (connect): " + str(e))
        raise e


def recv_handler(s):
    print("tcp_thread: Correctly connected to master.")
    while daemon.daemon_on:
        s.settimeout(None)
        response = s.recv(65536)
        if response is None or len(response) <= 0:
            daemon.daemon_on = False
        else:
            if response[0] == MsgId.COMPUTE:
                length = response[1]
                characters_length_final = 5 + response[4]
                daemon_ids_creator.compute(
                    length,
                    int.from_bytes(response[2:4], byteorder='big'),
                    response[5:characters_length_final].decode("utf-8"),
                    response[characters_length_final:characters_length_final + length].decode("utf-8")
                )


def tcp_thread():
    while daemon.daemon_on:
        try:
            print("tcp_thread: Connecting to master...")
            s = connect()
            recv_handler(s)
        except:
            pass
        time.sleep(120)
