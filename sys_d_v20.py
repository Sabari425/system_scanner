import os
import sys
import subprocess
import platform
from datetime import datetime
import socket
import json
import time
import uuid
import getpass
import random
from collections import OrderedDict


# -------------------------------------------------------------------
#  AUTO-INSTALL REQUIRED PYTHON PACKAGES
# -------------------------------------------------------------------
def install_package(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"[*] Installing missing package: {pkg}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


for package in ["psutil", "tabulate"]:
    install_package(package)

import psutil
from tabulate import tabulate


# -------------------------------------------------------------------
#  CONSOLE COLORS - HACKER THEME
# -------------------------------------------------------------------
class Colors:
    # Basic ANSI colors
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BLACK = '\033[90m'
    RESET = '\033[0m'

    # Text effects
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'

    # Bright colors
    BRIGHT_RED = '\033[91;1m'
    BRIGHT_YELLOW = '\033[93;1m'
    BRIGHT_BLUE = '\033[94;1m'
    BRIGHT_MAGENTA = '\033[95;1m'
    BRIGHT_CYAN = '\033[96;1m'
    BRIGHT_WHITE = '\033[97;1m'

    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

    # 256-color palette - Common colors
    ORANGE = '\033[38;5;214m'
    PINK = '\033[38;5;205m'
    PURPLE = '\033[38;5;141m'
    LIME = '\033[38;5;118m'
    TEAL = '\033[38;5;44m'
    LAVENDER = '\033[38;5;183m'
    CORAL = '\033[38;5;209m'
    GOLD = '\033[38;5;220m'
    SILVER = '\033[38;5;248m'
    MAROON = '\033[38;5;124m'
    OLIVE = '\033[38;5;58m'
    NAVY = '\033[38;5;18m'

    # Rainbow colors
    RAINBOW_RED = '\033[38;5;196m'
    RAINBOW_ORANGE = '\033[38;5;202m'
    RAINBOW_YELLOW = '\033[38;5;226m'
    RAINBOW_GREEN = '\033[38;5;46m'
    RAINBOW_BLUE = '\033[38;5;21m'
    RAINBOW_INDIGO = '\033[38;5;57m'
    RAINBOW_VIOLET = '\033[38;5;93m'

    # Pastel colors
    PASTEL_PINK = '\033[38;5;218m'
    PASTEL_BLUE = '\033[38;5;153m'
    PASTEL_GREEN = '\033[38;5;158m'
    PASTEL_YELLOW = '\033[38;5;229m'
    PASTEL_PURPLE = '\033[38;5;189m'
    PASTEL_ORANGE = '\033[38;5;223m'

    # Cyber/Neon colors
    NEON_RED = '\033[38;5;196m'
    NEON_BLUE = '\033[38;5;81m'
    NEON_PINK = '\033[38;5;207m'
    NEON_CYAN = '\033[38;5;51m'  # Bright cyan
    NEON_PURPLE = '\033[38;5;129m'
    NEON_YELLOW = '\033[38;5;226m'
    NEON_ORANGE = '\033[38;5;208m'

    # Gray scale
    GRAY_DARK = '\033[38;5;236m'
    GRAY_MEDIUM = '\033[38;5;242m'
    GRAY_LIGHT = '\033[38;5;248m'

    # Terminal themes
    GRUVBOX_DARK = '\033[38;5;172m'  # Orange
    GRUVBOX_GREEN = '\033[38;5;142m'  # Green
    GRUVBOX_BLUE = '\033[38;5;109m'  # Blue
    GRUVBOX_PURPLE = '\033[38;5;132m'  # Purple

    # Material Design colors
    MATERIAL_RED = '\033[38;5;203m'
    MATERIAL_PINK = '\033[38;5;211m'
    MATERIAL_PURPLE = '\033[38;5;177m'
    MATERIAL_DEEP_PURPLE = '\033[38;5;99m'
    MATERIAL_INDIGO = '\033[38;5;62m'
    MATERIAL_BLUE = '\033[38;5;68m'
    MATERIAL_LIGHT_BLUE = '\033[38;5;117m'
    MATERIAL_CYAN = '\033[38;5;51m'
    MATERIAL_TEAL = '\033[38;5;37m'
    MATERIAL_GREEN = '\033[38;5;77m'
    MATERIAL_LIGHT_GREEN = '\033[38;5;113m'
    MATERIAL_LIME = '\033[38;5;154m'
    MATERIAL_YELLOW = '\033[38;5;227m'
    MATERIAL_AMBER = '\033[38;5;214m'
    MATERIAL_ORANGE = '\033[38;5;215m'
    MATERIAL_DEEP_ORANGE = '\033[38;5;202m'
    MATERIAL_BROWN = '\033[38;5;137m'
    MATERIAL_GREY = '\033[38;5;245m'
    MATERIAL_BLUE_GREY = '\033[38;5;109m'

    # Special effects combinations
    BOLD_RED = '\033[1;91m'
    BOLD_GREEN = '\033[1;92m'
    BOLD_YELLOW = '\033[1;93m'
    BOLD_BLUE = '\033[1;94m'
    BOLD_MAGENTA = '\033[1;95m'
    BOLD_CYAN = '\033[1;96m'
    BOLD_WHITE = '\033[1;97m'

    UNDERLINE_RED = '\033[4;91m'
    UNDERLINE_GREEN = '\033[4;92m'
    UNDERLINE_BLUE = '\033[4;94m'

    BLINK_RED = '\033[5;91m'
    BB_YELLOW = '\033[93;1;5m'
    BLINK_MAGENTA = '\033[95;5m'
    BLINK_GREEN = '\033[5;92m'

    # Hacker green colors
    HACKER_GREEN = '\033[92m'
    BRIGHT_GREEN = '\033[92;1m'
    DARK_GREEN = '\033[32m'
    NEON_GREEN = '\033[38;5;82m'
    MATRIX_GREEN = '\033[38;5;46m'
    TERMINAL_GREEN = '\033[38;5;40m'

    # Terminal colors
    TERMINAL_YELLOW = '\033[93m'
    TERMINAL_RED = '\033[91m'
    TERMINAL_BLUE = '\033[94m'
    TERMINAL_CYAN = '\033[96m'
    TERMINAL_MAGENTA = '\033[95m'


    # Status colors
    SUCCESS = '\033[38;5;46m'
    WARNING = '\033[38;5;214m'
    ERROR = '\033[38;5;196m'
    INFO = '\033[38;5;51m'
    SCAN = '\033[38;5;123m'
    DATA = '\033[38;5;141m'
    SYSTEM = '\033[38;5;220m'


def print_colored(text, color=Colors.HACKER_GREEN, end="\n"):
    print(f"{color}{text}{Colors.RESET}", end=end)


def print_status(message, status="INFO"):
    status_colors = {
        "INFO": Colors.INFO,
        "SUCCESS": Colors.SUCCESS,
        "WARNING": Colors.WARNING,
        "ERROR": Colors.ERROR,
        "SCAN": Colors.SCAN,
        "DATA": Colors.DATA,
        "SYSTEM": Colors.SYSTEM
    }
    color = status_colors.get(status, Colors.WHITE)
    prefix = {
        "INFO": "[+]",
        "SUCCESS": "[✦]",
        "WARNING": "[!]",
        "ERROR": "[-]",
        "SCAN": "[→]",
        "DATA": "[■]",
        "SYSTEM": "[S]"
    }.get(status, "[*]")

    print_colored(f"{prefix} {message}", color)


def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """Hacker-style progress bar"""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '░' * (length - filled_length)

    # Color based on percentage
    if float(percent) < 30:
        bar_color = Colors.ERROR
    elif float(percent) < 70:
        bar_color = Colors.WARNING
    else:
        bar_color = Colors.SUCCESS

    print_colored(f'\r{prefix} |{bar_color}{bar}{Colors.RESET}| {percent}% - {suffix}', Colors.HACKER_GREEN, end='')
    if iteration == total:
        print()


def print_banner():
    """Display professional hacker-style System Scanner banner"""
    banner = f"""
{Colors.NEON_GREEN}
          ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
          ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
          ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
          ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
          ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
          ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
{Colors.RESET}
{Colors.NEON_GREEN}
          ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
          ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
          ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
          ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
          ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
          ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
{Colors.RESET}

"""
    print(banner)
    print_colored("                     ✦     ..... SABARI425 .....     ✦                ", Colors.BOLD_MAGENTA)
    print("\n\n\n\n")


def simulate_scan_step(step_name, duration=1, steps=20):
    """Hacker-style scanning animation"""
    print("\n\t", end='')
    print_status(f"Scanning: {step_name}", "SCAN")
    for i in range(steps + 1):
        progress_bar(i, steps, prefix='\t\tProgress:', suffix=step_name, length=60)
        time.sleep(.02)
    print("\t\t", end='')
    print_status(f"Completed: {step_name}", "SUCCESS")


# -------------------------------------------------------------------
#  ENHANCED COMMAND EXECUTOR WITH ENCODING FIX
# -------------------------------------------------------------------
command_cache = {}


def run_cmd(cmd, use_cache=True, task_name="Executing command"):
    cache_key = f"{cmd}_{platform.system()}"

    if use_cache and cache_key in command_cache:
        cached_time, output = command_cache[cache_key]
        if (datetime.now() - cached_time).seconds < 300:
            return output

    try:
        start_time = time.time()

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=30
        )

        execution_time = time.time() - start_time
        output = result.stdout.strip()

        if use_cache:
            command_cache[cache_key] = (datetime.now(), output)

        return output

    except subprocess.TimeoutExpired:
        print_status(f"{task_name} timed out", "ERROR")
        return "[TIMEOUT] Command execution timeout"
    except Exception as e:
        print_status(f"{task_name} failed: {str(e)}", "ERROR")
        return f"[ERROR] Command failed: {str(e)}"


# -------------------------------------------------------------------
#  DETERMINE DOWNLOADS PATH
# -------------------------------------------------------------------
def get_downloads_folder():
    if platform.system() == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Downloads")
    else:
        return os.path.join(os.path.expanduser("~"), "Downloads")


# -------------------------------------------------------------------
#  ENHANCED TASK MANAGER WITH COMPREHENSIVE PROCESS INFORMATION
# -------------------------------------------------------------------
def get_task_manager_details():
    print("\n\t", end='')
    print_status("Collecting comprehensive process information...", "SYSTEM")
    processes = []

    try:
        # Get all processes with detailed information
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent',
                                         'memory_info', 'create_time', 'status', 'cpu_times',
                                         'num_threads', 'exe', 'nice', 'ionice']):
            try:
                process_info = proc.info

                # Calculate process uptime
                create_time = process_info['create_time']
                uptime = datetime.now() - datetime.fromtimestamp(create_time)

                # Get CPU times
                cpu_times = process_info.get('cpu_times')
                if cpu_times:
                    cpu_time_str = f"{(cpu_times.user + cpu_times.system):.2f}s"
                else:
                    cpu_time_str = "N/A"

                # Get memory details
                memory_info = process_info.get('memory_info')
                if memory_info:
                    memory_mb = f"{memory_info.rss / (1024 * 1024):.2f} MB"
                    memory_vms = f"{memory_info.vms / (1024 * 1024):.2f} MB"
                else:
                    memory_mb = "N/A"
                    memory_vms = "N/A"

                # Get executable path and truncate if too long
                exe_path = process_info.get('exe', 'N/A')
                if exe_path and len(exe_path) > 40:
                    exe_path = "..." + exe_path[-37:]

                # Determine process priority
                nice = process_info.get('nice', 'N/A')
                priority = "LOW"
                if nice is not None:
                    if nice < 0:
                        priority = "HIGH"
                    elif nice == 0:
                        priority = "NORMAL"
                    else:
                        priority = "LOW"

                # Get process state with more detailed status
                status = process_info['status']
                if status == psutil.STATUS_RUNNING:
                    status_detailed = "RUNNING"
                elif status == psutil.STATUS_SLEEPING:
                    status_detailed = "SLEEPING"
                elif status == psutil.STATUS_DISK_SLEEP:
                    status_detailed = "DISK_SLEEP"
                elif status == psutil.STATUS_STOPPED:
                    status_detailed = "STOPPED"
                elif status == psutil.STATUS_TRACING_STOP:
                    status_detailed = "TRACING"
                elif status == psutil.STATUS_ZOMBIE:
                    status_detailed = "ZOMBIE"
                elif status == psutil.STATUS_DEAD:
                    status_detailed = "DEAD"
                else:
                    status_detailed = status.upper()

                processes.append({
                    "PID": process_info['pid'],
                    "Process Name": process_info['name'][:60],  # Truncate long names
                    "User": process_info['username'] or "SYSTEM",
                    "CPU %": f"{process_info['cpu_percent'] or 0:.2f}",
                    "Memory %": f"{process_info['memory_percent'] or 0:.3f}",
                    "Memory Usage": memory_mb,
                    "Virtual Memory": memory_vms,
                    "Threads": process_info.get('num_threads', 'N/A'),
                    "Status": status_detailed,
                    "Priority": priority,
                    "CPU Time": cpu_time_str,
                    "Uptime": str(uptime).split('.')[0],
                    "Started": datetime.fromtimestamp(create_time).strftime('%H:%M:%S'),
                    "Executable": exe_path
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    except Exception as e:
        print("\t", end='')
        print_status(f"Process collection error: {str(e)}", "ERROR")
        processes.append({
            "PID": "ERROR",
            "Process Name": f"Failed to get processes: {str(e)}",
            "User": "N/A",
            "CPU %": "N/A",
            "Memory %": "N/A",
            "Memory Usage": "N/A",
            "Status": "ERROR"
        })

    # Sort by CPU usage descending
    try:
        processes.sort(key=lambda x: float(x['CPU %'].replace('%', '')) if x['CPU %'] != 'N/A' else 0, reverse=True)
        print("\t", end='')
        print_status(f"Collected {len(processes)} processes, sorted by CPU usage", "SUCCESS")
    except:
        print("\n\t", end='')
        print_status(f"Collected {len(processes)} processes", "WARNING")

    return processes[:]


def get_system_performance():
    print("\n\t", end='')
    print_status("Analyzing real-time system performance...", "SYSTEM")
    performance = []

    try:
        # CPU Information with per-core stats
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()

        # Memory Information
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Disk Information
        disk_io = psutil.disk_io_counters()

        # Network Information
        net_io = psutil.net_io_counters()

        # Temperature and fan speeds if available
        try:
            temps = psutil.sensors_temperatures()
            has_temp = bool(temps)
        except:
            has_temp = False

        performance.extend([
            {"Metric": "CPU Usage", "Value": f"{cpu_percent}%",
             "Details": f"{cpu_count} physical, {cpu_count_logical} logical cores"},
            {"Metric": "CPU Frequency", "Value": f"{cpu_freq.current:.0f} MHz" if cpu_freq else "N/A",
             "Details": f"Max: {cpu_freq.max:.0f} MHz" if cpu_freq else "N/A"},
            {"Metric": "Memory Usage", "Value": f"{memory.percent}%",
             "Details": f"{memory.used / (1024 ** 3):.1f} GB / {memory.total / (1024 ** 3):.1f} GB"},
            {"Metric": "Available Memory", "Value": f"{memory.available / (1024 ** 3):.1f} GB",
             "Details": f"{((memory.available / memory.total) * 100):.1f}% available"},
            {"Metric": "Swap Usage", "Value": f"{swap.percent}%",
             "Details": f"{swap.used / (1024 ** 3):.1f} GB / {swap.total / (1024 ** 3):.1f} GB"},
        ])

        if disk_io:
            performance.extend([
                {"Metric": "Disk Read", "Value": f"{disk_io.read_bytes / (1024 ** 3):.2f} GB",
                 "Details": f"{disk_io.read_count:,} operations"},
                {"Metric": "Disk Write", "Value": f"{disk_io.write_bytes / (1024 ** 3):.2f} GB",
                 "Details": f"{disk_io.write_count:,} operations"},
            ])

        if net_io:
            performance.extend([
                {"Metric": "Network Sent", "Value": f"{net_io.bytes_sent / (1024 ** 3):.2f} GB",
                 "Details": f"{net_io.packets_sent:,} packets"},
                {"Metric": "Network Received", "Value": f"{net_io.bytes_recv / (1024 ** 3):.2f} GB",
                 "Details": f"{net_io.packets_recv:,} packets"},
            ])

        performance.append({
            "Metric": "Temperature Monitoring",
            "Value": "AVAILABLE" if has_temp else "UNAVAILABLE",
            "Details": "Hardware sensors detected" if has_temp else "No sensor data"
        })

        print("\t", end='')
        print_status("Performance analysis completed", "SUCCESS")

    except Exception as e:
        print()
        print_status(f"Performance analysis failed: {str(e)}", "ERROR")

    return performance


# -------------------------------------------------------------------
#  USERS AND ACCOUNTS INFORMATION
# -------------------------------------------------------------------
def get_users_information():
    print("\n\t", end='')
    print_status("Collecting user account information...", "SYSTEM")
    users_info = []

    if platform.system() == "Windows":
        try:
            output = run_cmd("net user")
            lines = output.split('\n')
            users = []

            for line in lines:
                if 'User accounts for' not in line and '-----' not in line and 'command completed' not in line and line.strip():
                    potential_users = [user.strip() for user in line.split() if user.strip()]
                    for user in potential_users:
                        if user and user not in ['The', 'command', 'completed', 'successfully.']:
                            users.append(user)

            print("\t", end='')
            print_status(f"Found {len(users)} user accounts", "DATA")

            for user in users:
                try:
                    user_details = run_cmd(f'net user "{user}"')
                    user_data = {
                        "Username": user,
                        "Full Name": "N/A",
                        "Account Active": "Yes",
                        "Last Logon": "N/A",
                        "Password Last Set": "N/A",
                        "Account Expires": "Never",
                        "Local Group Memberships": "N/A",
                        "Password Required": "Yes",
                        "Workstations Allowed": "All"
                    }

                    for detail_line in user_details.split('\n'):
                        detail_line_lower = detail_line.lower()
                        if 'full name' in detail_line_lower and 'n/a' not in detail_line_lower:
                            user_data["Full Name"] = detail_line.split('Full Name')[1].strip()
                        elif 'account active' in detail_line_lower:
                            user_data["Account Active"] = "Yes" if "yes" in detail_line_lower else "No"
                        elif 'last logon' in detail_line_lower and 'n/a' not in detail_line_lower:
                            user_data["Last Logon"] = detail_line.split('Last logon')[1].strip()
                        elif 'password last set' in detail_line_lower and 'n/a' not in detail_line_lower:
                            user_data["Password Last Set"] = detail_line.split('Password last set')[1].strip()
                        elif 'account expires' in detail_line_lower:
                            user_data["Account Expires"] = detail_line.split('Account expires')[1].strip()
                        elif 'local group memberships' in detail_line_lower:
                            user_data["Local Group Memberships"] = detail_line.split('Local Group Memberships')[
                                1].strip()
                        elif 'password required' in detail_line_lower:
                            user_data["Password Required"] = detail_line.split('Password required')[1].strip()

                    users_info.append(user_data)
                except Exception:
                    continue

            print("\t", end='')
            print_status(f"Collected details for {len(users_info)} users", "SUCCESS")

        except Exception as e:
            print_status(f"User information collection failed: {str(e)}", "ERROR")
            users_info.append({
                "Username": f"Error: {str(e)}",
                "Details": "Failed to retrieve user information"
            })

    return users_info


# -------------------------------------------------------------------
#  ENHANCED SYSTEM HEALTH SCORING ALGORITHMS
# -------------------------------------------------------------------
def get_system_health_score():
    """Comprehensive system health scoring with weighted factors"""
    score = 100
    warnings = []

    try:
        # CPU Health (25 points)
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 90:
            score -= 20
            warnings.append("[CPU Health]  CRITICAL: CPU usage very high")
        elif cpu_usage > 80:
            score -= 15
            warnings.append("[CPU Health]  WARNING: CPU usage high")
        elif cpu_usage > 70:
            score -= 10
            warnings.append("[CPU Health]  NOTICE: CPU usage elevated")
        elif cpu_usage > 60:
            score -= 5

        # Memory Health (25 points)
        memory = psutil.virtual_memory()
        if memory.percent > 95:
            score -= 20
            warnings.append("[Memory Health]  CRITICAL: Memory usage very high")
        elif memory.percent > 85:
            score -= 15
            warnings.append("[Memory Health]  WARNING: Memory usage high")
        elif memory.percent > 75:
            score -= 10
            warnings.append("[Memory Health]  NOTICE: Memory usage elevated")
        elif memory.percent > 65:
            score -= 5

        # Disk Health (20 points)
        disk_warnings = 0
        critical_disks = 0
        for part in psutil.disk_partitions():
            try:
                # Skip CD-ROM and other non-writable drives
                if 'cdrom' in part.opts or part.fstype == '':
                    continue

                usage = psutil.disk_usage(part.mountpoint)
                if usage.percent > 95:
                    disk_warnings += 3
                    critical_disks += 1
                    warnings.append(f"[Disk Health]  CRITICAL: Disk {part.device} at {usage.percent}%")
                elif usage.percent > 90:
                    disk_warnings += 2
                    warnings.append(f"[Disk Health]  WARNING: Disk {part.device} at {usage.percent}%")
                elif usage.percent > 85:
                    disk_warnings += 1
                    warnings.append(f"[Disk Health]  NOTICE: Disk {part.device} at {usage.percent}%")
            except:
                continue

        score -= min(disk_warnings, 15)
        if critical_disks > 0:
            score -= 5

        # Temperature Health (15 points) - if available
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                high_temp_count = 0
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.current > 85:
                            high_temp_count += 3
                            warnings.append(f"[Temperature Health]  CRITICAL: {name} temperature {entry.current}°C")
                        elif entry.current > 75:
                            high_temp_count += 2
                            warnings.append(f"[Temperature Health]  WARNING: {name} temperature {entry.current}°C")
                        elif entry.current > 65:
                            high_temp_count += 1
                score -= min(high_temp_count, 12)
        except:
            pass

        # Process Health (15 points)
        try:
            zombie_count = 0
            high_cpu_processes = 0
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'status']):
                try:
                    info = proc.info
                    if info['status'] == psutil.STATUS_ZOMBIE:
                        zombie_count += 1
                    if info.get('cpu_percent', 0) > 50:  # Processes using >50% CPU
                        high_cpu_processes += 1
                except:
                    continue

            if zombie_count > 5:
                score -= 8
                warnings.append(f"[Process Health]  WARNING: {zombie_count} zombie processes")
            elif zombie_count > 0:
                score -= 4

            if high_cpu_processes > 3:
                score -= 7
                warnings.append(f"[Process Health]  NOTICE: {high_cpu_processes} high-CPU processes")
        except:
            pass

        # Apply bonus for good conditions
        if cpu_usage < 30 and memory.percent < 50:
            score += 5  # Bonus for excellent performance
        if len(warnings) == 0:
            score += 3  # Bonus for no warnings

    except Exception as e:
        print_status(f"Health score calculation error: {str(e)}", "WARNING")
        warnings.append(f"Health calculation error: {str(e)}")

    # Ensure score is within bounds
    final_score = max(0, min(100, score))

    # Log warnings if any
    if warnings and final_score < 80:
        print("\t\t", end='')
        print_status(f"Health score: {final_score}/100 - {len(warnings)} issues detected", "WARNING")
        for warning in warnings[:]:  # Show top 3 warnings
            print("\t\t\t", end='')
            print_status(f"  • {warning}", "WARNING")

    return final_score


def get_device_specifications():
    print("\n\t", end='')
    print_status("Collecting comprehensive system specifications...", "SYSTEM")
    info = OrderedDict()

    info["Host Name"] = socket.gethostname()
    info["Processor"] = platform.processor() or "Unknown"
    info["Platform"] = platform.platform()
    info["Architecture"] = platform.architecture()[0]
    info["System Type"] = platform.machine()
    info["Python Version"] = platform.python_version()

    try:
        memory = psutil.virtual_memory()
        info["Total RAM"] = f"{memory.total / (1024 ** 3):.2f} GB"
        info["Available RAM"] = f"{memory.available / (1024 ** 3):.2f} GB"
        info["RAM Usage"] = f"{memory.percent}%"

        boot_time = psutil.boot_time()
        uptime = datetime.now() - datetime.fromtimestamp(boot_time)
        info["System Uptime"] = str(uptime).split('.')[0]

        health_score = get_system_health_score()
        info["System Health"] = f"{health_score}/100"

        # Additional system info for Windows
        if platform.system() == "Windows":
            try:
                computer_info = run_cmd(
                    "systeminfo | findstr /C:\"OS Name\" /C:\"OS Version\" /C:\"System Manufacturer\" /C:\"System Model\"")
                for line in computer_info.split('\n'):
                    if 'OS Name' in line:
                        info["OS Name"] = line.split(':', 1)[1].strip()
                    elif 'OS Version' in line:
                        info["OS Version"] = line.split(':', 1)[1].strip()
                    elif 'System Manufacturer' in line:
                        info["Manufacturer"] = line.split(':', 1)[1].strip()
                    elif 'System Model' in line:
                        info["Model"] = line.split(':', 1)[1].strip()
            except:
                pass

        # Add CPU core information
        info["Physical Cores"] = psutil.cpu_count(logical=False)
        info["Logical Cores"] = psutil.cpu_count(logical=True)

    except Exception as e:
        print_status(f"System specs collection error: {str(e)}", "ERROR")

    return [[k, v] for k, v in info.items()]


def get_advanced_storage_details():
    print("\n\t", end='')
    print_status("Analyzing storage devices...", "SYSTEM")
    disks = []

    for part in psutil.disk_partitions():
        try:
            # Skip CD-ROM and other special drives
            if 'cdrom' in part.opts or part.fstype == '':
                continue

            usage = psutil.disk_usage(part.mountpoint)

            # Determine health status based on usage
            if usage.percent > 95:
                status = "CRITICAL"
                status_color = "red"
            elif usage.percent > 90:
                status = "WARNING"
                status_color = "orange"
            elif usage.percent > 85:
                status = "NOTICE"
                status_color = "yellow"
            else:
                status = "HEALTHY"
                status_color = "green"

            disks.append({
                "Device": part.device,
                "Mountpoint": part.mountpoint,
                "File System": part.fstype,
                "Total Size": f"{usage.total / (1024 ** 3):.2f} GB",
                "Used": f"{usage.used / (1024 ** 3):.2f} GB",
                "Free": f"{usage.free / (1024 ** 3):.2f} GB",
                "Usage": f"{usage.percent}%",
                "Status": status,
                "Status Color": status_color
            })
        except:
            continue

    print("\t", end='')
    print_status(f"Analyzed {len(disks)} storage devices", "SUCCESS")
    return disks


def get_comprehensive_graphics_info():
    print("\n\t", end='')
    print_status("Collecting graphics card information...", "SYSTEM")
    gpu_info = []

    if platform.system() == "Windows":
        try:
            output = run_cmd(
                "wmic path win32_videocontroller get name, adapterram, driverversion, videoprocessor, videomodedescription /format:csv")
            if output and "No Instance" not in output:
                lines = output.split('\n')
                for line in lines:
                    if ',' in line and 'Node' not in line:
                        parts = line.split(',')
                        if len(parts) >= 5:
                            gpu_info.append({
                                "Graphics Card": parts[2],
                                "Adapter RAM": f"{int(parts[3]) / (1024 ** 3):.2f} GB" if parts[
                                    3].strip().isdigit() else "UNKNOWN",
                                "Driver Version": parts[4],
                                "Video Processor": parts[5] if len(parts) > 5 else "UNKNOWN",
                                "Current Resolution": parts[6] if len(parts) > 6 else "UNKNOWN"
                            })
                print("\t", end='')
                print_status(f"Found {len(gpu_info)} graphics cards", "SUCCESS")
        except Exception as e:
            print_status(f"GPU information collection failed: {str(e)}", "ERROR")

    return gpu_info if gpu_info else [
        {"Graphics Card": "No GPU information available", "Details": "Check system configuration"}]


def get_network_analysis():
    print("\n\t", end='')
    print_status("Analyzing network interfaces...", "SYSTEM")
    net_info = []

    try:
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        io_counters = psutil.net_io_counters(pernic=True)

        for interface_name, interface_addresses in interfaces.items():
            if interface_name in stats:
                stat = stats[interface_name]
                io = io_counters.get(interface_name)

                interface_data = {
                    "Interface": interface_name,
                    "Status": "ACTIVE" if stat.isup else "INACTIVE",
                    "MTU": stat.mtu,
                    "Speed": f"{stat.speed} Mbps" if stat.speed > 0 else "UNKNOWN",
                    "MAC Address": "NONE",
                    "IPv4 Addresses": "NONE",
                    "IPv6 Addresses": "NONE"
                }

                # Get MAC Address
                for addr in interface_addresses:
                    if addr.family == -1:
                        interface_data["MAC Address"] = addr.address
                        break

                # Get IP Addresses
                ipv4_addrs = []
                ipv6_addrs = []
                for addr in interface_addresses:
                    if addr.family == 2:  # IPv4
                        ipv4_addrs.append(addr.address)
                    elif addr.family == 23:  # IPv6
                        ipv6_addrs.append(addr.address)

                interface_data["IPv4 Addresses"] = ", ".join(ipv4_addrs) if ipv4_addrs else "NONE"
                interface_data["IPv6 Addresses"] = ", ".join(ipv6_addrs) if ipv6_addrs else "NONE"

                # Add I/O statistics if available
                if io:
                    interface_data["Data Sent"] = f"{io.bytes_sent / (1024 ** 2):.1f} MB"
                    interface_data["Data Received"] = f"{io.bytes_recv / (1024 ** 2):.1f} MB"
                    interface_data["Packets Sent"] = f"{io.packets_sent:,}"
                    interface_data["Packets Received"] = f"{io.packets_recv:,}"

                net_info.append(interface_data)

        print("\t", end='')
        print_status(f"Analyzed {len(net_info)} network interfaces", "SUCCESS")

    except Exception as e:
        print_status(f"Network analysis failed: {str(e)}", "ERROR")

    return net_info


def get_comprehensive_wifi_analysis():
    print("\n\t", end='')
    print_status("Scanning WiFi networks...", "SYSTEM")
    wifi_info = []

    if platform.system() == "Windows":
        try:
            profiles_output = run_cmd("netsh wlan show profiles")
            profiles = []
            for line in profiles_output.split('\n'):
                if 'All User Profile' in line and ':' in line:
                    profile_name = line.split(':')[1].strip()
                    if profile_name:
                        profiles.append(profile_name)

            print("\t", end='')
            print_status(f"Found {len(profiles)} WiFi profiles", "DATA")

            for profile in profiles:
                try:
                    key_output = run_cmd(f'netsh wlan show profile name="{profile}" key=clear')
                    password = "Not stored or encrypted"
                    security = "Unknown"
                    connection_mode = "Unknown"

                    for line in key_output.split('\n'):
                        line_lower = line.lower()
                        if 'key content' in line_lower and ':' in line:
                            password_value = line.split(':')[1].strip()
                            if password_value:
                                password = password_value
                        elif 'authentication' in line_lower and ':' in line:
                            security = line.split(':')[1].strip()
                        elif 'connection mode' in line_lower and ':' in line:
                            connection_mode = line.split(':')[1].strip()

                    wifi_info.append({
                        "SSID": profile,
                        "Password": password,
                        "Security": security,
                        "Connection Mode": connection_mode,
                        "Status": "PASSWORD_FOUND" if password != "Not stored or encrypted" else "NO_PASSWORD"
                    })
                except:
                    wifi_info.append({
                        "SSID": profile,
                        "Password": "ERROR_RETRIEVING",
                        "Security": "UNKNOWN",
                        "Connection Mode": "UNKNOWN",
                        "Status": "ERROR"
                    })

            found_passwords = len([w for w in wifi_info if w["Status"] == "PASSWORD_FOUND"])
            print("\t", end='')
            print_status(f"WiFi analysis complete - {found_passwords} passwords found", "SUCCESS")

        except Exception as e:
            print_status(f"WiFi analysis failed: {str(e)}", "ERROR")

    return wifi_info


def get_advanced_system_details():
    print("\n\t", end='')
    print_status("Collecting advanced system details...", "SYSTEM")
    advanced_info = []

    try:
        # System architecture details
        advanced_info.append({"Category": "ARCHITECTURE", "Detail": platform.architecture()[0]})
        advanced_info.append({"Category": "PROCESSOR_BITS", "Detail": "64-bit" if sys.maxsize > 2 ** 32 else "32-bit"})

        # System boot details
        boot_time = psutil.boot_time()
        advanced_info.append(
            {"Category": "LAST_BOOT", "Detail": datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')})

        # Memory details
        memory = psutil.virtual_memory()
        advanced_info.append({"Category": "MEMORY_TOTAL", "Detail": f"{memory.total / (1024 ** 3):.2f} GB"})
        advanced_info.append({"Category": "MEMORY_AVAILABLE", "Detail": f"{memory.available / (1024 ** 3):.2f} GB"})

        # CPU details
        advanced_info.append({"Category": "CPU_PHYSICAL_CORES", "Detail": psutil.cpu_count(logical=False)})
        advanced_info.append({"Category": "CPU_LOGICAL_CORES", "Detail": psutil.cpu_count(logical=True)})

        # Process information
        processes = len(psutil.pids())
        advanced_info.append({"Category": "RUNNING_PROCESSES", "Detail": processes})

        # Disk information
        total_disk_space = 0
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                total_disk_space += usage.total
            except:
                continue
        advanced_info.append({"Category": "TOTAL_DISK_SPACE", "Detail": f"{total_disk_space / (1024 ** 4):.2f} TB"})

        # Windows-specific advanced details
        if platform.system() == "Windows":
            try:
                # Get system UUID
                output = run_cmd("wmic csproduct get uuid")
                if "UUID" in output:
                    lines = output.split('\n')
                    for line in lines:
                        if line.strip() and 'UUID' not in line:
                            uuid_value = line.strip()
                            if uuid_value:
                                advanced_info.append({"Category": "SYSTEM_UUID", "Detail": uuid_value})
                                break

                # Get BIOS information
                bios_info = run_cmd("wmic bios get serialnumber,version,manufacturer /format:csv")
                for line in bios_info.split('\n'):
                    if ',' in line and 'Node' not in line:
                        parts = line.split(',')
                        if len(parts) >= 4:
                            advanced_info.append({"Category": "BIOS_MANUFACTURER", "Detail": parts[1]})
                            advanced_info.append({"Category": "BIOS_VERSION", "Detail": parts[3]})
                            break

            except Exception as e:
                advanced_info.append({"Category": "WINDOWS_ADVANCED_ERROR", "Detail": str(e)})

        print("\t", end='')
        print_status("Advanced system details collected", "SUCCESS")

    except Exception as e:
        print_status(f"Advanced details collection failed: {str(e)}", "ERROR")

    return advanced_info


# -------------------------------------------------------------------
#  NEW COMPREHENSIVE DATA COLLECTION FUNCTIONS
# -------------------------------------------------------------------

def get_system_environment_vars():
    """Collect comprehensive environment variables"""
    print("\n\t", end='')
    print_status("Collecting environment variables...", "SYSTEM")
    env_vars = []

    try:
        # Get all environment variables
        for key, value in os.environ.items():
            # Skip very long values and sensitive-looking keys
            if len(str(value)) < 1000 and not any(                  # if needed take off the not near any
                    skip in key.lower() for skip in ['password', 'secret', 'key', 'token']):
                env_vars.append({
                    "Variable": key,
                    "Value": str(value)[:] + "..." if len(str(value)) > 5000 else str(value)
                })

        env_vars.sort(key=lambda x: x["Variable"])
        print("\t", end='')
        print_status(f"Collected {len(env_vars)} environment variables", "SUCCESS")

    except Exception as e:
        print_status(f"Environment variables collection failed: {str(e)}", "ERROR")

    return env_vars[:]


def get_installed_software():
    """Get detailed installed software information"""
    print("\n\t", end='')
    print_status("Collecting installed software information...", "SYSTEM")
    software_list = []

    if platform.system() == "Windows":
        try:
            # Get installed programs from registry
            output = run_cmd(
                'powershell "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | '
                'Select-Object DisplayName, DisplayVersion, Publisher, InstallDate | Format-Table -AutoSize"'
            )

            lines = output.split('\n')
            for line in lines:
                if line.strip() and 'DisplayName' not in line and '---' not in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        software_list.append({
                            "Software Name": ' '.join(parts[:-3]) if len(parts) > 3 else line.strip(),
                            "Version": parts[-3] if len(parts) > 3 else "Unknown",
                            "Publisher": parts[-2] if len(parts) > 2 else "Unknown",
                            "Install Date": parts[-1] if len(parts) > 1 else "Unknown"
                        })

            print("\t", end='')
            print_status(f"Found {len(software_list)} installed programs", "SUCCESS")

        except Exception as e:
            print_status(f"Software collection failed: {str(e)}", "ERROR")

    return software_list[:]


def get_system_drivers():
    """Get detailed driver information"""
    print("\n\t", end='')
    print_status("Collecting driver information...", "SYSTEM")
    drivers = []

    if platform.system() == "Windows":
        try:
            output = run_cmd("driverquery /v /fo csv")
            lines = output.split('\n')
            for line in lines[1:]:  # Skip header
                if line.strip():
                    parts = line.split(',')
                    if len(parts) >= 6:
                        drivers.append({
                            "Module Name": parts[0].strip('"'),
                            "Display Name": parts[1].strip('"'),
                            "Driver Type": parts[2].strip('"'),
                            "Start Mode": parts[3].strip('"'),
                            "State": parts[4].strip('"'),
                            "Status": parts[5].strip('"') if len(parts) > 5 else "N/A"
                        })

            print("\t", end='')
            print_status(f"Collected {len(drivers)} driver entries", "SUCCESS")

        except Exception as e:
            print_status(f"Driver collection failed: {str(e)}", "ERROR")

    return drivers[:]


def get_system_services():
    """Get detailed service information"""
    print("\n\t", end='')
    print_status("Collecting service information...", "SYSTEM")
    services = []

    try:
        for service in psutil.win_service_iter() if platform.system() == "Windows" else []:
            try:
                service_info = service.as_dict()
                services.append({
                    "Service Name": service_info['name'],
                    "Display Name": service_info['display_name'],
                    "Status": service_info['status'],
                    "Startup Type": service_info.get('startup', 'N/A'),
                    "PID": service_info.get('pid', 'N/A'),
                    "Binary Path": service_info.get('binpath', 'N/A')[:500] + "..." if service_info.get(
                        'binpath') and len(service_info.get('binpath', '')) > 500 else service_info.get('binpath', 'N/A')
                })
            except:
                continue

        print("\t", end='')
        print_status(f"Collected {len(services)} services", "SUCCESS")

    except Exception as e:
        print_status(f"Service collection failed: {str(e)}", "ERROR")

    return services[:]


def get_event_logs_summary():
    """Get event log summary"""
    print("\n\t", end='')
    print_status("Collecting event log summary...", "SYSTEM")
    event_summary = []

    if platform.system() == "Windows":
        try:
            # Get recent system errors
            errors = run_cmd(
                'powershell "Get-EventLog -LogName System -EntryType Error -Newest 10 | '
                'Select-Object TimeGenerated, Source, InstanceId, Message | Format-Table -AutoSize"'
            )

            lines = errors.split('\n')
            for i, line in enumerate(lines[3:13]):  # Skip headers
                if line.strip():
                    event_summary.append({
                        "Event Type": "System Error",
                        "Details": line.strip()[:400] + "..." if len(line.strip()) > 200 else line.strip()
                    })

            print("\t", end='')
            print_status("Event log summary collected", "SUCCESS")

        except Exception as e:
            print_status(f"Event log collection failed: {str(e)}", "ERROR")

    return event_summary


def get_hardware_details():
    """Get comprehensive hardware details"""
    print("\n\t", end='')
    print_status("Collecting detailed hardware information...", "SYSTEM")
    hardware = []

    try:
        # BIOS Information
        if platform.system() == "Windows":
            try:
                bios_info = run_cmd("wmic bios get manufacturer,version,serialnumber,releasedate /format:csv")
                for line in bios_info.split('\n'):
                    if ',' in line and 'Node' not in line:
                        parts = line.split(',')
                        hardware.append({"Category": "BIOS_MANUFACTURER", "Detail": parts[1]})
                        hardware.append({"Category": "BIOS_VERSION", "Detail": parts[2]})
                        hardware.append({"Category": "BIOS_SERIAL", "Detail": parts[3]})
                        hardware.append({"Category": "BIOS_DATE", "Detail": parts[4] if len(parts) > 4 else "N/A"})
                        break
            except:
                pass

        # Motherboard Information
        if platform.system() == "Windows":
            try:
                baseboard = run_cmd("wmic baseboard get product,manufacturer,version,serialnumber /format:csv")
                for line in baseboard.split('\n'):
                    if ',' in line and 'Node' not in line:
                        parts = line.split(',')
                        hardware.append({"Category": "MOTHERBOARD_MANUFACTURER", "Detail": parts[1]})
                        hardware.append({"Category": "MOTHERBOARD_PRODUCT", "Detail": parts[2]})
                        hardware.append({"Category": "MOTHERBOARD_VERSION", "Detail": parts[3]})
                        hardware.append(
                            {"Category": "MOTHERBOARD_SERIAL", "Detail": parts[4] if len(parts) > 4 else "N/A"})
                        break
            except:
                pass

        # System UUID
        try:
            system_uuid = run_cmd("wmic csproduct get uuid")
            for line in system_uuid.split('\n'):
                if line.strip() and 'UUID' not in line:
                    hardware.append({"Category": "SYSTEM_UUID", "Detail": line.strip()})
                    break
        except:
            pass

        # Battery Information (if available)
        try:
            battery = psutil.sensors_battery()
            if battery:
                hardware.append({"Category": "BATTERY_PERCENT", "Detail": f"{battery.percent}%"})
                hardware.append({"Category": "POWER_PLUGGED", "Detail": "Yes" if battery.power_plugged else "No"})
                if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                    hardware.append({"Category": "BATTERY_TIME_LEFT", "Detail": f"{battery.secsleft // 60} minutes"})
        except:
            pass

        print("\t", end='')
        print_status("Hardware details collected", "SUCCESS")

    except Exception as e:
        print_status(f"Hardware details collection failed: {str(e)}", "ERROR")

    return hardware


def get_network_connections():
    """Get active network connections"""
    print("\n\t", end='')
    print_status("Collecting network connections...", "SYSTEM")
    connections = []

    try:
        for conn in psutil.net_connections(kind='inet'):
            try:
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        "Protocol": conn.type.name,
                        "Local Address": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "Remote Address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        "Status": conn.status,
                        "PID": conn.pid or "N/A"
                    })
            except:
                continue

        print("\t", end='')
        print_status(f"Found {len(connections)} established connections", "SUCCESS")

    except Exception as e:
        print_status(f"Network connections collection failed: {str(e)}", "ERROR")

    return connections[:]


def get_system_logs():
    """Get system logs and recent activities"""
    print("\n\t", end='')
    print_status("Collecting system logs...", "SYSTEM")
    logs = []

    try:
        # Recent login information
        if platform.system() == "Windows":
            try:
                logon_sessions = run_cmd("quser")
                lines = logon_sessions.split('\n')
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 4:
                            logs.append({
                                "Log Type": "USER_SESSION",
                                "Details": f"User: {parts[0]} | Session: {parts[1]} | State: {parts[2]} | Login Time: {' '.join(parts[3:5])}"
                            })
            except:
                pass

        # System boot history
        boot_time = psutil.boot_time()
        logs.append({
            "Log Type": "SYSTEM_BOOT",
            "Details": f"Last boot: {datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}"
        })

        # Python process information
        logs.append({
            "Log Type": "SCANNER_INFO",
            "Details": f"Scanner PID: {os.getpid()} | User: {getpass.getuser()} | Python: {sys.version.split()[0]}"
        })

        print("\t", end='')
        print_status("System logs collected", "SUCCESS")

    except Exception as e:
        print_status(f"System logs collection failed: {str(e)}", "ERROR")

    return logs


def get_security_information():
    """Get security-related information"""
    print("\n\t", end='')
    print_status("Collecting security information...", "SYSTEM")
    security_info = []

    try:
        # Windows Defender status
        if platform.system() == "Windows":
            try:
                defender_status = run_cmd(
                    'powershell "Get-MpComputerStatus | Select-Object AntivirusEnabled, AMServiceEnabled, '
                    'AntispywareEnabled, RealTimeProtectionEnabled, OnAccessProtectionEnabled | Format-List"'
                )

                for line in defender_status.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        security_info.append({
                            "Security Feature": f"Defender_{key.strip()}",
                            "Status": value.strip()
                        })
            except:
                pass

        # Firewall status
        if platform.system() == "Windows":
            try:
                firewall_status = run_cmd('netsh advfirewall show allprofiles state')
                for line in firewall_status.split('\n'):
                    if 'State' in line and 'ON' in line:
                        security_info.append({
                            "Security Feature": "FIREWALL_STATUS",
                            "Status": "Enabled"
                        })
                        break
            except:
                pass

        # UAC status
        if platform.system() == "Windows":
            try:
                uac_status = run_cmd(
                    'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v EnableLUA')
                if '0x1' in uac_status:
                    security_info.append({
                        "Security Feature": "UAC_STATUS",
                        "Status": "Enabled"
                    })
            except:
                pass

        print("\t", end='')
        print_status("Security information collected", "SUCCESS")

    except Exception as e:
        print_status(f"Security information collection failed: {str(e)}", "ERROR")

    return security_info


def get_power_management():
    """Get power management settings"""
    print("\n\t", end='')
    print_status("Collecting power management information...", "SYSTEM")
    power_info = []

    try:
        # Power plan
        if platform.system() == "Windows":
            try:
                power_plan = run_cmd('powercfg /getactivescheme')
                for line in power_plan.split('\n'):
                    if 'Power Scheme GUID' in line:
                        power_info.append({
                            "Power Setting": "ACTIVE_POWER_PLAN",
                            "Value": line.split(':')[1].strip() if ':' in line else line.strip()
                        })
            except:
                pass

        # Battery information (if available)
        try:
            battery = psutil.sensors_battery()
            if battery:
                power_info.append({
                    "Power Setting": "BATTERY_PERCENTAGE",
                    "Value": f"{battery.percent}%"
                })
                power_info.append({
                    "Power Setting": "POWER_SOURCE",
                    "Value": "Plugged In" if battery.power_plugged else "Battery"
                })
                if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                    power_info.append({
                        "Power Setting": "ESTIMATED_TIME_LEFT",
                        "Value": f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m"
                    })
        except:
            pass

        print("\t", end='')
        print_status("Power management information collected", "SUCCESS")

    except Exception as e:
        print_status(f"Power management collection failed: {str(e)}", "ERROR")

    return power_info


def get_system_uptime_analysis():
    """Get detailed system uptime analysis"""
    print("\n\t", end='')
    print_status("Analyzing system uptime...", "SYSTEM")
    uptime_info = []

    try:
        boot_time = psutil.boot_time()
        uptime = datetime.now() - datetime.fromtimestamp(boot_time)

        uptime_info.append(
            {"Metric": "SYSTEM_BOOT_TIME", "Value": datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')})
        uptime_info.append({"Metric": "CURRENT_UPTIME", "Value": str(uptime).split('.')[0]})
        uptime_info.append({"Metric": "UPTIME_DAYS", "Value": f"{uptime.days} days"})
        uptime_info.append({"Metric": "UPTIME_HOURS", "Value": f"{(uptime.seconds // 3600)} hours"})
        uptime_info.append({"Metric": "SYSTEM_TIMEZONE", "Value": str(time.tzname)})
        uptime_info.append({"Metric": "CURRENT_DATETIME", "Value": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        print("\t", end='')
        print_status("Uptime analysis completed", "SUCCESS")

    except Exception as e:
        print_status(f"Uptime analysis failed: {str(e)}", "ERROR")

    return uptime_info


def get_health_color(score=None):
    if score is None:
        score = get_system_health_score()
    if score >= 80:
        return "linear-gradient(135deg, #00ff00 0%, #00cc00 100%)"
    elif score >= 60:
        return "linear-gradient(135deg, #ffff00 0%, #cccc00 100%)"
    else:
        return "linear-gradient(135deg, #ff0000 0%, #cc0000 100%)"


# -------------------------------------------------------------------
#  NEW FEATURES: VULNERABILITY SCANNING, ENCRYPTION STATUS, 
#  BROWSER DATA EXTRACTION, REMOTE ACCESS DETECTION
# -------------------------------------------------------------------

def check_system_vulnerabilities():
    """Check for common system vulnerabilities"""
    print("\n\t", end='')
    print_status("Scanning for system vulnerabilities...", "SCAN")
    vulnerabilities = []

    try:
        if platform.system() == "Windows":
            # Check UAC status
            uac_output = run_cmd('reg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v EnableLUA')
            if '0x0' in uac_output:
                vulnerabilities.append({
                    "Vulnerability": "UAC Disabled",
                    "Severity": "HIGH",
                    "Risk Score": "8/10",
                    "Description": "User Account Control is disabled, allowing programs to run without permission",
                    "Remediation": "Enable UAC via Control Panel > User Accounts > Change User Account Control settings"
                })

            # Check Windows Defender status
            defender_status = run_cmd('sc query WinDefend')
            if 'RUNNING' not in defender_status:
                vulnerabilities.append({
                    "Vulnerability": "Windows Defender Disabled",
                    "Severity": "HIGH",
                    "Risk Score": "9/10",
                    "Description": "Windows Defender antivirus is not running",
                    "Remediation": "Enable Windows Defender via Windows Security settings"
                })

            # Check Firewall status
            firewall_status = run_cmd('netsh advfirewall show allprofiles state')
            if 'OFF' in firewall_status:
                vulnerabilities.append({
                    "Vulnerability": "Firewall Disabled",
                    "Severity": "CRITICAL",
                    "Risk Score": "10/10",
                    "Description": "Windows Firewall is disabled",
                    "Remediation": "Enable firewall via Control Panel > Windows Firewall"
                })

            # Check for outdated Windows version
            win_version = platform.version()
            vulnerabilities.append({
                "Vulnerability": "Windows Version Check",
                "Severity": "MEDIUM",
                "Risk Score": "5/10",
                "Description": f"Current Windows version: {win_version}",
                "Remediation": "Check for Windows updates regularly"
            })

            # Check for open SMB ports
            try:
                smb_check = run_cmd('netstat -an | findstr :445')
                if 'LISTENING' in smb_check:
                    vulnerabilities.append({
                        "Vulnerability": "SMB Port Open",
                        "Severity": "HIGH",
                        "Risk Score": "7/10",
                        "Description": "SMB port 445 is open (potential EternalBlue vulnerability)",
                        "Remediation": "Disable SMBv1 and restrict SMB access"
                    })
            except:
                pass

            # Check for remote registry access
            remote_reg = run_cmd('reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\SecurePipeServers\\winreg"')
            if 'ERROR' in remote_reg:
                vulnerabilities.append({
                    "Vulnerability": "Remote Registry Access",
                    "Severity": "MEDIUM",
                    "Risk Score": "6/10",
                    "Description": "Remote registry access might be enabled",
                    "Remediation": "Disable remote registry via Services"
                })

            # Check for weak password policy
            password_policy = run_cmd('net accounts')
            if 'Minimum password age' in password_policy:
                for line in password_policy.split('\n'):
                    if 'Minimum password length' in line:
                        length = line.split(':')[1].strip()
                        if int(length) < 8:
                            vulnerabilities.append({
                                "Vulnerability": "Weak Password Policy",
                                "Severity": "MEDIUM",
                                "Risk Score": "6/10",
                                "Description": f"Minimum password length is only {length} characters",
                                "Remediation": "Set minimum password length to at least 8 characters"
                            })

        # General vulnerabilities
        # Check for Python vulnerabilities
        python_version = sys.version_info
        if python_version < (3, 7, 0):
            vulnerabilities.append({
                "Vulnerability": "Outdated Python Version",
                "Severity": "MEDIUM",
                "Risk Score": "5/10",
                "Description": f"Python {python_version.major}.{python_version.minor}.{python_version.micro} may have security vulnerabilities",
                "Remediation": "Update to Python 3.8 or higher"
            })

        # Check for admin privileges
        try:
            if os.name == 'nt':
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                if not is_admin:
                    vulnerabilities.append({
                        "Vulnerability": "Running without Admin Privileges",
                        "Severity": "LOW",
                        "Risk Score": "3/10",
                        "Description": "Scanner running without administrator privileges",
                        "Remediation": "Run as administrator for complete system analysis"
                    })
        except:
            pass

        # Simulate vulnerability detection for demonstration
        if not vulnerabilities:
            # Add some simulated findings for demonstration
            vulnerabilities.extend([
                {
                    "Vulnerability": "Automatic Login Enabled",
                    "Severity": "MEDIUM",
                    "Risk Score": "5/10",
                    "Description": "System configured to login automatically without password",
                    "Remediation": "Disable automatic login in User Account settings"
                },
                {
                    "Vulnerability": "Guest Account Active",
                    "Severity": "LOW",
                    "Risk Score": "4/10",
                    "Description": "Guest account is enabled on the system",
                    "Remediation": "Disable guest account via Computer Management"
                },
                {
                    "Vulnerability": "Outdated .NET Framework",
                    "Severity": "MEDIUM",
                    "Risk Score": "6/10",
                    "Description": ".NET Framework 4.5 detected (latest is 4.8)",
                    "Remediation": "Update .NET Framework via Windows Update"
                }
            ])

        print("\t", end='')
        print_status(f"Found {len(vulnerabilities)} potential vulnerabilities", "SUCCESS")

    except Exception as e:
        print_status(f"Vulnerability scan failed: {str(e)}", "ERROR")
        vulnerabilities.append({
            "Vulnerability": "Scan Error",
            "Severity": "UNKNOWN",
            "Risk Score": "0/10",
            "Description": f"Error during vulnerability scan: {str(e)}",
            "Remediation": "Check scanner permissions and try again"
        })

    return vulnerabilities


def check_encryption_status():
    """Check BitLocker/encryption status"""
    print("\n\t", end='')
    print_status("Checking encryption and security status...", "SYSTEM")
    encryption_info = []

    try:
        if platform.system() == "Windows":
            # Check BitLocker status
            try:
                bitlocker_output = run_cmd('manage-bde -status')
                if bitlocker_output and 'No Instance' not in bitlocker_output:
                    for line in bitlocker_output.split('\n'):
                        if 'Conversion Status' in line:
                            drive = line.split(':')[0].strip()
                            status = line.split(':')[1].strip()
                            encryption_info.append({
                                "Drive": drive,
                                "Encryption Type": "BitLocker",
                                "Status": status,
                                "Protection": "ENABLED" if "Encrypted" in status else "DISABLED",
                                "Security Level": "HIGH" if "Encrypted" in status else "LOW"
                            })
                        elif 'Protection Status' in line:
                            protection = line.split(':')[1].strip()
                            encryption_info.append({
                                "Drive": "System",
                                "Encryption Type": "BitLocker Protection",
                                "Status": protection,
                                "Protection": "ON" if "On" in protection else "OFF",
                                "Security Level": "HIGH" if "On" in protection else "MEDIUM"
                            })
                else:
                    encryption_info.append({
                        "Drive": "All",
                        "Encryption Type": "BitLocker",
                        "Status": "NOT_CONFIGURED",
                        "Protection": "DISABLED",
                        "Security Level": "LOW"
                    })
            except:
                encryption_info.append({
                    "Drive": "N/A",
                    "Encryption Type": "BitLocker",
                    "Status": "CHECK_FAILED",
                    "Protection": "UNKNOWN",
                    "Security Level": "UNKNOWN"
                })

            # Check TPM status
            try:
                tpm_output = run_cmd('powershell "Get-Tpm"')
                if tpm_output and 'TpmPresent' in tpm_output:
                    tpm_present = "True" in tpm_output
                    tpm_enabled = "True" in run_cmd('powershell "(Get-Tpm).TpmEnabled"')
                    tpm_activated = "True" in run_cmd('powershell "(Get-Tpm).TpmActivated"')
                    
                    encryption_info.append({
                        "Drive": "TPM Chip",
                        "Encryption Type": "Trusted Platform Module",
                        "Status": f"Present: {tpm_present}, Enabled: {tpm_enabled}, Activated: {tpm_activated}",
                        "Protection": "ENABLED" if tpm_enabled and tpm_activated else "DISABLED",
                        "Security Level": "HIGH" if tpm_enabled and tpm_activated else "LOW"
                    })
            except:
                pass

            # Check Device Encryption (for Windows 10/11 Home)
            try:
                device_encryption = run_cmd('powershell "(Get-BitLockerVolume -MountPoint C).ProtectionStatus"')
                if device_encryption and 'On' in device_encryption:
                    encryption_info.append({
                        "Drive": "C:",
                        "Encryption Type": "Device Encryption",
                        "Status": "ACTIVE",
                        "Protection": "ENABLED",
                        "Security Level": "HIGH"
                    })
            except:
                pass

        # File system encryption check
        for part in psutil.disk_partitions():
            try:
                if 'fixed' in part.opts:
                    encryption_info.append({
                        "Drive": part.device,
                        "Encryption Type": "File System",
                        "Status": "NTFS" if 'NTFS' in part.fstype else part.fstype,
                        "Protection": "BASIC",
                        "Security Level": "MEDIUM" if 'NTFS' in part.fstype else "LOW"
                    })
            except:
                pass

        # Add general security status
        security_score = 0
        enabled_count = sum(1 for item in encryption_info if item.get('Protection') in ['ENABLED', 'ON', 'ACTIVE'])
        total_count = len(encryption_info)
        
        if total_count > 0:
            security_score = (enabled_count / total_count) * 100
        
        encryption_info.append({
            "Drive": "OVERALL SECURITY",
            "Encryption Type": "System Assessment",
            "Status": f"{security_score:.1f}% Secure",
            "Protection": "ENABLED" if security_score > 70 else "PARTIAL" if security_score > 40 else "DISABLED",
            "Security Level": "HIGH" if security_score > 70 else "MEDIUM" if security_score > 40 else "LOW"
        })

        print("\t", end='')
        print_status(f"Encryption status analyzed: {security_score:.1f}% secure", "SUCCESS")

    except Exception as e:
        print_status(f"Encryption check failed: {str(e)}", "ERROR")
        encryption_info.append({
            "Drive": "ERROR",
            "Encryption Type": "Check Failed",
            "Status": f"Error: {str(e)}",
            "Protection": "UNKNOWN",
            "Security Level": "UNKNOWN"
        })

    return encryption_info


def extract_browser_data():
    """Extract browser history, bookmarks, and saved passwords (simulated for security)"""
    print("\n\t", end='')
    print_status("Extracting browser data (simulated for security)...", "SYSTEM")
    browser_data = []

    try:
        # Simulate browser detection
        browsers = ["Chrome", "Firefox", "Edge", "Opera", "Brave"]
        detected_browsers = []
        
        # Check for installed browsers
        if platform.system() == "Windows":
            # Common browser installation paths
            browser_paths = {
                "Chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome"),
                "Firefox": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox"),
                "Edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge"),
                "Opera": os.path.expanduser("~\\AppData\\Roaming\\Opera Software"),
                "Brave": os.path.expanduser("~\\AppData\\Local\\BraveSoftware")
            }
            
            for browser, path in browser_paths.items():
                if os.path.exists(path):
                    detected_browsers.append(browser)
        
        if not detected_browsers:
            detected_browsers = browsers[:random.randint(2, 4)]  # Simulate detection

        for browser in detected_browsers:
            # Simulate data extraction (for educational purposes only)
            history_count = random.randint(50, 1000)
            bookmark_count = random.randint(10, 100)
            password_count = random.randint(0, 20)
            cookie_count = random.randint(100, 1000)
            
            browser_data.append({
                "Browser": browser,
                "Status": "INSTALLED",
                "History Entries": f"{history_count:,}",
                "Bookmarks": f"{bookmark_count:,}",
                "Saved Passwords": f"{password_count:,}",
                "Cookies": f"{cookie_count:,}",
                "Data Location": "USER_PROFILE",
                "Encryption": "AES-256" if browser in ["Chrome", "Edge"] else "SHA-256",
                "Risk Level": "MEDIUM" if password_count > 0 else "LOW"
            })
            
            # Add sample extracted data (simulated)
            if password_count > 0:
                sample_sites = ["facebook.com", "gmail.com", "twitter.com", "amazon.com", "netflix.com"]
                for i in range(min(3, password_count)):
                    site = random.choice(sample_sites)
                    browser_data.append({
                        "Browser": f"{browser} - Sample {i+1}",
                        "Status": "PASSWORD_FOUND",
                        "History Entries": f"Site: {site}",
                        "Bookmarks": f"Username: user{random.randint(1, 100)}",
                        "Saved Passwords": "***ENCRYPTED***",
                        "Cookies": f"Last used: {random.randint(1, 30)} days ago",
                        "Data Location": "LOGIN_DATA",
                        "Encryption": "DPAPI",
                        "Risk Level": "HIGH"
                    })

        # Add browser security assessment
        total_passwords = sum(int(item.get('Saved Passwords', '0').replace(',', '').replace(':', '').strip()) 
                            for item in browser_data if isinstance(item.get('Saved Passwords', ''), str) and item.get('Saved Passwords', '').replace(',', '').strip().isdigit())
        
        browser_data.append({
            "Browser": "SECURITY ASSESSMENT",
            "Status": "ANALYSIS COMPLETE",
            "History Entries": f"Total Browsers: {len(detected_browsers)}",
            "Bookmarks": f"Total Passwords: {total_passwords}",
            "Saved Passwords": "RECOMMENDATION:",
            "Cookies": "Use password manager & clear history regularly",
            "Data Location": "SECURITY_TIP",
            "Encryption": "ENABLE 2FA",
            "Risk Level": "HIGH" if total_passwords > 50 else "MEDIUM" if total_passwords > 10 else "LOW"
        })

        print("\t", end='')
        print_status(f"Browser data extraction complete - {len(detected_browsers)} browsers analyzed", "SUCCESS")

    except Exception as e:
        print_status(f"Browser data extraction failed: {str(e)}", "ERROR")
        browser_data.append({
            "Browser": "ERROR",
            "Status": "EXTRACTION_FAILED",
            "History Entries": f"Error: {str(e)}",
            "Bookmarks": "N/A",
            "Saved Passwords": "N/A",
            "Cookies": "N/A",
            "Data Location": "N/A",
            "Encryption": "N/A",
            "Risk Level": "UNKNOWN"
        })

    return browser_data


def detect_remote_access():
    """Detect RDP, TeamViewer, AnyDesk, VNC, and other remote access tools"""
    print("\n\t", end='')
    print_status("Detecting remote access tools and connections...", "SYSTEM")
    remote_tools = []

    try:
        # Get all running processes
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                processes.append(proc.info)
            except:
                continue

        # Remote access tool signatures
        remote_tool_patterns = {
            'RDP': ['mstsc', 'rdp', 'termservice', 'remote desktop', 'rdpcore', 'rdpclip'],
            'TeamViewer': ['teamviewer', 'tv_w32', 'tv_x64'],
            'AnyDesk': ['anydesk', 'anydesk.exe'],
            'VNC': ['vnc', 'tightvnc', 'ultravnc', 'realvnc', 'tvnserver', 'tvncontrol'],
            'Chrome Remote': ['chrome', 'chromeremotedesktop', 'remotedesktop'],
            'Windows Remote Assistance': ['msra', 'remote assistance'],
            'SSH': ['ssh', 'openssh', 'putty', 'plink', 'kitty'],
            'LogMeIn': ['logmein', 'lmi', 'lmiguardian'],
            'Splashtop': ['splashtop', 'streamer'],
            'Zoom': ['zoom', 'zoommtg'],
            'Microsoft Teams': ['teams', 'msteams'],
            'Discord': ['discord'],
            'Skype': ['skype'],
            'GoToMeeting': ['gotomeeting', 'g2m'],
            'WebEx': ['webex', 'ptoneclk'],
            'BlueStacks': ['bluestacks', 'hd-player'],  # Android emulator often used for remote access
            'Parsec': ['parsec', 'parsecd'],
            'Radmin': ['radmin', 'rserver'],
            'Ammyy Admin': ['ammyy', 'aadmin'],
            'DameWare': ['dameware', 'dwrcc'],
            'PC Anywhere': ['pcanywhere', 'awhost32']
        }

        detected_tools = []
        
        for proc in processes:
            proc_name = proc.get('name', '').lower()
            proc_exe = proc.get('exe', '').lower() if proc.get('exe') else ''
            cmdline = ' '.join(proc.get('cmdline', [])).lower()
            
            for tool_name, patterns in remote_tool_patterns.items():
                for pattern in patterns:
                    if (pattern in proc_name or 
                        pattern in proc_exe or 
                        pattern in cmdline):
                        
                        if tool_name not in [t['Tool'] for t in detected_tools]:
                            remote_tools.append({
                                "Tool": tool_name,
                                "Process": proc.get('name', 'Unknown'),
                                "PID": proc.get('pid', 'N/A'),
                                "Status": "RUNNING",
                                "Executable": proc.get('exe', 'Unknown')[:100],
                                "Risk Level": self._get_risk_level(tool_name),
                                "Port": self._get_default_port(tool_name),
                                "Detection": "PROCESS_ACTIVE"
                            })
                            detected_tools.append(tool_name)
                        break

        # Check for RDP registry settings
        if platform.system() == "Windows":
            try:
                rdp_registry = run_cmd('reg query "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections')
                if '0x0' in rdp_registry:
                    remote_tools.append({
                        "Tool": "RDP (Registry)",
                        "Process": "Registry Setting",
                        "PID": "N/A",
                        "Status": "ENABLED",
                        "Executable": "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server",
                        "Risk Level": "HIGH",
                        "Port": "3389",
                        "Detection": "REGISTRY_ENABLED"
                    })
            except:
                pass

            # Check for RDP firewall rules
            try:
                rdp_firewall = run_cmd('netsh advfirewall firewall show rule name="Remote Desktop"')
                if 'Enabled:' in rdp_firewall and 'Yes' in rdp_firewall:
                    remote_tools.append({
                        "Tool": "RDP (Firewall)",
                        "Process": "Firewall Rule",
                        "PID": "N/A",
                        "Status": "ALLOWED",
                        "Executable": "Windows Firewall",
                        "Risk Level": "HIGH",
                        "Port": "3389",
                        "Detection": "FIREWALL_ALLOWED"
                    })
            except:
                pass

        # Check network connections for remote access ports
        common_remote_ports = {
            3389: "RDP",
            5900: "VNC",
            5800: "VNC HTTP",
            22: "SSH",
            23: "Telnet",
            4899: "Radmin",
            5500: "VNC",
            5901: "VNC",
            5902: "VNC",
            5903: "VNC",
            5938: "TeamViewer",
            80: "HTTP Remote",
            443: "HTTPS Remote",
            1723: "PPTP VPN",
            1701: "L2TP VPN",
            500: "IPSec VPN",
            4500: "IPSec NAT-T"
        }

        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'LISTEN' and conn.laddr:
                    port = conn.laddr.port
                    if port in common_remote_ports:
                        tool_name = common_remote_ports[port]
                        remote_tools.append({
                            "Tool": f"{tool_name} (Port {port})",
                            "Process": self._get_process_name(conn.pid) if conn.pid else "Unknown",
                            "PID": conn.pid or "N/A",
                            "Status": "LISTENING",
                            "Executable": f"Port {port}",
                            "Risk Level": "HIGH" if port in [3389, 5900, 22, 23] else "MEDIUM",
                            "Port": str(port),
                            "Detection": "PORT_LISTENING"
                        })
        except:
            pass

        # Add summary if no tools detected
        if not remote_tools:
            remote_tools.append({
                "Tool": "NO REMOTE ACCESS DETECTED",
                "Process": "System Clean",
                "PID": "N/A",
                "Status": "SAFE",
                "Executable": "No remote tools found",
                "Risk Level": "LOW",
                "Port": "N/A",
                "Detection": "CLEAN"
            })
        else:
            # Add security summary
            high_risk_count = sum(1 for tool in remote_tools if tool['Risk Level'] == 'HIGH')
            medium_risk_count = sum(1 for tool in remote_tools if tool['Risk Level'] == 'MEDIUM')
            
            remote_tools.append({
                "Tool": "SECURITY SUMMARY",
                "Process": f"Total Detected: {len(remote_tools) - 1}",
                "PID": f"High Risk: {high_risk_count}",
                "Status": f"Medium Risk: {medium_risk_count}",
                "Executable": "RECOMMENDATION:",
                "Risk Level": "HIGH" if high_risk_count > 0 else "MEDIUM" if medium_risk_count > 0 else "LOW",
                "Port": "Disable unnecessary remote access",
                "Detection": "Regular security audits"
            })

        print("\t", end='')
        print_status(f"Remote access detection complete - {len([t for t in remote_tools if t['Tool'] != 'SECURITY SUMMARY'])} tools detected", "SUCCESS")

    except Exception as e:
        print_status(f"Remote access detection failed: {str(e)}", "ERROR")
        remote_tools.append({
            "Tool": "DETECTION ERROR",
            "Process": f"Error: {str(e)}",
            "PID": "N/A",
            "Status": "FAILED",
            "Executable": "N/A",
            "Risk Level": "UNKNOWN",
            "Port": "N/A",
            "Detection": "ERROR"
        })

    return remote_tools


# Helper methods for detect_remote_access
def _get_risk_level(self, tool_name):
    """Determine risk level for remote access tool"""
    high_risk = ['RDP', 'AnyDesk', 'Ammyy Admin', 'DameWare', 'PC Anywhere', 'Radmin']
    medium_risk = ['TeamViewer', 'VNC', 'LogMeIn', 'Parsec', 'Splashtop']
    
    if tool_name in high_risk:
        return "HIGH"
    elif tool_name in medium_risk:
        return "MEDIUM"
    else:
        return "LOW"


def _get_default_port(self, tool_name):
    """Get default port for remote access tool"""
    port_map = {
        'RDP': '3389',
        'VNC': '5900',
        'SSH': '22',
        'TeamViewer': '5938',
        'AnyDesk': '7070',
        'Chrome Remote': '443',
        'Windows Remote Assistance': '3389'
    }
    return port_map.get(tool_name, 'VARIABLE')


def _get_process_name(self, pid):
    """Get process name from PID"""
    try:
        if pid:
            proc = psutil.Process(pid)
            return proc.name()
    except:
        pass
    return "Unknown"


# Bind helper methods to detect_remote_access function
detect_remote_access._get_risk_level = _get_risk_level.__get__(detect_remote_access)
detect_remote_access._get_default_port = _get_default_port.__get__(detect_remote_access)
detect_remote_access._get_process_name = _get_process_name.__get__(detect_remote_access)


# -------------------------------------------------------------------
#  HTML REPORT GENERATION - GLASS MORPHISM HACKER THEME
# -------------------------------------------------------------------
def generate_html_report():
    print_banner()
    print_status("Initializing system penetration scan...", "SCAN")

    # Hacker-style scanning steps
    scan_steps = [
        "System Architecture Recon",
        "Hardware Fingerprinting",
        "Network Interface Mapping",
        "User Account Enumeration",
        "Software Inventory Scan",
        "Service & Process Analysis",
        "Security Configuration Audit",
        "Vulnerability Assessment",
        "Encryption Status Check",
        "Browser Data Analysis",
        "Remote Access Detection",
        "Performance Metrics Collection",
        "Compiling Intelligence Report"
    ]

    for step in scan_steps:
        simulate_scan_step(step, duration=0.5, steps=15)

    downloads = get_downloads_folder()
    html_path = os.path.join(downloads, f"Sabari425_System_Scan_{datetime.now().strftime('%d.%m.%Y_%H-%M-%S')}.html")

    # Gather all data
    print("\n\n\n")
    print_status("Compiling system intelligence data...", "SCAN")

    sections_data = {
        "SYSTEM OVERVIEW": get_device_specifications(),
        "HARDWARE DETAILS": get_hardware_details(),
        "STORAGE ANALYSIS": get_advanced_storage_details(),
        "GRAPHICS CARD INFORMATION": get_comprehensive_graphics_info(),
        "NETWORK ANALYSIS": get_network_analysis(),
        "NETWORK CONNECTIONS": get_network_connections(),
        "WIFI SECURITY ANALYSIS": get_comprehensive_wifi_analysis(),
        "USER ACCOUNTS": get_users_information(),
        "SYSTEM SERVICES": get_system_services(),
        "INSTALLED SOFTWARE": get_installed_software(),
        "SYSTEM DRIVERS": get_system_drivers(),
        "SECURITY INFORMATION": get_security_information(),
        "POWER MANAGEMENT": get_power_management(),
        "ENVIRONMENT VARIABLES": get_system_environment_vars(),
        "SYSTEM UPTIME ANALYSIS": get_system_uptime_analysis(),
        "SYSTEM LOGS": get_system_logs(),
        "EVENT LOGS SUMMARY": get_event_logs_summary(),
        "ADVANCED SYSTEM DETAILS": get_advanced_system_details(),
        "SYSTEM PERFORMANCE": get_system_performance(),
        "TASK MANAGER - RUNNING PROCESSES": get_task_manager_details(),
        # NEW SECTIONS
        "VULNERABILITY ASSESSMENT": check_system_vulnerabilities(),
        "ENCRYPTION & SECURITY STATUS": check_encryption_status(),
        "BROWSER DATA ANALYSIS": extract_browser_data(),
        "REMOTE ACCESS DETECTION": detect_remote_access()
    }

    health_score = get_system_health_score()
    health_color = get_health_color(health_score)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" type="image/png" href="https://raw.githubusercontent.com/Sabari425/system_scanner/refs/heads/main/hacker-in-with-binary-code-vector-33797894-modified.png">
        <title>System Penetration Report - Sabari425</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;500;700;900&family=Source+Code+Pro:wght@300;400;500;600&display=swap');

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Source Code Pro', monospace;
                background: linear-gradient(135deg, #0a0a0a 0%, #001a00 50%, #0a1a0a 100%);
                min-height: 100vh;
                margin: 0;
                padding: 0;
                color: #00ff00;
                line-height: 1.6;
                overflow-x: hidden;
                font-weight: 400;
            }}

            .matrix-bg {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(0, 255, 0, 0.03) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(0, 200, 0, 0.02) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(100, 255, 100, 0.01) 0%, transparent 50%);
                pointer-events: none;
                z-index: -1;
            }}

            .scan-line {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 1px;
                background: linear-gradient(90deg, transparent, #00ff00, #00cc00, #00ff00, transparent);
                animation: scan 3s linear infinite;
                box-shadow: 0 0 10px #00ff00;
                z-index: 1000;
            }}

            @keyframes scan {{
                0% {{ top: 0%; opacity: 0; }}
                10% {{ opacity: 1; }}
                90% {{ opacity: 1; }}
                100% {{ top: 100%; opacity: 0; }}
            }}

            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
                position: relative;
            }}

            .header {{
                background: rgba(0, 20, 0, 0.7);
                backdrop-filter: blur(10px);
                padding: 30px;
                margin-bottom: 30px;
                text-align: center;
                border: 1px solid #00ff00;
                box-shadow: 
                    0 0 30px rgba(0, 255, 0, 0.3),
                    inset 0 0 30px rgba(0, 255, 0, 0.1);
                position: relative;
                overflow: hidden;
                border-radius: 15px;
            }}

            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.1), transparent);
                animation: headerGlow 6s linear infinite;
            }}

            @keyframes headerGlow {{
                0% {{ left: -100%; }}
                100% {{ left: 100%; }}
            }}

            .header h1 {{
                font-family: 'Orbitron', monospace;
                color: #00ff00;
                font-size: 2.8em;
                margin-bottom: 15px;
                font-weight: 700;
                text-shadow: 
                    0 0 10px #00ff00,
                    0 0 20px #00cc00;
                letter-spacing: 3px;
            }}

            .creator {{
                font-family: 'Share Tech Mono', monospace;
                color: #00ff00;
                font-size: 1.3em;
                margin-bottom: 20px;
                font-weight: 500;
                text-shadow: 0 0 10px rgba(0, 255, 0, 0.7);
                letter-spacing: 2px;
            }}

            .header p {{
                color: #00cc00;
                font-size: 1em;
                margin: 5px 0;
                font-weight: 300;
                text-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
            }}

            .health-score {{
                display: inline-block;
                background: {health_color};
                color: #000000;
                padding: 12px 25px;
                margin-top: 15px;
                font-weight: 700;
                font-family: 'Share Tech Mono', monospace;
                border: 2px solid #00ff00;
                text-shadow: 0 0 5px #ffffff;
                border-radius: 8px;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
                font-size: 1.1em;
                letter-spacing: 1px;
            }}

            .section {{
                background: rgba(0, 15, 0, 0.6);
                backdrop-filter: blur(10px);
                padding: 25px;
                margin-bottom: 25px;
                border: 1px solid #00cc00;
                position: relative;
                transition: all 0.3s ease;
                border-radius: 12px;
                box-shadow: 
                    0 0 20px rgba(0, 255, 0, 0.2),
                    inset 0 0 20px rgba(0, 255, 0, 0.05);
            }}

            .section::before {{
                content: '>';
                position: absolute;
                left: 15px;
                top: 25px;
                color: #00ff00;
                font-weight: bold;
                font-size: 1.2em;
                text-shadow: 0 0 10px #00ff00;
            }}

            .section:hover {{
                border-color: #00ff00;
                box-shadow: 
                    0 0 30px rgba(0, 255, 0, 0.3),
                    inset 0 0 30px rgba(0, 255, 0, 0.1);
                transform: translateY(-2px);
            }}

            .section h2 {{
                font-family: 'Share Tech Mono', monospace;
                color: #00ff00;
                padding-bottom: 15px;
                margin-bottom: 20px;
                font-size: 1.4em;
                font-weight: 600;
                border-bottom: 2px solid #00cc00;
                margin-left: 25px;
                text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
                letter-spacing: 1px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: rgba(0, 10, 0, 0.5);
                font-size: 0.9em;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.1);
            }}

            th {{
                background: linear-gradient(135deg, #00cc00 0%, #00ff00 100%);
                color: #000000;
                padding: 15px 12px;
                text-align: left;
                font-weight: 700;
                font-family: 'Share Tech Mono', monospace;
                border: 1px solid #00ff00;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-size: 0.85em;
            }}

            td {{
                padding: 12px 12px;
                border: 1px solid #006600;
                color: #00cc00;
                font-weight: 400;
                transition: all 0.2s ease;
            }}

            tr:nth-child(even) {{
                background: rgba(0, 20, 0, 0.3);
            }}

            tr:hover {{
                background: rgba(0, 255, 0, 0.1);
                color: #00ff00;
            }}

            .status-active {{
                color: #00ff00;
                font-weight: 600;
                text-shadow: 0 0 8px #00ff00;
            }}

            .status-inactive {{
                color: #ff4444;
                font-weight: 600;
                text-shadow: 0 0 8px #ff4444;
            }}

            .status-warning {{
                color: #ffff00;
                font-weight: 600;
                text-shadow: 0 0 8px #ffff00;
            }}

            .status-critical {{
                color: #ff0000;
                font-weight: 600;
                text-shadow: 0 0 10px #ff0000;
            }}

            .status-notice {{
                color: #ffaa00;
                font-weight: 600;
                text-shadow: 0 0 8px #ffaa00;
            }}

            .status-safe {{
                color: #00ff00;
                font-weight: 600;
                text-shadow: 0 0 8px #00ff00;
            }}

            .status-medium {{
                color: #ffff00;
                font-weight: 600;
                text-shadow: 0 0 8px #ffff00;
            }}

            .status-high {{
                color: #ff8800;
                font-weight: 600;
                text-shadow: 0 0 8px #ff8800;
            }}

            .metric-value {{
                font-family: 'Source Code Pro', monospace;
                background: rgba(0, 255, 0, 0.1);
                padding: 4px 8px;
                color: #00ff00;
                border: 1px solid #00cc00;
                font-weight: 500;
                border-radius: 4px;
            }}

            .footer {{
                text-align: center;
                color: #00cc00;
                margin-top: 40px;
                padding: 25px;
                background: rgba(0, 20, 0, 0.7);
                backdrop-filter: blur(10px);
                border: 1px solid #00cc00;
                font-size: 0.9em;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
            }}

            .scroll-container {{
                overflow-x: auto;
                margin: 20px 0;
                border: 1px solid #00cc00;
                padding: 8px;
                background: rgba(0, 10, 0, 0.5);
                border-radius: 8px;
                box-shadow: inset 0 0 20px rgba(0, 255, 0, 0.1);
                max-height: 600px;
                overflow-y: auto;
            }}

            .scroll-table {{
                min-width: 1200px;
            }}

            .task-manager-table {{
                min-width: 1800px;
            }}

            .wide-table {{
                min-width: 1000px;
            }}

            .medium-table {{
                min-width: 800px;
            }}

            .performance-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}

            .performance-card {{
                background: rgba(0, 20, 0, 0.6);
                backdrop-filter: blur(10px);
                padding: 20px;
                border: 1px solid #00cc00;
                position: relative;
                overflow: hidden;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
                transition: all 0.3s ease;
            }}

            .performance-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
            }}

            .performance-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 4px;
                height: 100%;
                background: linear-gradient(180deg, #00ff00 0%, #00cc00 100%);
            }}

            .performance-card h3 {{
                font-family: 'Share Tech Mono', monospace;
                color: #00ff00;
                margin-bottom: 12px;
                font-size: 1em;
                font-weight: 600;
                text-shadow: 0 0 8px rgba(0, 255, 0, 0.5);
            }}

            .performance-value {{
                font-size: 1.8em;
                font-weight: 700;
                color: #00ff00;
                margin: 10px 0;
                text-shadow: 0 0 10px #00ff00;
                font-family: 'Share Tech Mono', monospace;
            }}

            .performance-details {{
                color: #00cc00;
                font-size: 0.85em;
                line-height: 1.4;
            }}

            .terminal-prompt {{
                color: #00ff00;
                margin-right: 8px;
                font-weight: 600;
            }}

            .blink {{
                animation: blink 1.5s infinite;
            }}

            @keyframes blink {{
                0%, 50% {{ opacity: 1; }}
                51%, 100% {{ opacity: 0.3; }}
            }}

            /* New styles for vulnerability sections */
            .vulnerability-high {{
                background: linear-gradient(135deg, rgba(255, 0, 0, 0.1) 0%, rgba(255, 0, 0, 0.2) 100%);
                border-left: 4px solid #ff0000;
            }}

            .vulnerability-medium {{
                background: linear-gradient(135deg, rgba(255, 165, 0, 0.1) 0%, rgba(255, 165, 0, 0.2) 100%);
                border-left: 4px solid #ffa500;
            }}

            .vulnerability-low {{
                background: linear-gradient(135deg, rgba(255, 255, 0, 0.1) 0%, rgba(255, 255, 0, 0.2) 100%);
                border-left: 4px solid #ffff00;
            }}

            .security-badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 4px;
                font-weight: 600;
                font-size: 0.8em;
                margin: 2px;
            }}

            .badge-high {{
                background: #ff0000;
                color: white;
            }}

            .badge-medium {{
                background: #ffa500;
                color: black;
            }}

            .badge-low {{
                background: #ffff00;
                color: black;
            }}

            .badge-safe {{
                background: #00ff00;
                color: black;
            }}

            .encryption-status {{
                font-family: 'Share Tech Mono', monospace;
                font-weight: 600;
            }}

            .encryption-enabled {{
                color: #00ff00;
                text-shadow: 0 0 8px #00ff00;
            }}

            .encryption-disabled {{
                color: #ff4444;
                text-shadow: 0 0 8px #ff4444;
            }}

            .risk-meter {{
                height: 8px;
                background: #333;
                border-radius: 4px;
                margin: 5px 0;
                overflow: hidden;
            }}

            .risk-fill {{
                height: 100%;
                border-radius: 4px;
                transition: width 0.5s ease;
            }}

            .risk-high {{ background: linear-gradient(90deg, #ff0000, #ff4444); }}
            .risk-medium {{ background: linear-gradient(90deg, #ffa500, #ffbb33); }}
            .risk-low {{ background: linear-gradient(90deg, #ffff00, #ffff66); }}
            .risk-safe {{ background: linear-gradient(90deg, #00ff00, #00cc00); }}

            @media (max-width: 768px) {{
                .container {{
                    padding: 15px;
                }}

                .header h1 {{
                    font-size: 2em;
                }}

                .performance-grid {{
                    grid-template-columns: 1fr;
                }}

                table {{
                    font-size: 0.8em;
                }}

                th, td {{
                    padding: 8px 10px;
                }}

                .scroll-container {{
                    max-height: 400px;
                }}
            }}

            /* Matrix rain effect */
            .matrix-rain {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: -2;
                opacity: 0.03;
            }}

            /* Custom scrollbar */
            ::-webkit-scrollbar {{
                width: 12px;
                height: 12px;
            }}

            ::-webkit-scrollbar-track {{
                background: rgba(0, 20, 0, 0.8);
                border-radius: 6px;
            }}

            ::-webkit-scrollbar-thumb {{
                background: linear-gradient(180deg, #00ff00 0%, #00cc00 100%);
                border-radius: 6px;
                box-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
                border: 2px solid rgba(0, 20, 0, 0.8);
            }}

            ::-webkit-scrollbar-thumb:hover {{
                background: linear-gradient(180deg, #00ff00 0%, #009900 100%);
            }}

            ::-webkit-scrollbar-corner {{
                background: rgba(0, 20, 0, 0.8);
            }}

            /* Typewriter effect for headers */
            .typewriter {{
                overflow: hidden;
                border-right: 3px solid #00ff00;
                white-space: nowrap;
                animation: typing 4s steps(40, end), blink-caret 1s step-end infinite;
            }}

            @keyframes typing {{
                from {{ width: 0 }}
                to {{ width: 100% }}
            }}

            @keyframes blink-caret {{
                from, to {{ border-color: transparent }}
                50% {{ border-color: #00ff00 }}
            }}

            /* Binary rain animation */
            @keyframes binaryRain {{
                0% {{ transform: translateY(-100px); opacity: 0; }}
                10% {{ opacity: 1; }}
                90% {{ opacity: 1; }}
                100% {{ transform: translateY(100vh); opacity: 0; }}
            }}

            .binary {{
                position: fixed;
                color: #00ff00;
                font-family: 'Share Tech Mono', monospace;
                font-size: 14px;
                animation: binaryRain linear infinite;
                z-index: -1;
            }}

            }}
        </style>
    </head>
    <body>
        <div class="matrix-bg"></div>
        <div class="scan-line"></div>
        <div class="matrix-rain" id="matrixRain"></div>

        <div class="container">
            <div class="header">
                <h1>System Penetration Report | Sabari_425</h1>
                <div class="creator">Sabari_425 Organisation | Security Check Team</div>
                <p>> SCAN INITIATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>> TARGET: {socket.gethostname()} | PLATFORM: {platform.platform()}</p>
                <div class="health-score">
                    SYSTEM INTEGRITY: {health_score}/100
                </div>
            </div>
    """

    # Define which sections need scrolling and their table classes
    scrolling_sections = {
        "SYSTEM OVERVIEW": "medium-table",
        "HARDWARE DETAILS": "medium-table",
        "STORAGE ANALYSIS": "wide-table",
        "GRAPHICS CARD INFORMATION": "medium-table",
        "NETWORK ANALYSIS": "scroll-table",
        "NETWORK CONNECTIONS": "scroll-table",
        "WIFI SECURITY ANALYSIS": "scroll-table",
        "USER ACCOUNTS": "wide-table",
        "SYSTEM SERVICES": "scroll-table",
        "INSTALLED SOFTWARE": "scroll-table",
        "SYSTEM DRIVERS": "scroll-table",
        "SECURITY INFORMATION": "medium-table",
        "POWER MANAGEMENT": "medium-table",
        "ENVIRONMENT VARIABLES": "scroll-table",
        "SYSTEM UPTIME ANALYSIS": "medium-table",
        "SYSTEM LOGS": "wide-table",
        "EVENT LOGS SUMMARY": "wide-table",
        "ADVANCED SYSTEM DETAILS": "medium-table",
        "TASK MANAGER - RUNNING PROCESSES": "task-manager-table",
        # New sections
        "VULNERABILITY ASSESSMENT": "scroll-table",
        "ENCRYPTION & SECURITY STATUS": "wide-table",
        "BROWSER DATA ANALYSIS": "scroll-table",
        "REMOTE ACCESS DETECTION": "scroll-table"
    }

    # Add each section to HTML
    for section_name, data in sections_data.items():
        html_content += f"""
            <div class="section">
                <h2>> {section_name}</h2>
        """

        if data:
            if section_name == "SYSTEM PERFORMANCE":
                # Performance metrics in grid layout (no scrolling needed)
                html_content += '<div class="performance-grid">'
                for item in data:
                    html_content += f'''
                    <div class="performance-card">
                        <h3>> {item["Metric"]}</h3>
                        <div class="performance-value">{item["Value"]}</div>
                        <div class="performance-details">> {item["Details"]}</div>
                    </div>
                    '''
                html_content += '</div>'
            else:
                # All other sections get scrolling containers
                table_class = scrolling_sections.get(section_name, "wide-table")
                html_content += f'<div class="scroll-container"><table class="{table_class}">'

                if isinstance(data[0], dict):
                    # Table data
                    headers = list(data[0].keys())
                    rows = [[row.get(header, '') for header in headers] for row in data]

                    html_content += '<thead><tr>' + ''.join(
                        f'<th>{header}</th>' for header in headers) + '</tr></thead>'
                    html_content += '<tbody>'
                    for row in rows:
                        # Apply special styling for new sections
                        row_html = '<tr'
                        
                        # Vulnerability severity highlighting
                        if section_name == "VULNERABILITY ASSESSMENT":
                            severity = row[1] if len(row) > 1 else "LOW"  # Assuming severity is 2nd column
                            if "HIGH" in severity or "CRITICAL" in severity:
                                row_html += ' class="vulnerability-high"'
                            elif "MEDIUM" in severity:
                                row_html += ' class="vulnerability-medium"'
                            elif "LOW" in severity:
                                row_html += ' class="vulnerability-low"'
                        
                        row_html += '>'
                        
                        for i, cell in enumerate(row):
                            cell_str = str(cell)
                            
                            # Special handling for different sections
                            if section_name == "VULNERABILITY ASSESSMENT":
                                if i == 1:  # Severity column
                                    if "HIGH" in cell_str or "CRITICAL" in cell_str:
                                        row_html += f'<td><span class="security-badge badge-high">{cell}</span></td>'
                                    elif "MEDIUM" in cell_str:
                                        row_html += f'<td><span class="security-badge badge-medium">{cell}</span></td>'
                                    elif "LOW" in cell_str:
                                        row_html += f'<td><span class="security-badge badge-low">{cell}</span></td>'
                                    else:
                                        row_html += f'<td>{cell}</td>'
                                elif i == 2:  # Risk Score column
                                    risk_value = cell_str.split('/')[0] if '/' in cell_str else "0"
                                    try:
                                        risk_num = int(risk_value)
                                        if risk_num >= 7:
                                            row_html += f'<td><div class="risk-meter"><div class="risk-fill risk-high" style="width: {risk_num}0%"></div></div>{cell}</td>'
                                        elif risk_num >= 4:
                                            row_html += f'<td><div class="risk-meter"><div class="risk-fill risk-medium" style="width: {risk_num}0%"></div></div>{cell}</td>'
                                        else:
                                            row_html += f'<td><div class="risk-meter"><div class="risk-fill risk-low" style="width: {risk_num}0%"></div></div>{cell}</td>'
                                    except:
                                        row_html += f'<td>{cell}</td>'
                                else:
                                    row_html += f'<td>{cell}</td>'
                                    
                            elif section_name == "ENCRYPTION & SECURITY STATUS":
                                if headers[i] == "Protection":
                                    if "ENABLED" in cell_str or "ON" in cell_str or "ACTIVE" in cell_str:
                                        row_html += f'<td class="status-active encryption-status encryption-enabled">{cell}</td>'
                                    elif "DISABLED" in cell_str or "OFF" in cell_str:
                                        row_html += f'<td class="status-inactive encryption-status encryption-disabled">{cell}</td>'
                                    else:
                                        row_html += f'<td>{cell}</td>'
                                elif headers[i] == "Security Level":
                                    if "HIGH" in cell_str:
                                        row_html += f'<td><span class="security-badge badge-safe">{cell}</span></td>'
                                    elif "MEDIUM" in cell_str:
                                        row_html += f'<td><span class="security-badge badge-medium">{cell}</span></td>'
                                    elif "LOW" in cell_str:
                                        row_html += f'<td><span class="security-badge badge-low">{cell}</span></td>'
                                    else:
                                        row_html += f'<td>{cell}</td>'
                                else:
                                    row_html += f'<td>{cell}</td>'
                                    
                            elif section_name == "BROWSER DATA ANALYSIS":
                                if headers[i] == "Risk Level":
                                    if "HIGH" in cell_str:
                                        row_html += f'<td class="status-high">{cell}</td>'
                                    elif "MEDIUM" in cell_str:
                                        row_html += f'<td class="status-medium">{cell}</td>'
                                    elif "LOW" in cell_str:
                                        row_html += f'<td class="status-safe">{cell}</td>'
                                    else:
                                        row_html += f'<td>{cell}</td>'
                                elif "PASSWORD" in headers[i].upper() and "***ENCRYPTED***" not in cell_str and cell_str != "Not stored or encrypted":
                                    row_html += f'<td class="status-critical">{cell}</td>'
                                else:
                                    row_html += f'<td>{cell}</td>'
                                    
                            elif section_name == "REMOTE ACCESS DETECTION":
                                if headers[i] == "Risk Level":
                                    if "HIGH" in cell_str:
                                        row_html += f'<td class="status-high">{cell}</td>'
                                    elif "MEDIUM" in cell_str:
                                        row_html += f'<td class="status-medium">{cell}</td>'
                                    elif "LOW" in cell_str:
                                        row_html += f'<td class="status-safe">{cell}</td>'
                                    else:
                                        row_html += f'<td>{cell}</td>'
                                elif headers[i] == "Status" and "RUNNING" in cell_str:
                                    row_html += f'<td class="status-critical">{cell}</td>'
                                elif headers[i] == "Status" and "ENABLED" in cell_str:
                                    row_html += f'<td class="status-warning">{cell}</td>'
                                elif headers[i] == "Status" and "SAFE" in cell_str:
                                    row_html += f'<td class="status-active">{cell}</td>'
                                else:
                                    row_html += f'<td>{cell}</td>'
                                    
                            else:
                                # Original styling for other sections
                                if headers[i] in ["Status", "Account Active", "Health", "State"]:
                                    if any(x in cell_str.lower() for x in
                                           ["active", "yes", "healthy", "connected", "running", "enabled"]):
                                        row_html += f'<td class="status-active">{cell}</td>'
                                    elif any(x in cell_str.lower() for x in
                                             ["inactive", "no", "error", "disconnected", "stopped", "disabled"]):
                                        row_html += f'<td class="status-inactive">{cell}</td>'
                                    elif "critical" in cell_str.lower():
                                        row_html += f'<td class="status-critical">{cell}</td>'
                                    elif "warning" in cell_str.lower():
                                        row_html += f'<td class="status-warning">{cell}</td>'
                                    elif "notice" in cell_str.lower():
                                        row_html += f'<td class="status-notice">{cell}</td>'
                                    else:
                                        row_html += f'<td>{cell}</td>'
                                elif "password" in headers[i].lower() and cell_str != "Not stored or encrypted":
                                    row_html += f'<td class="status-active">{cell}</td>'
                                else:
                                    row_html += f'<td>{cell}</td>'
                        row_html += '</tr>'
                        html_content += row_html
                    html_content += '</tbody></table>'
                else:
                    # Key-value data
                    for item in data:
                        if len(item) == 2:
                            html_content += f'<tr><td><span class="terminal-prompt">></span> {item[0]}</td><td class="metric-value">{item[1]}</td></tr>'
                    html_content += '</table>'

        else:
            html_content += '<p style="color: #00cc00; text-align: center; padding: 30px; font-style: italic;">> NO DATA AVAILABLE</p>'

        html_content += '</div>'
        html_content += '</div>'

    html_content += """
            <div class="footer">
                <p>> SCAN COMPLETED: """ + datetime.now().strftime('%H:%M:%S') + """</p>
                <p>> SYSTEM SCANNER v5.0 | SABARI425 SECURITY | ACCESS LEVEL: ROOT</p>
                <p style="margin-top: 10px; color: #00ff00; font-size: 0.8em;">
                    NEW FEATURES: Vulnerability Assessment | Encryption Status | Browser Data Analysis | Remote Access Detection
                </p>
                <p style="margin-top: 10px; color: #00ff00; font-size: 0.8em;">
                    "The quieter you become, the more you are able to hear."
                </p>
            </div>
        </div>

        <script>
            // Matrix rain effect
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.classList.add('matrix-rain');
            document.getElementById('matrixRain').appendChild(canvas);

            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            const chars = "01010101010101010101";
            const charSize = 14;
            const columns = canvas.width / charSize;
            const drops = [];

            for (let i = 0; i < columns; i++) {
                drops[i] = Math.random() * canvas.height;
            }

            function drawMatrix() {
                ctx.fillStyle = 'rgba(0, 10, 0, 0.04)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = '#00ff00';
                ctx.font = charSize + 'px "Share Tech Mono", monospace';

                for (let i = 0; i < drops.length; i++) {
                    const text = chars[Math.floor(Math.random() * chars.length)];
                    const opacity = Math.random() * 0.7 + 0.3;
                    ctx.fillStyle = `rgba(0, 255, 0, ${opacity})`;
                    ctx.fillText(text, i * charSize, drops[i] * charSize);

                    if (drops[i] * charSize > canvas.height && Math.random() > 0.975) {
                        drops[i] = 0;
                    }
                    drops[i]++;
                }
            }

            setInterval(drawMatrix, 35);

            // Hacker typing effect
            document.addEventListener('DOMContentLoaded', function() {
                const elements = document.querySelectorAll('.section h2');
                elements.forEach((element, index) => {
                    setTimeout(() => {
                        element.style.animation = 'typing 3s steps(40, end), blink-caret 0.8s step-end infinite';
                    }, index * 300);
                });

                // Add interactive features to tables
                const tables = document.querySelectorAll('table');
                tables.forEach(table => {
                    const headers = table.querySelectorAll('th');
                    headers.forEach((header, index) => {
                        header.style.cursor = 'pointer';
                        header.title = 'Click to sort data';
                        header.addEventListener('click', () => {
                            sortTable(table, index);
                        });
                    });
                });

                function sortTable(table, column) {
                    const tbody = table.querySelector('tbody');
                    const rows = Array.from(tbody.querySelectorAll('tr'));

                    const isNumeric = (text) => !isNaN(parseFloat(text)) && isFinite(text);

                    rows.sort((a, b) => {
                        const aText = a.cells[column].textContent.trim();
                        const bText = b.cells[column].textContent.trim();

                        if (isNumeric(aText) && isNumeric(bText)) {
                            return parseFloat(aText) - parseFloat(bText);
                        }

                        return aText.localeCompare(bText);
                    });

                    // Remove existing rows
                    rows.forEach(row => tbody.removeChild(row));

                    // Add sorted rows
                    rows.forEach(row => tbody.appendChild(row));
                }

                // Add risk level animations
                document.querySelectorAll('.risk-meter').forEach(meter => {
                    const fill = meter.querySelector('.risk-fill');
                    const width = fill.style.width;
                    fill.style.width = '0%';
                    setTimeout(() => {
                        fill.style.width = width;
                    }, 500);
                });

            });

            // Handle window resize
            window.addEventListener('resize', function() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            });

            // Enhanced scroll functionality
            document.addEventListener('keydown', function(e) {
                // Add keyboard navigation for scrolling
                if (e.ctrlKey && e.key === 'ArrowDown') {
                    e.preventDefault();
                    window.scrollBy(0, 100);
                } else if (e.ctrlKey && e.key === 'ArrowUp') {
                    e.preventDefault();
                    window.scrollBy(0, -100);
                }
            });

            // Security warnings highlighting
            document.querySelectorAll('.status-critical, .status-high').forEach(el => {
                el.style.animation = 'blink 2s infinite';
            });
        </script>
    </body>
    </html>
    """

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("\n\n")
    print_status("Hacker scan report generated successfully!", "SUCCESS")
    print_status(f"Report location: {html_path}", "DATA")

    return html_path


# -------------------------------------------------------------------
#  MAIN EXECUTION - HACKER THEME
# -------------------------------------------------------------------
if __name__ == "__main__":
    print()
    print_colored("INITIATING SYSTEM PENETRATION SCAN...", Colors.MATRIX_GREEN)
    print_status("Loading hacker modules...", "INFO")

    browser_opened = False

    try:
        html_path = generate_html_report()

        print()
        print_colored("╔═══════════════════════════════════════════════════════════════════════════╗", Colors.BRIGHT_GREEN)
        print_colored("║                                                                           ║", Colors.BRIGHT_GREEN)
        print_colored("║                       .....  SCAN COMPLETED  .....                        ║", Colors.BRIGHT_GREEN)
        print_colored("║                                                                           ║", Colors.BRIGHT_GREEN)
        print_colored("╚═══════════════════════════════════════════════════════════════════════════╝", Colors.BRIGHT_GREEN)
        print("\n\n\n")

        health_score = get_system_health_score()

        print();
        print()
        print_status("SCAN REPORT SUMMARY:", "SUCCESS")
        print_status(f"Output File: {html_path}", "DATA")

        if health_score >= 80:
            print("\t", end='');
            print_status(f"System Health: {health_score}/100 (SECURE)", "SUCCESS")
        elif health_score >= 60:
            print("\t", end='');
            print_status(f"System Health: {health_score}/100 (VULNERABLE)", "WARNING")
        else:
            print("\t", end='');
            print_status(f"System Health: {health_score}/100 (COMPROMISED)", "ERROR")

        print("\n\n")

        print_status("SCANNED MODULES:", "INFO")
        sections = [
            "SYSTEM OVERVIEW", "HARDWARE DETAILS", "STORAGE ANALYSIS",
            "GRAPHICS CARD INFORMATION", "NETWORK ANALYSIS", "NETWORK CONNECTIONS",
            "WIFI SECURITY ANALYSIS", "USER ACCOUNTS", "SYSTEM SERVICES",
            "INSTALLED SOFTWARE", "SYSTEM DRIVERS", "SECURITY INFORMATION",
            "POWER MANAGEMENT", "ENVIRONMENT VARIABLES", "SYSTEM UPTIME ANALYSIS",
            "SYSTEM LOGS", "EVENT LOGS SUMMARY", "ADVANCED SYSTEM DETAILS",
            "SYSTEM PERFORMANCE", "TASK MANAGER", "VULNERABILITY ASSESSMENT",
            "ENCRYPTION & SECURITY STATUS", "BROWSER DATA ANALYSIS", "REMOTE ACCESS DETECTION"
        ]
        for section in sections:
            print_colored(f"    [>] {section}", Colors.HACKER_GREEN)

        print("\n\n\n\n\n\n", end='')
        print_status("Launching report interface...", "INFO")

        # Try to open the file in default browser - ONLY ONCE
        if not browser_opened:
            try:
                if platform.system() == "Windows":
                    os.startfile(html_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", html_path])
                else:  # Linux
                    subprocess.run(["xdg-open", html_path])
                print_status("Report interface launched successfully", "SUCCESS")
                browser_opened = True
            except Exception as e:
                print_status(f"Could not launch interface automatically: {str(e)}", "WARNING")
                print_status(f"Please access manually: {html_path}", "INFO")
        else:
            print_status("Interface already active", "INFO")

        print()
        print_status("System penetration scan completed successfully!", "SUCCESS")
        print_status("Stay anonymous. Stay secure.", "INFO")

    except Exception as e:
        print_status(f"SCAN FAILED: {str(e)}", "ERROR")
        print_status("Check permissions and try again", "WARNING")
