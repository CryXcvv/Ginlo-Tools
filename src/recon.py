import socket
import json
import urllib.request
import subprocess
import platform
from utils import GREEN, WHITE, RESET, DIM, section, end_section, input_prompt

def dns_lookup():
    section("DNS LOOKUP")
    target = input_prompt("  Domain: ")
    if not target:
        end_section()
        return
    try:
        ip = socket.gethostbyname(target)
        print(GREEN + f"  [+] {target} -> {ip}" + RESET)
    except Exception:
        print(WHITE + "  [!] Not found." + RESET)
    end_section()

def reverse_dns_lookup():
    section("REVERSE DNS LOOKUP")
    target = input_prompt("  IP Address: ")
    if not target:
        end_section()
        return
    try:
        hostname, _, _ = socket.gethostbyaddr(target)
        print(GREEN + f"  [+] {target} -> {hostname}" + RESET)
    except socket.herror:
        print(WHITE + "  [!] No PTR record found." + RESET)
    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)
    end_section()

def http_headers():
    section("HTTP HEADER SNIFFER")
    target = input_prompt("  Target: ")
    if not target:
        end_section()
        return

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target, 80))
        s.send(f"HEAD / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n".encode())
        resp = s.recv(4096).decode(errors='ignore')
        s.close()

        print(WHITE + "\n  Headers:" + RESET)
        print(DIM + "  " + "-" * 40 + RESET)
        for line in resp.splitlines():
            if line.strip():
                print(WHITE + "  " + line + RESET)
    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)
    end_section()

def geoip_lookup():
    section("GEOIP LOOKUP")
    target = input_prompt("  IP Address (blank for your IP): ")
    if not target:
        target = ""

    try:
        url = f"http://ip-api.com/json/{target}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,query"
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read().decode())

        if data.get("status") == "fail":
            print(WHITE + f"  [!] {data.get('message', 'Lookup failed')}" + RESET)
            end_section()
            return

        fields = [
            ("IP", "query"),
            ("Country", "country"),
            ("Region", "regionName"),
            ("City", "city"),
            ("ZIP Code", "zip"),
            ("Latitude", "lat"),
            ("Longitude", "lon"),
            ("ISP", "isp"),
            ("Organization", "org"),
            ("AS", "as"),
        ]
        for label, key in fields:
            val = data.get(key, "?")
            if val:
                print(GREEN + f"  {label:<16}" + RESET + ": " + WHITE + str(val) + RESET)

    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)
    end_section()

def public_ip_check():
    section("PUBLIC IP CHECK")
    services = [
        "https://api.ipify.org",
        "https://checkip.amazonaws.com",
        "https://icanhazip.com",
    ]
    for svc in services:
        try:
            with urllib.request.urlopen(svc, timeout=5) as r:
                ip = r.read().decode().strip()
                print(GREEN + f"  [+] Public IP" + RESET + ": " + WHITE + ip + RESET)
                end_section()
                return
        except Exception:
            pass
    print(WHITE + "  [!] Could not determine public IP." + RESET)
    end_section()

def mac_vendor_lookup():
    section("MAC VENDOR LOOKUP")
    mac = input_prompt("  MAC Address (e.g. 00:11:22:AA:BB:CC): ")
    if not mac:
        end_section()
        return

    mac = mac.replace("-", ":").upper().strip()
    oui = mac[:8]

    try:
        url = f"https://api.macvendors.com/{mac}"
        with urllib.request.urlopen(url, timeout=10) as r:
            vendor = r.read().decode().strip()
            if vendor and "errors" not in vendor.lower():
                print(GREEN + f"  MAC   : " + RESET + WHITE + mac + RESET)
                print(GREEN + f"  Vendor: " + RESET + WHITE + vendor + RESET)
            else:
                print(WHITE + "  [!] Vendor not found." + RESET)
    except urllib.error.HTTPError:
        print(WHITE + "  [!] Vendor not found in database." + RESET)
    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)
    end_section()

def traceroute():
    section("TRACEROUTE")
    target = input_prompt("  Target IP or Domain: ")
    if not target:
        end_section()
        return

    plat = platform.system().lower()
    if plat.startswith('win'):
        cmd = f"tracert -d -h 30 {target}"
    else:
        cmd = f"traceroute -n -m 30 {target}"

    print(WHITE + "  [*] Tracing route..." + RESET)
    print(DIM + "  " + "-" * 52 + RESET)

    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        output = (r.stdout or '') + (r.stderr or '')
        for line in output.splitlines():
            cleaned = line.rstrip()
            if cleaned:
                print(WHITE + "  " + cleaned + RESET)
    except subprocess.TimeoutExpired:
        print(WHITE + "  [!] Traceroute timed out." + RESET)
    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)
    end_section()
