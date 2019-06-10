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
                characters_final = 6 + response[4]
                beginning_final = characters_final + length
                num_of_sizes = response[5]
                sizes = []
                for i in range(0, num_of_sizes):
                    sizes.append(int.from_bytes(
                        response[beginning_final + (i*2):beginning_final + (i*2) + 2], byteorder='big'))
                daemon_ids_creator.compute(
                    length,
                    int.from_bytes(response[2:4], byteorder='big'),
                    response[6:characters_final].decode("utf-8"),
                    response[characters_final:beginning_final].decode("utf-8"),
                    sizes
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
