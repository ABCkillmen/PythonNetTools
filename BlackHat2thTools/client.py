# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# !/usr/bin/python3
import socket

def tcp_client():
    target_host = "0.0.0.0"
    target_port = 9998

    # create a socket object
    # AF_INET参数表示我们将使用标准的IPv4地址或主机名，SOCK_STREAM表示这是一个TCP客户端。
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # create the client
    # 然后，我们将该客户端连接到服务器
    client.connect((target_host, target_port))
    # send some data
    # 并发送一些bytes类型的数据。
    client.send(b"ABCDEF")
    # receive some data
    # 最后一步，接收返回的数据并将其打印到屏幕上。
    # response = client.recv(4096)

    print(response.decode())
    client.close()

def udp_client():
    target_host = "127.0.0.1"
    target_port = 8888

    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # UDP是一个无连接协议，所以开始通信前不需要用connect()函数建立连接。
    # send some data
    # 调用sendto函数，填好要发送的数据和接收数据的服务器地址就可以了。
    client.sendto(b"AAABBBCCC", (target_host, target_port))
    # receive some data
    # 最后一步，接收返回的数据并将其打印到屏幕上。
    data, addr = client.recvfrom(4096)

    print(data.decode())
    client.close()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    tcp_client()
    # udp_client()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/























