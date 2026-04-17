import argparse
import sys
from modules.scanner       import run_scan
from modules.banner        import grab_all_banners
from modules.whois_lookup  import get_whois_info
from modules.reporter      import generate_report


def parse_args():
    parser = argparse.ArgumentParser(
        description="Net Recon Toolkit — Port Scanner + Banner Grabber + Whois",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-t", "--target",  required=True,  help="Target IP or domain")
    parser.add_argument("-p", "--ports",   default="1-1024", help="Port range (default: 1-1024)")
    parser.add_argument("-T", "--threads", default=100,    type=int, help="Thread count (default: 100)")
    parser.add_argument("--no-whois",                      action="store_true", help="Skip Whois lookup")
    parser.add_argument("--no-report",                     action="store_true", help="Don't generate HTML report")
    return parser.parse_args()


def parse_port_range(port_str):
    """Parse '1-1024' into (1, 1024). Also handles single port '80'."""
    if "-" in port_str:
        start, end = port_str.split("-")
        return (int(start), int(end))
    return (int(port_str), int(port_str))


def main():
    print("""
  ███╗   ██╗███████╗████████╗    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
  ████╗  ██║██╔════╝╚══██╔══╝    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
  ██╔██╗ ██║█████╗     ██║       ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
  ██║╚██╗██║██╔══╝     ██║       ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
  ██║ ╚████║███████╗   ██║       ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═╝  ╚═══╝╚══════╝   ╚═╝       ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
    [For authorized testing only]
    """)

    args = parse_args()
    target     = args.target
    port_range = parse_port_range(args.ports)

    # ── STEP 1: Whois ──
    whois_data = {}
    if not args.no_whois:
        whois_data = get_whois_info(target)

    # ── STEP 2: Port scan ──
    open_ports = run_scan(target, port_range, args.threads)

    if not open_ports:
        print("[-] No open ports found.")
        sys.exit(0)

    # ── STEP 3: Banner grab ──
    port_data = grab_all_banners(target, open_ports)

    # ── STEP 4: Generate report ──
    if not args.no_report:
        generate_report(target, whois_data, port_data)

    print("\n[✓] Done.")


if __name__ == "__main__":
    main()