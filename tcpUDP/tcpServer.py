import socket
import config
import json
import time
import requests
import threading


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton


@singleton
class TcpServer:
    def __init__(self):
        self.bind_ip = config.tcp_server_ip  # 监听所有可用的接口
        self.bind_port = config.tcp_server_port  # 非特权端口号都可以使用
        # AF_INET：使用标准的IPv4地址或主机名，SOCK_STREAM：说明这是一个TCP服务器
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 服务器监听的ip和端口号
        self.tcp_server_socket.bind((self.bind_ip, self.bind_port))
        print("[*] Listening on %s:%d" % (self.bind_ip, self.bind_port))
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 最大连接数
        self.tcp_server_socket.listen(128)
        # 是否有链接上
        self.b_connect = 0
        self.client = None

    def wait_connect(self):
        # 等待客户连接，连接成功后，将socket对象保存到client，将细节数据等保存到addr
        client, addr = self.tcp_server_socket.accept()
        print("客户端的ip地址和端口号为:", addr)
        self.b_connect = 1
        self.client = client

    def start_server(self):
        # 等待客户连接，连接成功后，将socket对象保存到client，将细节数据等保存到addr
        client, addr = self.tcp_server_socket.accept()
        print("客户端的ip地址和端口号为:", addr)
        print('time:', time.time())
        # 代码执行到此，说明客户端和服务端套接字建立连接成功
        print("[*] Acception connection from %s:%d" % (addr[0], addr[1]))
        while True:
            input_str = 'abcd'
            client.send(input_str.encode())
            client_handler = threading.Thread(target=self.handle_client, args=(client,))
            client_handler.start()
            time.sleep(0.5)

    # 客户处理线程
    def handle_client(self, client):
        recv_data = client.recv(1024)
        print("[*] Received: %s" % recv_data)
        # client_socket.send("hi~".encode())
        # recv_data = client_socket.recv(1024)
        # print("[*] Received: %s" % recv_data)
        # 向客户端返回数据
        data_len = len(recv_data)
        print("接收的数据长度为:", data_len)
        # 对二进制数据进行解码
        recv_content = recv_data.decode("gbk")
        print("接收客户端的数据:", recv_content)

    def close(self):
        self.tcp_server_socket.close()

    def write_data(self,data):
        self.client.send(data.encode())


if __name__ == '__main__':
    obj = TcpServer()
    obj.start_server()
