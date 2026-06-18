<p align="center">
  <img src="assets/logo.png" alt="Logo" width="150">
</p>

<h1 align="center">Network Recon Toolkit</h1>

<p align="center">
  <img src="assets/banner.png" alt="Ginlo Flow Banner" width="100%">
</p>

A modular, menu-driven network reconnaissance CLI tool written in Python. Works across Windows, Linux, and Termux (Android) with green-lime gradient colored terminal output.

## Features

### WiFi & Network
- **Scan WiFi Networks** - Lists nearby WiFi networks with SSID, BSSID, signal strength, channel, and authentication type.
- **Current WiFi Connection Info** - Displays details about the currently active WiFi connection.
- **Scan Local Network Devices** - Discovers your local IP and subnet, pings all `/24` hosts in parallel, resolves MAC addresses and hostnames.
- **Custom Subnet Scan** - Scan any `/24` subnet (not just your own).
- **Traceroute** - Trace the network path to a target IP or domain.

### Port & Service
- **Port Scan (Common Ports)** - Scan against 13 common ports with banner grabbing.
- **Port Scan (Custom Range)** - Scan any port range (e.g. `1-10000`).
- **Service Version Detection** - Deep banner probing to identify service versions.

### Recon & Discovery
- **DNS Lookup** - Resolve a domain name to its IP address.
- **Reverse DNS Lookup** - Find domain names from an IP address.
- **HTTP Header Sniffer** - Fetch and display raw HTTP response headers.
- **GeoIP Lookup** - Geolocate any IP address (country, city, ISP, coordinates).
- **Public IP Check** - Display your public IP address.
- **MAC Vendor Lookup** - Identify hardware vendor from a MAC address.

### Security Audit
- **Weak Password Check** - Test FTP/SSH/Telnet against common default credentials.
- **Vulnerability Checker** - Match service banners against known CVEs.

### Tools
- **Full Scan** - Run all applicable scans in sequence.
- **Export Report** - Export session data as JSON, TXT, or HTML.
- **Save Session** - Persist scan results for later review.
- **Schedule Scan** - Run scans automatically at set intervals.

## Project Structure

```
Ginlo-Tools/
├── assets/
│   ├── banner.png
│   └── logo.png
├── downloads/           # Generated output files
│   ├── scan_*.json      # Network scan results
│   ├── report_*.json    # Exported reports (JSON/TXT/HTML)
│   └── sessions/        # Saved scan sessions
├── src/
│   ├── start.py       # Entry point & menu
│   ├── utils.py       # Shared utilities & gradient logo
│   ├── wifi.py        # WiFi scanning features
│   ├── network.py     # Network/subnet scanning
│   ├── portscan.py    # Port scanning & service detection
│   ├── recon.py       # DNS, GeoIP, HTTP, MAC, traceroute
│   ├── audit.py       # Password check & vulnerability check
│   └── report.py      # Export, session, scheduling
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.7+
- `colorama` for colored output

```bash
pip install -r requirements.txt
```

## Platform Support

| Feature | Windows | Linux | Termux |
|---|---|---|---|
| WiFi Scan | Yes (netsh) | No | Yes (termux-api) |
| Current Connection Info | Yes (netsh) | No | Yes (termux-api) |
| Local Network Scan | Yes | Yes | Yes |
| Custom Subnet Scan | Yes | Yes | Yes |
| Port Scan (Common/Custom) | Yes | Yes | Yes |
| Service Version Detection | Yes | Yes | Yes |
| DNS / Reverse DNS | Yes | Yes | Yes |
| HTTP Header Sniffer | Yes | Yes | Yes |
| GeoIP Lookup | Yes | Yes | Yes |
| Public IP Check | Yes | Yes | Yes |
| MAC Vendor Lookup | Yes | Yes | Yes |
| Traceroute | Yes | Yes | Yes |
| Weak Password Check | Yes | Yes | Yes |
| Vulnerability Checker | Yes | Yes | Yes |
| Full Scan | Yes | Yes | Yes |
| Export Report | Yes | Yes | Yes |
| Save Session | Yes | Yes | Yes |
| Schedule Scan | Yes | Yes | Yes |

On Termux, WiFi features require the `Termux:API` app and the `termux-api` package:

```bash
pkg install termux-api
```

You will also need to grant location permission to Termux for WiFi scanning to work.

## Usage

Clone the repository and run the script:

```bash
git clone https://github.com/CryXcvv/Ginlo-Tools.git
cd Ginlo-Tools
python src/start.py
```

You will be greeted with a gradient banner and a compact main menu:

```
+-[ MENU ]---------------------------------------+
|  1. WiFi & Network                             |
|  2. Port & Service                             |
|  3. Recon & Discovery                          |
|  4. Security Audit                             |
|  5. Tools                                      |
|                                                |
|  0. Exit                                       |
+------------------------------------------------+
```

Select a category to drill into its sub-menu, for example:

```
+-[ WIFI & NETWORK ]-----------------------------+
|  1. Scan WiFi Networks                         |
|  2. Current WiFi Connection Info               |
|  3. Scan Local Network Devices                 |
|  4. Custom Subnet Scan                         |
|  5. Traceroute                                 |
|                                                |
|  0. Back to Main Menu                          |
+------------------------------------------------+
```

## Notes

- Local network scanning relies on ICMP ping and ARP/neighbor table lookups. Results may vary depending on OS permissions and firewall settings.
- Port scanning uses configurable timeouts, meant for quick checks rather than comprehensive audits.
- Vulnerability checker uses a local CVE mapping for common services (Apache, Nginx, OpenSSH, vsftpd, ProFTPD).
- GeoIP and MAC vendor lookups require internet access (free public APIs).
- This tool is intended for scanning networks and devices you own or have explicit permission to test. Use responsibly.

## Author

**AvreyDev**
GitHub: [CryXcvv](https://github.com/CryXcvv)
