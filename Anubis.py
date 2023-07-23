import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((ip, port))

        if result == 0:
            sock.close()
            return port

        sock.close()
    except socket.error:
        pass

    return None

def scan_ports(target_ip, port_range):
    open_ports = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(scan_port, target_ip, port): port for port in port_range}

        for future in futures:
            port = futures[future]
            result = future.result()
            if result:
                open_ports.append(result)

    return open_ports

if __name__ == "__main__":
    target_ip = input("➜ Enter the target IP address: ")
    start_port = int(input("➜ Enter the starting port: "))
    end_port = int(input("➜ Enter the ending port: "))

    port_range = range(start_port, end_port + 1)

    open_ports = scan_ports(target_ip, port_range)

    if open_ports:
        print("Open Ports:")
        for port in open_ports:
            print(f"Port {port} is open.")
    else:
        print("No open ports were found.")
