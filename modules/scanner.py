import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def scan_port(target, port, timeout=1):
    """Try connecting to one port. Return port number if open, None if closed."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            return port  # return the open port number
        return None
    except:
        return None


def run_scan(target, port_range=(1, 1024), threads=100, timeout=1):
    """
    Scan a range of ports using multiple threads.
    Returns a list of open port numbers.
    """
    print(f"\n[*] Scanning {target} — ports {port_range[0]}-{port_range[1]}")
    print(f"[*] Using {threads} threads | timeout: {timeout}s")
    print(f"[*] Started at {datetime.now().strftime('%H:%M:%S')}\n")

    open_ports = []
    ports_to_scan = range(port_range[0], port_range[1] + 1)

    # ThreadPoolExecutor runs scan_port() on many ports simultaneously
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Submit all port scans at once
        futures = {
            executor.submit(scan_port, target, port, timeout): port
            for port in ports_to_scan
        }
        # Collect results as they complete
        for future in futures:
            result = future.result()
            if result:  # if port was open
                open_ports.append(result)
                print(f"  [+] Port {result}/tcp  OPEN")

    open_ports.sort()  # sort numerically
    print(f"\n[*] Scan complete. {len(open_ports)} open ports found.")
    return open_ports