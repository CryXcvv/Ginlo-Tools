import socket
import time
from utils import GREEN, WHITE, RESET, DIM, section, end_section, input_prompt

COMMON_CREDS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("admin", "12345"),
    ("admin", "root"),
    ("root", "root"),
    ("root", "admin"),
    ("root", "toor"),
    ("user", "user"),
    ("user", "password"),
    ("test", "test"),
    ("guest", "guest"),
    ("admin", "1234"),
    ("admin", "pass"),
    ("pi", "raspberry"),
    ("ubnt", "ubnt"),
    ("support", "support"),
    ("ftp", "ftp"),
    ("anonymous", ""),
    ("anonymous", "anonymous"),
    ("admin", "admin123"),
    ("admin", "letmein"),
    ("admin", "welcome"),
    ("admin", "123456"),
]

VULN_DB = {
    "OpenSSH_2": ["CVE-2000-0525", "SSH protocol integer overflow"],
    "OpenSSH_3": ["CVE-2002-0083", "SSH buffer overflow"],
    "OpenSSH_4": ["CVE-2007-2243", "SSH denial of service"],
    "OpenSSH_5": ["CVE-2014-1692", "SSH hash collision"],
    "OpenSSH_6": ["CVE-2015-6563", "SSH MaxAuthTries bypass"],
    "OpenSSH_7.0": ["CVE-2016-6210", "SSH user enumeration"],
    "OpenSSH_7.1": ["CVE-2016-6210", "SSH user enumeration"],
    "OpenSSH_7.2": ["CVE-2016-6210", "SSH user enumeration"],
    "OpenSSH_7.3": ["CVE-2016-8858", "SSH denial of service"],
    "OpenSSH_7.4": ["CVE-2017-15906", "SSH password audit bypass"],
    "OpenSSH_7.5": [],
    "OpenSSH_7.6": [],
    "OpenSSH_7.7": [],
    "OpenSSH_7.8": [],
    "OpenSSH_7.9": [],
    "OpenSSH_8.0": [],
    "OpenSSH_8.1": [],
    "OpenSSH_8.2": [],
    "OpenSSH_8.3": [],
    "OpenSSH_8.4": [],
    "OpenSSH_8.5": ["CVE-2021-41617", "SSH privilege escalation"],
    "vsftPD_2.0": ["CVE-2006-6563", "vsftpd denial of service"],
    "vsftPD_2.1": ["CVE-2011-0762", "vsftpd buffer overflow"],
    "vsftPD_2.3": ["CVE-2011-0762", "vsftpd buffer overflow"],
    "vsftPD_3.0": [],
    "ProFTPD_1.3": ["CVE-2010-4221", "ProFTPD buffer overflow"],
    "ProFTPD_1.4": [],
    "Apache_1": ["CVE-2003-0020", "Apache HTTP request smuggling"],
    "Apache_2.0": ["CVE-2004-0940", "Apache path disclosure"],
    "Apache_2.2": ["CVE-2010-1452", "Apache mod_cache DoS"],
    "Apache_2.4.0": ["CVE-2014-6271", "Shellshock (CGI)"],
    "Apache_2.4.1": ["CVE-2014-6271", "Shellshock (CGI)"],
    "Apache_2.4.10": ["CVE-2014-6271", "Shellshock (CGI)"],
    "Apache_2.4.17": [],
    "Apache_2.4.18": ["CVE-2015-3183", "Apache chunked transfer"],
    "Apache_2.4.20": [],
    "Apache_2.4.25": [],
    "Apache_2.4.29": [],
    "Apache_2.4.34": [],
    "Apache_2.4.37": [],
    "Apache_2.4.38": [],
    "Apache_2.4.39": [],
    "Apache_2.4.41": [],
    "Apache_2.4.43": [],
    "Apache_2.4.46": ["CVE-2020-11993", "Apache push diary DoS"],
    "Apache_2.4.48": [],
    "Apache_2.4.49": ["CVE-2021-41773", "Apache path traversal"],
    "Apache_2.4.50": ["CVE-2021-42013", "Apache path traversal RCE"],
    "nginx_0": ["CVE-2009-2629", "nginx integer overflow"],
    "nginx_1.0": ["CVE-2012-1180", "nginx buffer overflow"],
    "nginx_1.4": ["CVE-2014-3616", "nginx starttls DoS"],
    "nginx_1.6": ["CVE-2014-3616", "nginx starttls DoS"],
    "nginx_1.8": [],
    "nginx_1.10": ["CVE-2017-7529", "nginx integer overflow"],
    "nginx_1.12": ["CVE-2017-7529", "nginx integer overflow"],
    "nginx_1.14": [],
    "nginx_1.16": [],
    "nginx_1.18": [],
    "nginx_1.20": [],
    "nginx_1.22": [],
}

def grab_banner(target, port, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((target, port))
        banner = s.recv(256).decode(errors='ignore').strip()
        s.close()
        return banner
    except Exception:
        return ""

def try_ftp_login(target, port, user, passwd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target, port))
        s.recv(128)
        s.send(f"USER {user}\r\n".encode())
        s.recv(128)
        s.send(f"PASS {passwd}\r\n".encode())
        resp = s.recv(128).decode(errors='ignore')
        s.send(b"QUIT\r\n")
        s.close()
        if "230" in resp or "Logged" in resp or "OK" in resp:
            return True
    except Exception:
        pass
    return False

def try_ssh_login(target, port, user, passwd):
    """Check if SSH server exists - full auth is slow, note open port"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((target, port))
        banner = s.recv(256).decode(errors='ignore')
        s.close()
        return "SSH" in banner or "OpenSSH" in banner
    except Exception:
        return False

def try_telnet_login(target, port, user, passwd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((target, port))
        data = s.recv(256).decode(errors='ignore', timeout=3)
        s.send(f"{user}\n".encode())
        time.sleep(0.5)
        data += s.recv(256).decode(errors='ignore', timeout=3)
        s.send(f"{passwd}\n".encode())
        time.sleep(0.5)
        data += s.recv(256).decode(errors='ignore', timeout=3)
        s.close()

        prompts = ["#", "$", ">", "C:\\", "Welcome"]
        if any(p in data for p in prompts) and "Login incorrect" not in data and "Password:" not in data:
            return True
    except Exception:
        pass
    return False

def weak_password_check():
    section("WEAK PASSWORD CHECK")
    target = input_prompt("  Target IP: ")
    if not target:
        end_section()
        return

    print(WHITE + "  [*] Checking default credentials on common services..." + RESET)
    print()

    services_to_check = []

    for port, name, desc in [(21, "FTP", "File Transfer Protocol"),
                              (22, "SSH", "Secure Shell"),
                              (23, "Telnet", "Telnet")]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            if s.connect_ex((target, port)) == 0:
                services_to_check.append((port, name, desc))
            s.close()
        except Exception:
            pass

    if not services_to_check:
        print(WHITE + "  [!] No vulnerable services (FTP/SSH/Telnet) found open." + RESET)
        end_section()
        return

    for port, name, desc in services_to_check:
        print(GREEN + f"  [*] Testing {name} ({desc}) on {target}:{port}..." + RESET)
        found = False
        tested = 0

        for user, passwd in COMMON_CREDS:
            tested += 1
            if tested > 10:
                print(DIM + "      ... checked 10+ credentials, stopping scan" + RESET)
                break

            if port == 21 and try_ftp_login(target, port, user, passwd):
                print(WHITE + f"  [!] WEAK: {name} - {user}:{passwd}" + RESET)
                found = True
                break
            elif port == 22 and try_ssh_login(target, port, user, passwd):
                print(DIM + f"      SSH detected - test if banner suggests weak config" + RESET)
                break
            elif port == 23 and try_telnet_login(target, port, user, passwd):
                print(WHITE + f"  [!] WEAK: {name} - {user}:{passwd}" + RESET)
                found = True
                break

        if not found and port in [21, 23]:
            print(GREEN + f"      No weak credentials found for {name}" + RESET)

    end_section()

def check_vuln(service_name, version_str):
    results = []
    for key, vulns in VULN_DB.items():
        if key.lower().startswith(service_name.lower().replace(" ", "")):
            if not version_str or version_str[0].isdigit():
                if version_str:
                    ver_major = version_str.split(".")[0]
                    key_ver = key.split("_")[-1].split(".")[0]
                    if ver_major == key_ver:
                        results.extend(vulns)
            else:
                if version_str and version_str in key:
                    results.extend(vulns)
    return results

def vuln_checker():
    section("VULNERABILITY CHECKER")
    target = input_prompt("  Target IP: ")
    if not target:
        end_section()
        return

    print(WHITE + "  [*] Scanning for vulnerable services..." + RESET)
    print()

    check_ports = [21, 22, 25, 80, 110, 143, 443, 3306, 8080, 8443]
    port_names = {
        21: "FTP", 22: "SSH", 25: "SMTP", 80: "HTTP",
        110: "POP3", 143: "IMAP", 443: "HTTPS",
        3306: "MySQL", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
    }

    found_any = False
    for port in check_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            if s.connect_ex((target, port)) == 0:
                name = port_names.get(port, f"Port {port}")
                banner = grab_banner(target, port, timeout=2)
                svc_name = name
                ver = ""

                if banner:
                    for svc in ["OpenSSH", "Apache", "nginx", "vsftpd", "ProFTPD"]:
                        if svc.lower() in banner.lower():
                            idx = banner.lower().index(svc.lower())
                            ver_part = banner[idx:].split()[0] if banner[idx:] else ""
                            for token in banner[idx:].split():
                                if token[0].isdigit() or token[0] in "(":
                                    ver = token.strip("(),")
                                    break
                            svc_name = svc
                            break

                vulns = check_vuln(svc_name, ver)
                if vulns:
                    found_any = True
                    print(GREEN + f"  [+] {target}:{port} ({name})" + RESET)
                    print(WHITE + f"      Banner: {banner[:80]}" + RESET)
                    print(WHITE + f"      Version: {ver or 'unknown'}" + RESET)
                    for cve, desc in vulns:
                        print(WHITE + f"      - {cve}: {desc}" + RESET)
                    print()
            s.close()
        except Exception:
            pass

    if not found_any:
        print(WHITE + "  [+] No known vulnerabilities detected." + RESET)

    end_section()
