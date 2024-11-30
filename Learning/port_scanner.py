import nmap3
from openpyxl import Workbook
import json
import time

def scan(ip, default=100, args='-sV'):
    scanner = nmap3.Nmap()
    ports = scanner.scan_top_ports(ip)
    return ip, ports

def write_to_excel_sheet(ip, data, ws):
    try:
        scanned_ip = ip
        ip_datas = data[ip].get('ports',"")
        if ip_datas:
            for ip_data in ip_datas:
                # 端口协议
                port_col = ip_data.get('protocol','')
                # 端口号
                port_id = ip_data.get('portid','')
                # 端口服务
                port_service = ip_data.get('service','').get('name','')
                ws.append([scanned_ip,port_id,port_col,port_service])
    except PermissionError:
        print("文件可能处于打开状态，请关闭后重试。")

def read_from_txt(filename):
    try:
        with open(filename,'r') as f:
            return [i.strip() for i in f.readlines()]
    except FileNotFoundError:
        print("文件不存在，请检查文件名")

if __name__ == '__main__':
    start = time.time()
    ips = read_from_txt('ip.txt')
    wb = Workbook()
    ws = wb.active
    ws.append(["IP","开放端口","端口协议","端口服务"])
    for ip in ips:
        data = scan(ip, 100, args='')
        write_to_excel_sheet(data[0], data[1], ws)
    wb.save(f'端口扫描初步.xlsx')
    print("保存成功！")

    end = time.time()
    cost = end - start
    print(f"扫描完成,耗时{cost:.2f}秒")