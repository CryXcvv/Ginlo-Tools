import socket
import time
from utils import GREEN, WHITE, RESET, DIM, section, end_section, input_prompt

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt"
}

SERVICE_BANNER_PORTS = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
}

def grab_banner(target, port, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((target, port))
        banner = ""
        if port in [21, 25, 110, 143]:
            banner = s.recv(256).decode(errors='ignore').strip()
        elif port in [80, 443]:
            s.send(f"HEAD / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n".encode())
            resp = s.recv(1024).decode(errors='ignore')
            for line in resp.splitlines():
                if line.startswith("Server:"):
                    banner = line.strip()
                    break
        elif port == 22:
            banner = s.recv(256).decode(errors='ignore').strip()
        s.close()
        return banner
    except Exception:
        return ""

def port_scan(target=None, ports=None):
    if not target:
        section("PORT SCAN")
        target = input_prompt("  Target IP: ")
        if not target:
            end_section()
            return

    if not ports:
        ports = COMMON_PORTS

    section(f"PORT SCAN {target}")
    open_ports = []

    for p in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((target, p)) == 0:
                banner = ""
                try:
                    banner = s.recv(100).decode(errors='ignore').strip()
                except Exception:
                    pass
                svc = COMMON_PORTS.get(p, "Unknown")
                open_ports.append((p, svc, banner))
                line = f"  [OPEN] {target}:{p} ({svc})"
                if banner:
                    line += f" [{banner[:60]}]"
                print(GREEN + line + RESET)
            s.close()
        except Exception:
            pass

    if not open_ports:
        print(WHITE + "  [!] No open ports found." + RESET)
    else:
        print()
        print(WHITE + f"  {'Port':<8}{'Service':<15}{'Banner'}" + RESET)
        print(DIM + "  " + "─" * 60 + RESET)
        for p, svc, banner in open_ports:
            b = banner[:50] if banner else "-"
            print(WHITE + f"  {p:<8}{svc:<15}{b}" + RESET)
        print()
        print(GREEN + f"  [+] {len(open_ports)} open ports" + RESET)

    end_section()

def port_scan_custom():
    section("PORT SCAN (CUSTOM)")
    target = input_prompt("  Target IP: ")
    if not target:
        end_section()
        return

    range_input = input_prompt("  Port range (e.g. 1-1000): ")
    if not range_input or '-' not in range_input:
        print(WHITE + "  [!] Invalid range. Use format: start-end" + RESET)
        end_section()
        return

    try:
        start_p, end_p = map(int, range_input.split('-'))
        if start_p < 1 or end_p > 65535 or start_p > end_p:
            raise ValueError
    except ValueError:
        print(WHITE + "  [!] Invalid range. Use numbers 1-65535." + RESET)
        end_section()
        return

    port_count = end_p - start_p + 1
    print(WHITE + f"  [*] Scanning {target} ports {start_p}-{end_p} ({port_count} ports)..." + RESET)

    open_ports = []
    start_time = time.time()

    for p in range(start_p, end_p + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((target, p)) == 0:
                open_ports.append(p)
                print(GREEN + f"  [OPEN] {target}:{p}" + RESET)
            s.close()
        except Exception:
            pass

    elapsed = time.time() - start_time
    print()
    if not open_ports:
        print(WHITE + "  [!] No open ports found." + RESET)
    else:
        print(GREEN + f"  [+] {len(open_ports)} open ports" + RESET)
        print(WHITE + "  " + ", ".join(str(p) for p in open_ports) + RESET)

    print(DIM + f"  [*] Scan completed in {elapsed:.1f}s" + RESET)
    end_section()

def service_version_detection():
    section("SERVICE VERSION DETECTION")
    target = input_prompt("  Target IP: ")
    if not target:
        end_section()
        return

    print(WHITE + "  [*] Probing services on common ports..." + RESET)
    print()

    found = []
    for port, svc in SERVICE_BANNER_PORTS.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            if s.connect_ex((target, port)) == 0:
                banner = grab_banner(target, port, timeout=3)
                found.append((port, svc, banner))
                line = f"  [OPEN] {target}:{port} ({svc})"
                if banner:
                    line += f" -> {banner[:80]}"
                print(GREEN + line + RESET)
            s.close()
        except Exception:
            pass

    if not found:
        print(WHITE + "  [!] No services detected." + RESET)
    else:
        print()
        print(WHITE + f"  {'Port':<8}{'Service':<12}{'Version/Banner'}" + RESET)
        print(DIM + "  " + "─" * 60 + RESET)
        for p, svc, banner in found:
            b = banner[:50] if banner else "no banner"
            print(WHITE + f"  {p:<8}{svc:<12}{b}" + RESET)

    end_section()
