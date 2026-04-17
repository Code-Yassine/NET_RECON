import whois
import socket


def get_whois_info(target):
    """
    Get Whois registration info for a domain or IP.
    Returns a dict with all available info.
    """
    print(f"\n[*] Running Whois lookup for {target}...")
    info = {"target": target}

    try:
        # Resolve domain to IP first
        info["ip"] = socket.gethostbyname(target)
        print(f"  [+] IP Address : {info['ip']}")
    except:
        info["ip"] = "Could not resolve"

    try:
        w = whois.whois(target)

        # Extract the useful fields
        info["registrar"]    = str(w.registrar or "N/A")
        info["org"]          = str(w.org or "N/A")
        info["country"]      = str(w.country or "N/A")
        info["creation_date"]= str(w.creation_date or "N/A")
        info["expiry_date"]  = str(w.expiration_date or "N/A")
        info["name_servers"] = w.name_servers or []

        # Print summary
        print(f"  [+] Registrar  : {info['registrar']}")
        print(f"  [+] Org        : {info['org']}")
        print(f"  [+] Country    : {info['country']}")
        print(f"  [+] Created    : {info['creation_date']}")

    except Exception as e:
        print(f"  [-] Whois failed: {e}")
        info["error"] = str(e)

    return info