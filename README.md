```markdown
<p align="center">
  <img src="logo.png" alt="Logo" width="150">
</p>

<h1 align="center">Network Recon Toolkit</h1>

<p align="center">
  <img src="banner.png" alt="Ginlo Flow Banner" width="100%">
</p>

A simple, menu-driven network reconnaissance CLI tool written in Python. It works across Windows, Linux, and Termux (Android), with colored terminal output for readability.

## Features

- **Scan WiFi Networks** - Lists nearby WiFi networks with SSID, BSSID, signal strength, channel, and authentication type.
- **Current WiFi Connection Info** - Displays details about the currently active WiFi connection.
- **Scan Local Network Devices** - Discovers your local IP and subnet, then pings all hosts on the `/24` range in parallel to find active devices, resolving their MAC addresses and hostnames.
  - **Export to JSON** - Save scan results to a `.json` file for documentation.
- **Port Scan** - Scans a target IP against a list of common ports (FTP, SSH, Telnet, SMTP, DNS, HTTP, POP3, IMAP, HTTPS, SMB, MySQL, and common HTTP alt ports) and grabs a basic banner if available.
- **DNS Lookup** - Resolves a domain name to its IP address.
- **HTTP Header Sniffer** - Retrieves HTTP headers from a web server to identify technologies and server versions.
- **Full Scan** - Runs all of the above in sequence.

## Requirements

- Python 3.7+
- Optional: `colorama` for colored output

```bash
pip install colorama
```

## Platform Support

| Feature | Windows | Linux | Termux |
|---|---|---|---|
| WiFi Scan | Yes (netsh) | No | Yes (termux-api) |
| Current Connection Info | Yes (netsh) | No | Yes (termux-api) |
| Local Network Scan | Yes | Yes | Yes |
| Port Scan | Yes | Yes | Yes |
| DNS Lookup | Yes | Yes | Yes |
| HTTP Header Sniffer | Yes | Yes | Yes |

On Termux, WiFi features require the `Termux:API` app and the `termux-api` package:

```bash
pkg install termux-api
```

You will also need to grant location permission to Termux for WiFi scanning to work.

## Usage

Clone the repository and run the script directly:

```bash
git clone https://github.com/CryXcvv/your-repo-name.git
cd your-repo-name
python start.py
```

You will be greeted with a banner and a menu:

```
MENU
1. Scan WiFi Networks
2. Current WiFi Connection Info
3. Scan Local Network Devices (Export Enabled)
4. Port Scan
5. Full Scan
6. DNS Lookup (New)
7. HTTP Header Sniffer (New)
0. Exit
```

Select an option by entering its number.

## Notes

- Local network scanning relies on ICMP ping and ARP/neighbor table lookups. Results may vary depending on OS permissions and firewall settings.
- Port scanning checks only a fixed list of common ports and uses a short timeout, so it is meant for quick checks rather than a comprehensive scan.
- This tool is intended for scanning networks and devices you own or have explicit permission to test. Use responsibly.

## Author

**AvreyDev**
GitHub: [CryXcvv](https://github.com/CryXcvv)
```
