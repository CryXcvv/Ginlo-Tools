import re
import json
from utils import GREEN, WHITE, RESET, DIM, section, end_section, run_cmd

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
            if current:
                networks.append(current)
            current = {'ssid': line.split(":", 1)[1].strip() if ":" in line else ""}
        elif line.lower().startswith("bssid"):
            current['bssid'] = line.split(":", 1)[1].strip() if ":" in line else ""
        elif "signal" in line.lower():
            m = re.search(r'(\d+)%', line)
            if m:
                current['signal'] = m.group(1) + "%"
        elif "channel" in line.lower() and ":" in line:
            current['channel'] = line.split(":", 1)[1].strip()
        elif "authentication" in line.lower() and ":" in line:
            current['auth'] = line.split(":", 1)[1].strip()
        elif "encryption" in line.lower() and ":" in line:
            current['enc'] = line.split(":", 1)[1].strip()
    if current:
        networks.append(current)

    if not networks:
        print(WHITE + "  [!] No networks found." + RESET)
        end_section()
        return

    print(WHITE + f"  {'#':<3}{'SSID':<26}{'BSSID':<20}{'Signal':<9}{'Ch':<5}{'Auth'}" + RESET)
    print(DIM + "  " + "─" * 72 + RESET)
    for i, n in enumerate(networks, 1):
        ssid = (n.get('ssid', '?') or '?')[:25]
        bssid = n.get('bssid', '?')
        sig = n.get('signal', '?')
        ch = n.get('channel', '?')
        auth = n.get('auth', '?')
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
        if isinstance(data, dict) and "results" in data:
            data = data["results"]
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
        ssid = (n.get('ssid', '') or '<hidden>')[:23]
        bssid = n.get('bssid', '?')
        level = n.get('level', n.get('signal_strength', '?'))
        sig = f"{level} dBm" if level != '?' else '?'
        freq = n.get('frequency', 0)
        ch = (int(freq) // 5 - 2007) if freq and isinstance(freq, (int, float)) and freq >= 2412 else '?'
        cap = n.get('capabilities', '?')[:25]
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
    except Exception:
        pass
    end_section()
