# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# !/usr/bin/python3
import socket

def tcp_client():
    target_host = "www.baidu.com"
    target_port = 80

    # create a socket object
    # AF_INET参数表示我们将使用标准的IPv4地址或主机名，SOCK_STREAM表示这是一个TCP客户端。
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # create the client
    # 然后，我们将该客户端连接到服务器
    client.connect((target_host, target_port))
    # send some data
    # 并发送一些bytes类型的数据。
    client.send(b"GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n")
    # receive some data
    # 最后一步，接收返回的数据并将其打印到屏幕上。
    response = client.recv(4096)
    print(response.decode())
    client.close()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    tcp_client()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/























