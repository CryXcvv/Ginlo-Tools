import os
import sys
import platform
import subprocess
import socket

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    GREEN  = Fore.GREEN + Style.BRIGHT
    WHITE  = Style.BRIGHT
    RESET  = Style.RESET_ALL
    DIM    = Fore.WHITE
except ImportError:
    GREEN = WHITE = RESET = DIM = ""

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "downloads")
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

U = chr(0x250C) if platform.system().lower().startswith('win') and sys.stdout.encoding.lower() in ('utf-8', 'utf-16') else '+'
R = chr(0x2510) if platform.system().lower().startswith('win') and sys.stdout.encoding.lower() in ('utf-8', 'utf-16') else '+'
B = chr(0x2514) if platform.system().lower().startswith('win') and sys.stdout.encoding.lower() in ('utf-8', 'utf-16') else '+'
V = chr(0x2502) if platform.system().lower().startswith('win') and sys.stdout.encoding.lower() in ('utf-8', 'utf-16') else '|'
H = chr(0x2500) if platform.system().lower().startswith('win') and sys.stdout.encoding.lower() in ('utf-8', 'utf-16') else '-'

def section(title):
    pad = max(0, 48 - len(title))
    print(f"\n{GREEN}{U}{H}[ {title} ]{H * pad}{R}{RESET}")

def end_section():
    print(GREEN + B + H * 52 + R + RESET)

def _gradient_logo():
    logo_lines = LOGO.strip('\n').split('\n')
    gradient = [
        "\033[38;2;0;120;0m",
        "\033[38;2;0;120;0m",
        "\033[38;2;0;120;0m",
        "\033[38;2;0;120;0m",
        "\033[38;2;0;160;0m",
        "\033[38;2;0;160;0m",
        "\033[38;2;0;160;0m",
        "\033[38;2;0;160;0m",
        "\033[38;2;0;195;10m",
        "\033[38;2;0;195;10m",
        "\033[38;2;0;195;10m",
        "\033[38;2;0;195;10m",
        "\033[38;2;30;215;0m",
        "\033[38;2;30;215;0m",
        "\033[38;2;30;215;0m",
        "\033[38;2;30;215;0m",
        "\033[38;2;70;230;0m",
        "\033[38;2;70;230;0m",
        "\033[38;2;70;230;0m",
        "\033[38;2;70;230;0m",
        "\033[38;2;120;240;0m",
        "\033[38;2;120;240;0m",
        "\033[38;2;120;240;0m",
        "\033[38;2;120;240;0m",
        "\033[38;2;180;255;0m",
        "\033[38;2;180;255;0m",
        "\033[38;2;180;255;0m",
        "\033[38;2;180;255;0m",
    ]
    for i, line in enumerate(logo_lines):
        c = gradient[i] if i < len(gradient) else gradient[-1]
        print(c + line + RESET)

def show_banner():
    try:
        _gradient_logo()
    except Exception:
        print(GREEN + LOGO + RESET)
    print(GREEN + "  Author : AvreyDev" + RESET)
    print(GREEN + "  GitHub : https://github.com/CryXcvv" + RESET)
    print(WHITE + "  " + H * 50 + RESET)
    print()

def menu_header(text):
    print(GREEN + f"\n  {U}{H}[ {text} ]" + H * 39 + R + RESET)

def menu_item(num, text):
    print(WHITE + f"  {V}  {num}. {text:<48}{V}" + RESET)

def menu_separator():
    print(DIM + f"  {V}{' ' * 52}{V}" + RESET)

def menu_footer():
    print(GREEN + "  " + B + H * 52 + R + RESET)

def show_menu():
    menu_header("MENU")
    menu_item("1", "WiFi & Network")
    menu_item("2", "Port & Service")
    menu_item("3", "Recon & Discovery")
    menu_item("4", "Security Audit")
    menu_item("5", "Tools")
    menu_separator()
    menu_item("0", "Exit")
    menu_footer()
    print(DIM + "  Select a category to view its tools" + RESET)

def show_wifi_menu():
    menu_header("WIFI & NETWORK")
    menu_item("1", "Scan WiFi Networks")
    menu_item("2", "Current WiFi Connection Info")
    menu_item("3", "Scan Local Network Devices")
    menu_item("4", "Custom Subnet Scan")
    menu_item("5", "Traceroute")
    menu_separator()
    menu_item("0", "Back to Main Menu")
    menu_footer()

def show_port_menu():
    menu_header("PORT & SERVICE")
    menu_item("1", "Port Scan (Common Ports)")
    menu_item("2", "Port Scan (Custom Range)")
    menu_item("3", "Service Version Detection")
    menu_separator()
    menu_item("0", "Back to Main Menu")
    menu_footer()

def show_recon_menu():
    menu_header("RECON & DISCOVERY")
    menu_item("1", "DNS Lookup")
    menu_item("2", "Reverse DNS Lookup")
    menu_item("3", "HTTP Header Sniffer")
    menu_item("4", "GeoIP Lookup")
    menu_item("5", "Public IP Check")
    menu_item("6", "MAC Vendor Lookup")
    menu_separator()
    menu_item("0", "Back to Main Menu")
    menu_footer()

def show_audit_menu():
    menu_header("SECURITY AUDIT")
    menu_item("1", "Weak Password Check")
    menu_item("2", "Vulnerability Checker")
    menu_separator()
    menu_item("0", "Back to Main Menu")
    menu_footer()

def show_tools_menu():
    menu_header("TOOLS")
    menu_item("1", "Full Scan")
    menu_item("2", "Export Report")
    menu_item("3", "Save Session")
    menu_item("4", "Schedule Scan")
    menu_separator()
    menu_item("0", "Back to Main Menu")
    menu_footer()

def input_prompt(msg="  > "):
    return input(WHITE + msg + RESET).strip()

def press_enter():
    input(WHITE + "\n  Press Enter..." + RESET)
