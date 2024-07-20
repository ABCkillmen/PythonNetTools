# 先打开kali监听80端口，再运行udpclient
import socket

target_host = "127.0.0.1"
target_port = 80

def udp_client():
    # 建立一个 socket 对象
    # AF_INET 参数说明我们将使用标准的 IPv4地址或者主机名
    # SOCK_STREAM 说明这将是一个 UDP 客户端
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 发送一些数据
    client.sendto(b"This is test message!", (target_host, target_port))

    # 接收一些数据
    data, addr = client.recvfrom(4096)

    client.close()

if __name__ == '__main__':
    udp_client()

