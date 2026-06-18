import os
import json
import time
import threading
from datetime import datetime
from utils import GREEN, WHITE, RESET, DIM, section, end_section, input_prompt, press_enter, OUTPUT_DIR

SESSION_DIR = os.path.join(OUTPUT_DIR, "sessions")

try:
    os.makedirs(SESSION_DIR, exist_ok=True)
except Exception:
    pass

session_history = []
schedule_active = False
schedule_thread = None
schedule_actions = []

def export_report():
    section("EXPORT REPORT")
    print("  1. Export as JSON")
    print("  2. Export as TXT")
    print("  3. Export as HTML")
    choice = input_prompt("  Choice: ")

    if not session_history:
        print(WHITE + "  [!] No scan data in current session." + RESET)
        end_section()
        return

    fname = input_prompt("  Filename (without extension): ") or f"report_{int(time.time())}"

    if choice == "1":
        _export_json(fname)
    elif choice == "2":
        _export_txt(fname)
    elif choice == "3":
        _export_html(fname)
    else:
        print(WHITE + "  [!] Invalid choice." + RESET)

    end_section()

def add_scan_data(data_type, data):
    session_history.append({
        "type": data_type,
        "data": data,
        "timestamp": datetime.now().isoformat()
    })

def _export_json(fname):
    path = os.path.join(OUTPUT_DIR, f"{fname}.json")
    try:
        with open(path, 'w') as f:
            json.dump(session_history, f, indent=4)
        print(GREEN + f"  [+] Exported to {path}" + RESET)
    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)

def _export_txt(fname):
    path = os.path.join(OUTPUT_DIR, f"{fname}.txt")
    try:
        with open(path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("Ginlo-Tools Scan Report\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write("=" * 60 + "\n\n")
            for entry in session_history:
                f.write(f"[{entry['timestamp']}] {entry['type']}\n")
                f.write("-" * 40 + "\n")
                f.write(json.dumps(entry['data'], indent=2))
                f.write("\n\n")
        print(GREEN + f"  [+] Exported to {path}" + RESET)
    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)

def _export_html(fname):
    path = os.path.join(OUTPUT_DIR, f"{fname}.html")
    try:
        rows = ""
        for entry in session_history:
            rows += f"""
            <div class="entry">
                <div class="entry-header">{entry['type']}</div>
                <div class="entry-time">{entry['timestamp']}</div>
                <pre>{json.dumps(entry['data'], indent=2)}</pre>
            </div>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Ginlo-Tools Report</title>
<style>
body {{ font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 20px; }}
h1 {{ text-align: center; border-bottom: 2px solid #00ff00; padding-bottom: 10px; }}
.entry {{ background: #111; border: 1px solid #333; margin: 10px 0; padding: 15px; border-radius: 5px; }}
.entry-header {{ color: #0f0; font-size: 1.2em; font-weight: bold; }}
.entry-time {{ color: #666; font-size: 0.8em; }}
pre {{ background: #000; padding: 10px; overflow-x: auto; color: #0f0; }}
</style>
</head>
<body>
<h1>Ginlo-Tools Scan Report</h1>
<p>Generated: {datetime.now().isoformat()}</p>
{rows}
</body>
</html>"""
        with open(path, 'w') as f:
            f.write(html)
        print(GREEN + f"  [+] Exported to {path}" + RESET)
    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)

def save_session():
    section("SAVE SESSION")
    if not session_history:
        print(WHITE + "  [!] No scan data to save." + RESET)
        end_section()
        return

    fname = input_prompt("  Session name: ") or f"session_{int(time.time())}"
    path = os.path.join(SESSION_DIR, f"{fname}.json")

    session_data = {
        "name": fname,
        "created": datetime.now().isoformat(),
        "entries": session_history
    }

    try:
        with open(path, 'w') as f:
            json.dump(session_data, f, indent=4)
        print(GREEN + f"  [+] Session saved to {path}" + RESET)

        all_sessions = _list_saved_sessions()
        print(DIM + f"  [*] Total saved sessions: {len(all_sessions)}" + RESET)
    except Exception as e:
        print(WHITE + f"  [!] Error: {e}" + RESET)
    end_section()

def _list_saved_sessions():
    if not os.path.exists(SESSION_DIR):
        return []
    sessions = []
    for fname in os.listdir(SESSION_DIR):
        if fname.endswith(".json"):
            sessions.append(fname)
    return sorted(sessions)

def _schedule_worker(interval, action_name, action_func):
    global schedule_active
    schedule_active = True
    while schedule_active:
        print(DIM + f"  [Schedule] Running {action_name}..." + RESET)
        try:
            action_func()
        except Exception as e:
            print(WHITE + f"  [!] Schedule error: {e}" + RESET)
        for _ in range(interval * 60):
            if not schedule_active:
                return
            time.sleep(1)

def schedule_scan():
    global schedule_active, schedule_thread

    section("SCHEDULE SCAN")
    if schedule_active:
        print(WHITE + "  [*] A schedule is already active." + RESET)
        stop = input_prompt("  Stop current schedule? (y/n): ")
        if stop.lower() == 'y':
            schedule_active = False
            print(GREEN + "  [+] Schedule stopped." + RESET)
        end_section()
        return

    print("  Available scans:")
    print("  1. Scan Local Network")
    print("  2. Port Scan (Common)")
    print("  3. Full Scan")
    scan_choice = input_prompt("  Choice: ")

    from network import scan_local_network
    from portscan import port_scan, COMMON_PORTS
    from wifi import windows_scan_wifi

    if scan_choice == "1":
        action = scan_local_network
        name = "Local Network Scan"
    elif scan_choice == "2":
        def port_scan_wrapper():
            ip = getattr(schedule_scan, 'last_target', None)
            if not ip:
                ip = input("  Target IP: ").strip()
                schedule_scan.last_target = ip
            if ip:
                port_scan(target=ip, ports=COMMON_PORTS)
        action = port_scan_wrapper
        name = "Port Scan"
    elif scan_choice == "3":
        def full_scan_wrapper():
            from utils import detect_os
            os_name = detect_os()
            if os_name == "windows":
                windows_scan_wifi()
            scan_local_network()
        action = full_scan_wrapper
        name = "Full Scan"
    else:
        print(WHITE + "  [!] Invalid choice." + RESET)
        end_section()
        return

    interval_str = input_prompt("  Interval (minutes): ")
    try:
        interval = int(interval_str)
        if interval < 1:
            raise ValueError
    except ValueError:
        print(WHITE + "  [!] Invalid interval. Using 5 minutes." + RESET)
        interval = 5

    schedule_active = True
    schedule_thread = threading.Thread(
        target=_schedule_worker, args=(interval, name, action), daemon=True
    )
    schedule_thread.start()
    print(GREEN + f"  [+] Scheduled '{name}' every {interval} minute(s)." + RESET)
    print(WHITE + "      Select option 20 again to stop." + RESET)
    end_section()
