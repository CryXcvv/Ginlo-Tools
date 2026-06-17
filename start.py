#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =========================================================================
# 1. IMPORT & CONFIGURATION
# =========================================================================
import os
import sys
import re
import socket
import platform
import subprocess
import time
import json
from concurrent.futures import ThreadPoolExecutor

# Color Configuration
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN  = Fore.GREEN + Style.BRIGHT
    WHITE  = Style.BRIGHT
    RESET  = Style.RESET_ALL
    DIM    = Fore.WHITE
except ImportError:
    GREEN = WHITE = RESET = DIM = ""

# Logo ASCII Art
LOGO = r"""
                                         %@@@@*                           
                          =.            *@@@@@@:                          
                       .@@@@@+           @@@@@@                           
                       :@@@@@#              .           .                 
                         +%#              @@@@@=    .@@@@@@=              
                         =@@@@          .@@@@@@@@   @@@@@@@@              
                        #@@@@@@@@@@@@@@@@@@@@@@@@%  %@@@@@@@              
              .@@@@*    %@@@@@@@@+      .@@@@@@@@@@.  %@@@.               
             @@@@@@@@=   @@@@@@-          -@@@@@@*@@@@=                   
            :@@@@@@@@@   .@@@@     %@@#            :@@@@@@@@-             
             @@@@@@@@*     ##   +@@@@@@@@=         +@@@@@@@@@.            
              :@@@@%           =@@@@@@@@@@:        @@@@@@@@@@.            
                               #@@@@@@@@@@+       #@@@@@@@@@=             
                 ...            @@@@@@@@@@       :@@@@@@@@@               
             @@@@@@@@@%           @@@@@%        @@@@@@@@@@+               
             @@@@@@@@@@@@              .    .%@@@@@@@@@@@@%               
              @@@@@@@@@@@@@%    #@@@@@@@@@@@@@@@@@@@@@@@@@@               
               -@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+              
                .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.  :@@@@@@+              
                 %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.      -=                 
                 -@@@@@@@:  #@@@@@@@@@@@@@@@@@@@                          
                 :@@@@@@+    .@@@@@@@@@@@@@@@@@                           
                 -@@@@@@      :@@@@@@@@@@@@@@@                            
                  @@@@@@        @@@@@@@@@@@@#                             
                  *@@@@*        =@@@@@@@@@@@                              
                                 @@@@@@@@@@@                              
                                  @@@@@@@@@@                              
                                   %@@@@@@@#                              
"""

# =========================================================================
# 2. SYSTEM UTILITIES
# =========================================================================
def clear_screen():
    os.system('cls' if platform.system().lower().startswith('win') else 'clear')

def detect_os():
    if os.path.exists('/data/data/com.termux/files/usr'):
        return 'termux'
    if platform.system().lower().startswith('win'):
        return 'windows'
    if platform.system().lower() == 'linux':
        return 'linux'
    return 'unknown'

def run_cmd(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return (r.stdout or '') + (r.stderr or '')
    except subprocess.TimeoutExpired:
        return "[!] Command timed out"
    except Exception as e:
        return f"[!] Error: {e}"

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_subnet(ip):
    return '.'.join(ip.split('.')[:3]) + '.'

# =========================================================================
# 3. UI & DISPLAY HELPERS
# =========================================================================
def section(title):
    print(f"\n{GREEN}┌─[ {title} ]{'─' * max(0, 48 - len(title))}┐{RESET}")

def end_section():
    print(GREEN + "└" + "─" * 52 + "┘" + RESET)

def show_banner():
    print(GREEN + LOGO + RESET)
    print(GREEN + "  Author : AvreyDev" + RESET)
    print(GREEN + "  GitHub : https://github.com/CryXcvv" + RESET)
    print(WHITE + "  " + "─" * 50 + RESET)
    print()

def show_menu():
    print(GREEN + "\n  ┌─[ MENU ]" + "─" * 43 + "┐" + RESET)
    print(WHITE + "  │  1. Scan WiFi Networks                               │" + RESET)
    print(WHITE + "  │  2. Current WiFi Connection Info                     │" + RESET)
    print(WHITE + "  │  3. Scan Local Network Devices (Export Enabled)      │" + RESET)
    print(WHITE + "  │  4. Port Scan                                        │" + RESET)
    print(WHITE + "  │  5. Full Scan                                        │" + RESET)
    print(WHITE + "  │  6. DNS Lookup (New)                                 │" + RESET)
    print(WHITE + "  │  7. HTTP Header Sniffer (New)                        │" + RESET)
    print(WHITE + "  │  0. Exit                                             │" + RESET)
    print(GREEN + "  └" + "─" * 52 + "┘" + RESET)

# =========================================================================
# 4. WIFI OPERATIONS
# =========================================================================
def windows_scan_wifi():
    section("WIFI NETWORKS")
    out = run_cmd("netsh wlan show networks mode=bssid")
    if not out.strip():
        print(GREEN + "  [!] Unable to access netsh." + RESET)
        return

    networks = []
    current = {}
    for line in out.splitlines():
        line = line.strip()
        if line.lower().startswith("ssid"):
            if current: networks.append(current)
            current = {'ssid': line.split(":", 1)[1].strip() if ":" in line else ""}
        elif line.lower().startswith("bssid"):
            current['bssid'] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif "signal" in line.lower():
            m = re.search(r'(\d+)%', line)
            if m: current['signal'] = m.group(1) + "%"
        elif "channel" in line.lower() and ":" in line:
            current['channel'] = line.split(":", 1)[1].strip()
        elif "authentication" in line.lower() and ":" in line:
            current['auth'] = line.split(":", 1)[1].strip()
        elif "encryption" in line.lower() and ":" in line:
            current['enc'] = line.split(":", 1)[1].strip()
    if current: networks.append(current)

    if not networks:
        print(WHITE + "  [!] No networks found." + RESET)
        end_section()
        return

    print(WHITE + f"  {'#':<3}{'SSID':<26}{'BSSID':<20}{'Signal':<9}{'Ch':<5}{'Auth'}" + RESET)
    print(DIM + "  " + "─" * 72 + RESET)
    for i, n in enumerate(networks, 1):
        ssid   = (n.get('ssid', '?') or '?')[:25]
        bssid  = n.get('bssid', '?')
        sig    = n.get('signal', '?')
        ch     = n.get('channel', '?')
        auth   = n.get('auth', '?')
        print(WHITE + f"  {i:<3}{ssid:<26}{bssid:<20}{sig:<9}{ch:<5}{auth}" + RESET)
    print()
    print(GREEN + f"  [+] Total: {len(networks)} networks found" + RESET)
    end_section()

def termux_scan_wifi():
    section("WIFI NETWORKS")
    chk = run_cmd("command -v termux-wifi-scaninfo")
    if "not found" in chk.lower() or not chk.strip():
        print(GREEN + "  [!] termux-api not installed." + RESET)
        print(WHITE + "      pkg install termux-api" + RESET)
        end_section()
        return

    print(WHITE + "  [*] Scanning..." + RESET)
    out = run_cmd("termux-wifi-scaninfo", timeout=40)
    try:
        data = json.loads(out)
        if isinstance(data, dict) and "results" in data: data = data["results"]
    except Exception:
        print(GREEN + "  [!] Failed to parse results." + RESET)
        end_section()
        return

    if not data:
        print(WHITE + "  [!] No networks found." + RESET)
        end_section()
        return

    print(WHITE + f"  {'#':<3}{'SSID':<24}{'BSSID':<20}{'Signal':<13}{'Ch':<5}{'Cap'}" + RESET)
    print(DIM + "  " + "─" * 76 + RESET)
    for i, n in enumerate(data, 1):
        ssid  = (n.get('ssid', '') or '<hidden>')[:23]
        bssid = n.get('bssid', '?')
        level = n.get('level', n.get('signal_strength', '?'))
        sig   = f"{level} dBm" if level != '?' else '?'
        freq  = n.get('frequency', 0)
        ch    = (int(freq) // 5 - 2007) if freq and isinstance(freq, (int, float)) and freq >= 2412 else '?'
        cap   = n.get('capabilities', '?')[:25]
        print(WHITE + f"  {i:<3}{ssid:<24}{bssid:<20}{sig:<13}{str(ch):<5}{cap}" + RESET)
    print()
    print(GREEN + f"  [+] Total: {len(data)} networks found" + RESET)
    end_section()

def windows_current_connection():
    section("CURRENT CONNECTION")
    out = run_cmd("netsh wlan show interfaces")
    for line in out.splitlines():
        line = line.strip()
        if any(k in line.lower() for k in ["ssid", "state", "signal", "bssid", "auth"]):
            if ":" in line:
                k, v = line.split(":", 1)
                print(GREEN + f"  {k.strip():<22}" + RESET + ": " + WHITE + v.strip() + RESET)
    end_section()

def termux_current_connection():
    section("CURRENT CONNECTION")
    out = run_cmd("termux-wifi-connectioninfo")
    try:
        data = json.loads(out)
        for k, v in data.items():
            print(GREEN + f"  {k:<22}" + RESET + ": " + WHITE + str(v) + RESET)
    except Exception: pass
    end_section()

# =========================================================================
# 5. NETWORK & ARP LOGIC
# =========================================================================
def ping_host(ip):
    plat = platform.system().lower()
    param = '-n 1 -w 500' if plat.startswith('win') else '-c 1 -W 1'
    null = 'NUL' if plat.startswith('win') else '/dev/null'
    cmd = f"ping {param} {ip} > {null} 2>&1"
    return ip if subprocess.call(cmd, shell=True) == 0 else None

def flush_arp_cache():
    plat = platform.system().lower()
    if plat.startswith('win'): run_cmd("arp -d *", timeout=10)
    elif plat == 'linux': run_cmd("ip neigh flush all 2>/dev/null", timeout=10)

def get_arp_snapshot():
    arp = {}
    plat = platform.system().lower()
    if plat.startswith('win'):
        out = run_cmd("arp -a", timeout=10)
        for line in out.splitlines():
            m = re.match(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-:]{11,17})\s+(\w+)', line.strip())
            if m: arp[m.group(1)] = (m.group(2), m.group(3))
    else:
        out = run_cmd("ip neigh", timeout=10)
        for line in out.splitlines():
            m = re.search(r'(\d+\.\d+\.\d+\.\d+).*?((?:[0-9a-fA-F]{2}[:\-]){5}[0-9a-fA-F]{2})', line)
            if m: arp[m.group(1)] = (m.group(2), '')
    return arp

def resolve_arp_for_hosts(hosts, retries=4, delay=0.5):
    found = {}
    pending = set(hosts)
    for _ in range(retries):
        if not pending: break
        with ThreadPoolExecutor(max_workers=50) as ex: list(ex.map(ping_host, pending))
        time.sleep(delay)
        snap = get_arp_snapshot()
        for ip in list(pending):
            if ip in snap:
                found[ip] = snap[ip]
                pending.discard(ip)
    for ip in pending: found[ip] = ("?", "?")
    return found

def get_hostname(ip):
    try: return socket.gethostbyaddr(ip)[0]
    except Exception: return "?"

def scan_local_network():
    section("LOCAL NETWORK SCAN")
    local_ip = get_local_ip()
    subnet   = get_subnet(local_ip)
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
        host     = get_hostname(ip)
        
        scan_results.append({"ip": ip, "mac": mac, "type": typ, "hostname": host})
        
        color    = GREEN if ip == local_ip else WHITE
        print(color + f"  {i:<3}{ip:<17}{mac:<21}{typ:<12}{host}" + RESET)

    print()
    print(GREEN + f"  [+] {len(alive)} active devices" + RESET)
    end_section()
    
    # Save to JSON
    if input(WHITE + "  Save to JSON? (y/n): " + RESET).strip().lower() == 'y':
        fname = input(WHITE + "  Filename: " + RESET).strip() or "scan.json"
        try:
            with open(fname, 'w') as f: json.dump(scan_results, f, indent=4)
            print(GREEN + f"  [+] Saved to {fname}" + RESET)
        except Exception as e: print(WHITE + f"  [!] Error: {e}" + RESET)

# =========================================================================
# 6. TOOLS (PORT SCAN, DNS, HTTP HEADERS)
# =========================================================================
def port_scan(target):
    section(f"PORT SCAN {target}")
    ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 8080, 8443]
    open_ports = []
    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((target, p)) == 0:
                try: banner = s.recv(100).decode(errors='ignore').strip()
                except: banner = ""
                open_ports.append((p, banner))
                print(GREEN + f"  [OPEN] {target}:{p}" + RESET + (f" {banner}" if banner else ""))
            s.close()
        except: pass
    if not open_ports: print(WHITE + "  [!] No open ports." + RESET)
    else: print(GREEN + f"  [+] {len(open_ports)} open ports" + RESET)
    end_section()

def dns_lookup():
    section("DNS LOOKUP")
    target = input(WHITE + "  Domain: " + RESET).strip()
    if not target: return
    try:
        ip = socket.gethostbyname(target)
        print(GREEN + f"  [+] {target} -> {ip}" + RESET)
    except: print(WHITE + "  [!] Not found." + RESET)
    end_section()

def http_headers():
    section("HTTP HEADER SNIFFER")
    target = input(WHITE + "  Target: " + RESET).strip()
    if not target: return
    
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
            if line.strip(): print(WHITE + "  " + line + RESET)
    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)
    end_section()

# =========================================================================
# 7. MAIN EXECUTION
# =========================================================================
def main():
    os_name = detect_os()

    while True:
        clear_screen()
        show_banner()
        print(GREEN + f"  [*] Platform : " + RESET + WHITE + os_name.upper() + RESET)
        show_menu()
        choice = input(GREEN + "\n  > " + RESET).strip()

        if choice == "1":
            if os_name == "windows": windows_scan_wifi()
            elif os_name == "termux": termux_scan_wifi()
            else: print(GREEN + "  [!] Not supported." + RESET)

        elif choice == "2":
            if os_name == "windows": windows_current_connection()
            elif os_name == "termux": termux_current_connection()
            else: print(GREEN + "  [!] Not supported." + RESET)

        elif choice == "3": scan_local_network()
        elif choice == "4":
            t = input(WHITE + "  Target IP: " + RESET).strip()
            if t: port_scan(t)
        elif choice == "5":
            if os_name == "windows": windows_current_connection(); windows_scan_wifi()
            elif os_name == "termux": termux_current_connection(); termux_scan_wifi()
            scan_local_network()
        elif choice == "6": dns_lookup()
        elif choice == "7": http_headers()
        elif choice == "0":
            print(GREEN + "\n  [*] Exit.\n" + RESET)
            sys.exit(0)
        else: print(WHITE + "  [!] Invalid option." + RESET)

        input(WHITE + "\n  Press Enter..." + RESET)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print(GREEN + "\n\n  [!] Interrupted.\n" + RESET)
        sys.exit(0)