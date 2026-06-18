import os
import socket
import time
import json
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor
from utils import GREEN, WHITE, RESET, DIM, section, end_section, get_local_ip, get_subnet, run_cmd, OUTPUT_DIR

def ping_host(ip):
    plat = platform.system().lower()
    param = '-n 1 -w 500' if plat.startswith('win') else '-c 1 -W 1'
    null = 'NUL' if plat.startswith('win') else '/dev/null'
    cmd = f"ping {param} {ip} > {null} 2>&1"
    return ip if subprocess.call(cmd, shell=True) == 0 else None

def flush_arp_cache():
    plat = platform.system().lower()
    if plat.startswith('win'):
        run_cmd("arp -d *", timeout=10)
    elif plat == 'linux':
        run_cmd("ip neigh flush all 2>/dev/null", timeout=10)

def get_arp_snapshot():
    arp = {}
    plat = platform.system().lower()
    if plat.startswith('win'):
        out = run_cmd("arp -a", timeout=10)
        for line in out.splitlines():
            m = re.match(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-:]{11,17})\s+(\w+)', line.strip())
            if m:
                arp[m.group(1)] = (m.group(2), m.group(3))
    else:
        out = run_cmd("ip neigh", timeout=10)
        for line in out.splitlines():
            m = re.search(r'(\d+\.\d+\.\d+\.\d+).*?((?:[0-9a-fA-F]{2}[:\-]){5}[0-9a-fA-F]{2})', line)
            if m:
                arp[m.group(1)] = (m.group(2), '')
    return arp

def resolve_arp_for_hosts(hosts, retries=4, delay=0.5):
    found = {}
    pending = set(hosts)
    for _ in range(retries):
        if not pending:
            break
        with ThreadPoolExecutor(max_workers=50) as ex:
            list(ex.map(ping_host, pending))
        time.sleep(delay)
        snap = get_arp_snapshot()
        for ip in list(pending):
            if ip in snap:
                found[ip] = snap[ip]
                pending.discard(ip)
    for ip in pending:
        found[ip] = ("?", "?")
    return found

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "?"

def scan_local_network():
    section("LOCAL NETWORK SCAN")
    local_ip = get_local_ip()
    subnet = get_subnet(local_ip)
    print(GREEN + f"  [*] IP  : " + RESET + WHITE + local_ip + RESET)
    print(GREEN + f"  [*] Subnet: " + RESET + WHITE + subnet + "0/24" + RESET)

    flush_arp_cache()
    print(WHITE + "  [*] Scanning hosts..." + RESET)
    targets = [f"{subnet}{i}" for i in range(1, 255)]
    with ThreadPoolExecutor(max_workers=50) as ex:
        results = list(ex.map(ping_host, targets))
    alive = [r for r in results if r]

    print(WHITE + "  [*] Resolving MACs..." + RESET)
    arp = resolve_arp_for_hosts(alive)

    print()
    print(WHITE + f"  {'#':<3}{'IP':<17}{'MAC':<21}{'Type':<12}{'Hostname'}" + RESET)
    print(DIM + "  " + "─" * 68 + RESET)

    scan_results = []
    for i, ip in enumerate(alive, 1):
        mac_info = arp.get(ip, ("?", "?"))
        mac, typ = mac_info if isinstance(mac_info, tuple) else (mac_info, "")
        host = get_hostname(ip)
        scan_results.append({"ip": ip, "mac": mac, "type": typ, "hostname": host})
        color = GREEN if ip == local_ip else WHITE
        print(color + f"  {i:<3}{ip:<17}{mac:<21}{typ:<12}{host}" + RESET)

    print()
    print(GREEN + f"  [+] {len(alive)} active devices" + RESET)
    end_section()

    if input(WHITE + "  Save to JSON? (y/n): " + RESET).strip().lower() == 'y':
        fname = input(WHITE + "  Filename: " + RESET).strip() or "scan"
        fpath = os.path.join(OUTPUT_DIR, f"{fname}.json")
        try:
            with open(fpath, 'w') as f:
                json.dump(scan_results, f, indent=4)
            print(GREEN + f"  [+] Saved to {fpath}" + RESET)
        except Exception as e:
            print(WHITE + f"  [!] Error: {e}" + RESET)

    return scan_results

def scan_custom_subnet():
    section("CUSTOM SUBNET SCAN")
    subnet_input = input(WHITE + "  Subnet (e.g. 192.168.1 or 10.0.0): " + RESET).strip()
    if not subnet_input:
        print(WHITE + "  [!] No subnet provided." + RESET)
        end_section()
        return

    parts = subnet_input.split('.')
    if len(parts) != 3:
        print(WHITE + "  [!] Invalid subnet format. Use: x.x.x" + RESET)
        end_section()
        return

    print(WHITE + "  [*] Scanning subnet " + subnet_input + ".0/24..." + RESET)
    flush_arp_cache()
    targets = [f"{subnet_input}.{i}" for i in range(1, 255)]

    with ThreadPoolExecutor(max_workers=50) as ex:
        results = list(ex.map(ping_host, targets))
    alive = [r for r in results if r]

    print(WHITE + "  [*] Resolving MACs..." + RESET)
    arp = resolve_arp_for_hosts(alive)

    print()
    print(WHITE + f"  {'#':<3}{'IP':<17}{'MAC':<21}{'Hostname'}" + RESET)
    print(DIM + "  " + "─" * 62 + RESET)

    for i, ip in enumerate(alive, 1):
        mac_info = arp.get(ip, ("?", "?"))
        mac, _ = mac_info if isinstance(mac_info, tuple) else (mac_info, "")
        host = get_hostname(ip)
        print(WHITE + f"  {i:<3}{ip:<17}{mac:<21}{host}" + RESET)

    print()
    print(GREEN + f"  [+] {len(alive)} active devices" + RESET)
    end_section()

import re
