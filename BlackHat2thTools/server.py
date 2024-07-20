#!/usr/bin/python3

import socket
import threading

IP = '0.0.0.0'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 先指定服务器应该监听哪个IP地址和端口。
    server.bind((IP, PORT))
    # 让服务器开始监听，并把最大连接数设为5。
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')
    # 让服务器进入主循环中，并在该循环中等待外来连接。
    while True:
        # 当一个客户端成功建立连接的时候，
        # 将接收到的客户端socket对象保存到client变量中，
        # 将远程连接的详细信息保存到address变量中。
        client, address = server.accept()

        print(f'[*] Accepted connection form {address[0]}:{address[1]}')
        # 创建一个新的线程，让它指向handle_client函数，并传入client变量。
        client_handler = threading.Thread(target=handle_client(), args=(client,))
        # 创建好后，我们启动这个线程来处理刚才收到的连接。
        client_handler.start()
        # 与此同时服务端的主循环也已经准备好处理下一个外来连接。

# handle_client函数会调用recv()接收数据，并给客户端发送一段简单的回复。
def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == '__main__':
    main()
