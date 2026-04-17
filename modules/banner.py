import socket

# Common ports and their service names — extend this list!
SERVICE_NAMES = {
    21: "FTP",   22: "SSH",    23: "Telnet",
    25: "SMTP",  53: "DNS",    80: "HTTP",
    110: "POP3", 143: "IMAP",  443: "HTTPS",
    445: "SMB",  3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB"
}


def grab_banner(target, port, timeout=2):
    """
    Connect to an open port and read its banner (service greeting).
    Returns dict with port, service name, and banner text.
    """
    service = SERVICE_NAMES.get(port, "Unknown")
    banner = "No banner"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))

        # For HTTP, we need to SEND a request first to get a response
        if port in [80, 8080, 8443]:
            sock.send(b"HEAD / HTTP/1.0\r\nHost: target\r\n\r\n")

        # Read up to 1024 bytes of the response
        raw = sock.recv(1024)
        sock.close()

        # Decode bytes to string, remove junk characters
        banner = raw.decode("utf-8", errors="ignore").strip()
        # Keep only first line (the important part)
        banner = banner.split("\n")[0][:200]  # max 200 chars

    except:
        pass  # some ports don't respond — that's fine

    return {
        "port": port,
        "service": service,
        "banner": banner
    }


def grab_all_banners(target, open_ports):
    """Grab banners for all open ports. Returns list of dicts."""
    print("\n[*] Grabbing service banners...")
    results = []
    for port in open_ports:
        info = grab_banner(target, port)
        results.append(info)
        print(f"  [+] {port}/tcp ({info['service']}) — {info['banner'][:60]}")
    return results