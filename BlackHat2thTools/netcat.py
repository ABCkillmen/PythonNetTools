import argparse
import socket
import shlex
# subprocess这个库提供了一组强大的进程创建接口，可以通过多种方式调用其他程序。
import subprocess
import sys
import textwrap
import threading

# 这个函数将会接受一条命令并执行，然后将结果作为一段字符串返回。
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    # subprocess用到了它的check_output函数，这个函数会在本机运行一条命令，并返回该命令的输出。
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

class NetCat:
    # main代码块传进来的命令行参数和缓冲区数据，初始化一个NetCat对象
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        # 然后创建一个socket对象
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def run(self):
        # 如果我们的NetCat对象是接收方，run就执行listen函数
        if self.args.listen:
            self.listen()
        # 如果是发送方，run就执行send函数
        else:
            self.send()

    def send(self):
        # 先连接到target和port
        self.socket.connect((self.args.target, self.args.port))
        # 如果这时缓冲区里有数据的话，就先把这些数据发过去。
        if self.buffer:
            self.socket.send(self.buffer)

        # 创建一个try/catch块，这样就能直接用Ctrl+C组合键手动关闭连接
        try:
            # 创建一个大循环，一轮一轮地接收target返回的数据
            while True:
                recv_len = 1
                response = ''
                # 在大循环里，建了一个小循环，用来读取socket本轮返回的数据
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    # 如果socket里的数据目前已经读到头，就退出小循环
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    # 检查刚才有没有实际读出什么东西来，如果读出了什么，就输出到屏幕上，
                    # 并暂停，等待用户输入新的内容，再把新的内容发给target
                    self.socket.send(buffer.encode())
                    # 接着开始下一轮大循环
        # Ctrl+C组合键触发KeyboardInterrupt中断循环
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        # listen函数把socket对象绑定到target和port上
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        # 开始用一个循环监听新连接
        while True:
            client_socket, _ = self.socket.accept()
            # 并把已连接的socket对象传递给handle函数
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    def handle(self, client_socket):
        # 如果要执行命令，handle函数就会把该命令传递给execute函数，然后把输出结果通过socket发回去。
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        # 如果要上传文件，我们就建一个循环来接收socket传来的文件内容
        # 再将收到的全部数据写到参数指定的文件里。
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        # 如果要创建一个shell，创建一个循环，向发送方发一个提示符，然后等待其发回命令。
        # 每收到一条命令，就用execute函数执行它，然后把结果发回发送方。
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    # shell是收到换行符后才执行命令的
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''

                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()


if __name__ == '__main__':
    # 标准库里的argparse库创建了一个带命令行界面的程序
    # 传递不同的参数，就能控制这个程序执行不同的操作
    # 比如上传文件、远程执行命令，或是打开一个命令行shell。
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # 编写了一段帮助信息，程序启动的时候如果发现--help参数，就会显示这段信息。
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.1 -p 6666 -l -c # command shell
            netcat.py -t 192.168.1.1 -p 6666 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.1 -p 6666 -l -e=\"cat /etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.1 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.1 -p 6666 # connect to server
        '''))
    # 添加了6个参数，用来控制程序的行为
    # 使用了-c、-e和-u这三个参数，就意味着要使用-l参数，因为这些行为都只能由接收方来完成。
    # 程序收到-c参数，就会打开一个交互式的命令行shell；
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    # 收到-e参数，就会执行一条命令；
    parser.add_argument('-e', '--execute', help='execute specified command')
    # 收到-l参数，就会创建一个监听器；
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    # -p参数用来指定要通信的端口；
    parser.add_argument('-p', "--port", type=int, default=6666, help='specified port')
    # -t参数用来指定要通信的目标IP地址；
    parser.add_argument('-t', '--target', default='192.168.152.128', help='specified IP')
    # -u参数用来指定要上传的文件。
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    # 如果确定了程序要进行监听，我们就在缓冲区里填上空白数据，把空白缓冲区传给NetCat对象。
    # 反之，我们就把stdin里的数据通过缓冲区传进去。最后调用NetCat类的run函数来启动它。
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()






































