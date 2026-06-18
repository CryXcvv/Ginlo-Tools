import sys
from utils import clear_screen, detect_os, show_banner, show_menu, GREEN, WHITE, RESET, input_prompt, press_enter
from utils import show_wifi_menu, show_port_menu, show_recon_menu, show_audit_menu, show_tools_menu

def wifi_network_menu(os_name):
    while True:
        clear_screen()
        show_banner()
        print(GREEN + f"  [*] Platform : " + RESET + WHITE + os_name.upper() + RESET)
        show_wifi_menu()
        choice = input_prompt()

        if choice == "1":
            from wifi import windows_scan_wifi, termux_scan_wifi
            if os_name == "windows":
                windows_scan_wifi()
            elif os_name == "termux":
                termux_scan_wifi()
            else:
                print(GREEN + "  [!] Not supported." + RESET)
        elif choice == "2":
            from wifi import windows_current_connection, termux_current_connection
            if os_name == "windows":
                windows_current_connection()
            elif os_name == "termux":
                termux_current_connection()
            else:
                print(GREEN + "  [!] Not supported." + RESET)
        elif choice == "3":
            from network import scan_local_network
            data = scan_local_network()
            if data:
                from report import add_scan_data
                add_scan_data("Local Network Scan", data)
        elif choice == "4":
            from network import scan_custom_subnet
            scan_custom_subnet()
        elif choice == "5":
            from recon import traceroute
            traceroute()
        elif choice == "0":
            break
        else:
            print(WHITE + "  [!] Invalid option." + RESET)
        press_enter()

def port_service_menu(os_name):
    while True:
        clear_screen()
        show_banner()
        print(GREEN + f"  [*] Platform : " + RESET + WHITE + os_name.upper() + RESET)
        show_port_menu()
        choice = input_prompt()

        if choice == "1":
            from portscan import port_scan
            port_scan()
        elif choice == "2":
            from portscan import port_scan_custom
            port_scan_custom()
        elif choice == "3":
            from portscan import service_version_detection
            service_version_detection()
        elif choice == "0":
            break
        else:
            print(WHITE + "  [!] Invalid option." + RESET)
        press_enter()

def recon_discovery_menu(os_name):
    while True:
        clear_screen()
        show_banner()
        print(GREEN + f"  [*] Platform : " + RESET + WHITE + os_name.upper() + RESET)
        show_recon_menu()
        choice = input_prompt()

        if choice == "1":
            from recon import dns_lookup
            dns_lookup()
        elif choice == "2":
            from recon import reverse_dns_lookup
            reverse_dns_lookup()
        elif choice == "3":
            from recon import http_headers
            http_headers()
        elif choice == "4":
            from recon import geoip_lookup
            geoip_lookup()
        elif choice == "5":
            from recon import public_ip_check
            public_ip_check()
        elif choice == "6":
            from recon import mac_vendor_lookup
            mac_vendor_lookup()
        elif choice == "0":
            break
        else:
            print(WHITE + "  [!] Invalid option." + RESET)
        press_enter()

def audit_menu(os_name):
    while True:
        clear_screen()
        show_banner()
        print(GREEN + f"  [*] Platform : " + RESET + WHITE + os_name.upper() + RESET)
        show_audit_menu()
        choice = input_prompt()

        if choice == "1":
            from audit import weak_password_check
            weak_password_check()
        elif choice == "2":
            from audit import vuln_checker
            vuln_checker()
        elif choice == "0":
            break
        else:
            print(WHITE + "  [!] Invalid option." + RESET)
        press_enter()

def tools_menu(os_name):
    while True:
        clear_screen()
        show_banner()
        print(GREEN + f"  [*] Platform : " + RESET + WHITE + os_name.upper() + RESET)
        show_tools_menu()
        choice = input_prompt()

        if choice == "1":
            print(WHITE + "  [*] Running Full Scan..." + RESET)
            if os_name == "windows":
                from wifi import windows_current_connection, windows_scan_wifi
                windows_current_connection()
                windows_scan_wifi()
            elif os_name == "termux":
                from wifi import termux_current_connection, termux_scan_wifi
                termux_current_connection()
                termux_scan_wifi()
            from network import scan_local_network
            data = scan_local_network()
            if data:
                from report import add_scan_data
                add_scan_data("Full Scan", data)
        elif choice == "2":
            from report import export_report
            export_report()
        elif choice == "3":
            from report import save_session
            save_session()
        elif choice == "4":
            from report import schedule_scan
            schedule_scan()
        elif choice == "0":
            break
        else:
            print(WHITE + "  [!] Invalid option." + RESET)
        press_enter()

def main():
    os_name = detect_os()

    while True:
        clear_screen()
        show_banner()
        print(GREEN + f"  [*] Platform : " + RESET + WHITE + os_name.upper() + RESET)
        show_menu()
        choice = input_prompt()

        if choice == "1":
            wifi_network_menu(os_name)
        elif choice == "2":
            port_service_menu(os_name)
        elif choice == "3":
            recon_discovery_menu(os_name)
        elif choice == "4":
            audit_menu(os_name)
        elif choice == "5":
            tools_menu(os_name)
        elif choice == "0":
            print(GREEN + "\n  [*] Exit.\n" + RESET)
            sys.exit(0)
        else:
            print(WHITE + "  [!] Invalid option." + RESET)
        press_enter()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(GREEN + "\n\n  [!] Interrupted.\n" + RESET)
        sys.exit(0)
