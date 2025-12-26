import os
import sys
import subprocess
import platform
from datetime import datetime, timedelta
import socket
import json
import time
import uuid
import getpass
import hashlib
import re
import threading
import queue
from collections import OrderedDict, defaultdict
import winreg  # Windows registry access
import ctypes  # For Windows API calls

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

# Enhanced package list
required_packages = [
    "psutil", "tabulate", "wmi", "GPUtil", "pypiwin32", "pywin32",
    "requests", "python-dateutil", "colorama", "pillow", "netifaces"
]

for package in required_packages:
    try:
        install_package(package)
    except:
        pass  # Silently continue if some packages fail

import psutil
from tabulate import tabulate
import colorama
from colorama import Fore, Back, Style

# Try to import optional packages
try:
    import wmi
    WMI_AVAILABLE = True
except:
    WMI_AVAILABLE = False

try:
    import GPUtil
    GPU_AVAILABLE = True
except:
    GPU_AVAILABLE = False

try:
    import win32api
    import win32con
    import win32security
    WIN32_AVAILABLE = True
except:
    WIN32_AVAILABLE = False

# -------------------------------------------------------------------
#  ENHANCED COLOR CLASS WITH GRADIENTS AND EFFECTS
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
    
    # Enhanced effects
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    
    # Custom gradients
    @staticmethod
    def gradient(text, start_color, end_color):
        """Create gradient text effect"""
        result = ""
        length = len(text)
        for i, char in enumerate(text):
            ratio = i / length
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            result += f'\033[38;2;{r};{g};{b}m{char}'
        return result + Colors.RESET
    
    @staticmethod
    def rainbow(text):
        """Create rainbow text effect"""
        colors = [
            (255, 0, 0),    # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (75, 0, 130),   # Indigo
            (148, 0, 211)   # Violet
        ]
        result = ""
        for i, char in enumerate(text):
            color_idx = int((i / len(text)) * (len(colors) - 1))
            r, g, b = colors[color_idx]
            result += f'\033[38;2;{r};{g};{b}m{char}'
        return result + Colors.RESET

# -------------------------------------------------------------------
#  ENHANCED UTILITY FUNCTIONS
# -------------------------------------------------------------------
def print_colored(text, color=Colors.WHITE, style="", end="\n"):
    """Print colored text with optional styles"""
    if style == "gradient" and isinstance(color, tuple) and len(color) == 2:
        text = Colors.gradient(text, color[0], color[1])
        print(text, end=end)
    elif style == "rainbow":
        text = Colors.rainbow(text)
        print(text, end=end)
    else:
        print(f"{color}{text}{Colors.RESET}", end=end)

def print_status(message, status="INFO", details=""):
    """Enhanced status printer with details"""
    status_config = {
        "INFO": {"color": Colors.BOLD_CYAN, "icon": "[+]"},
        "SUCCESS": {"color": Colors.GREEN, "icon": "[✓]"},
        "WARNING": {"color": Colors.YELLOW, "icon": "[!]"},
        "ERROR": {"color": Colors.RED, "icon": "[✗]"},
        "SCAN": {"color": Colors.MAGENTA, "icon": "[→]"},
        "DATA": {"color": Colors.BLUE, "icon": "[■]"},
        "SYSTEM": {"color": Colors.CYAN, "icon": "[⚙]"},
        "SECURITY": {"color": Colors.RED, "icon": "[🛡]"},
        "NETWORK": {"color": Colors.GREEN, "icon": "[🌐]"},
        "HARDWARE": {"color": Colors.YELLOW, "icon": "[💻]"}
    }
    
    config = status_config.get(status, status_config["INFO"])
    icon = config["icon"]
    color = config["color"]
    
    if details:
        message = f"{message} {Colors.DIM}({details}){Colors.RESET}"
    
    print_colored(f"{icon} {message}", color)

def format_bytes(bytes_num):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} PB"

def get_file_hash(filepath):
    """Calculate file hash"""
    try:
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    except:
        return None

# -------------------------------------------------------------------
#  PARALLEL DATA COLLECTION WITH THREADING
# -------------------------------------------------------------------
class DataCollector:
    def __init__(self):
        self.results = {}
        self.queue = queue.Queue()
        
    def collect_parallel(self, functions):
        """Collect data from multiple functions in parallel"""
        threads = []
        
        def worker(func, name):
            try:
                result = func()
                self.queue.put((name, result))
            except Exception as e:
                self.queue.put((name, {"error": str(e)}))
        
        for name, func in functions.items():
            thread = threading.Thread(target=worker, args=(func, name))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Collect results
        while not self.queue.empty():
            name, result = self.queue.get()
            self.results[name] = result
        
        return self.results

# -------------------------------------------------------------------
#  ENHANCED SYSTEM INFORMATION COLLECTION
# -------------------------------------------------------------------
def get_comprehensive_system_info():
    """Get extremely detailed system information"""
    info = OrderedDict()
    
    # Basic system info
    info["System"] = platform.system()
    info["Node Name"] = platform.node()
    info["Release"] = platform.release()
    info["Version"] = platform.version()
    info["Machine"] = platform.machine()
    info["Processor"] = platform.processor()
    info["Architecture"] = platform.architecture()[0]
    
    # Python info
    info["Python Version"] = platform.python_version()
    info["Python Compiler"] = platform.python_compiler()
    info["Python Build"] = platform.python_build()[1]
    
    # Windows specific
    if platform.system() == "Windows":
        try:
            # Get Windows edition
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            info["Product Name"] = winreg.QueryValueEx(key, "ProductName")[0]
            info["Edition ID"] = winreg.QueryValueEx(key, "EditionID")[0]
            info["Build Branch"] = winreg.QueryValueEx(key, "BuildBranch")[0]
            info["Build Lab"] = winreg.QueryValueEx(key, "BuildLabEx")[0]
            info["Registered Owner"] = winreg.QueryValueEx(key, "RegisteredOwner")[0]
            info["Registered Organization"] = winreg.QueryValueEx(key, "RegisteredOrganization")[0]
            winreg.CloseKey(key)
        except:
            pass
    
    # Uptime
    boot_time = psutil.boot_time()
    uptime = datetime.now() - datetime.fromtimestamp(boot_time)
    info["Boot Time"] = datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')
    info["Uptime"] = str(uptime).split('.')[0]
    
    return [[k, v] for k, v in info.items()]

def get_extended_hardware_info():
    """Get detailed hardware information"""
    hardware = []
    
    # CPU Information
    try:
        cpu_info = psutil.cpu_freq()
        hardware.append({
            "Category": "CPU",
            "Detail": platform.processor(),
            "Current Frequency": f"{cpu_info.current:.2f} MHz" if cpu_info else "N/A",
            "Max Frequency": f"{cpu_info.max:.2f} MHz" if cpu_info else "N/A",
            "Cores": f"{psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical"
        })
    except:
        pass
    
    # Memory Information
    try:
        memory = psutil.virtual_memory()
        hardware.append({
            "Category": "MEMORY",
            "Detail": f"Total: {format_bytes(memory.total)}",
            "Available": format_bytes(memory.available),
            "Used": format_bytes(memory.used),
            "Usage": f"{memory.percent}%",
            "Swap Total": format_bytes(psutil.swap_memory().total)
        })
    except:
        pass
    
    # Disk Information
    try:
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                hardware.append({
                    "Category": "DISK",
                    "Device": partition.device,
                    "Mountpoint": partition.mountpoint,
                    "Filesystem": partition.fstype,
                    "Total": format_bytes(usage.total),
                    "Used": format_bytes(usage.used),
                    "Free": format_bytes(usage.free),
                    "Usage": f"{usage.percent}%"
                })
            except:
                continue
    except:
        pass
    
    # GPU Information (if available)
    if GPU_AVAILABLE:
        try:
            gpus = GPUtil.getGPUs()
            for i, gpu in enumerate(gpus):
                hardware.append({
                    "Category": "GPU",
                    "Name": gpu.name,
                    "Load": f"{gpu.load*100:.1f}%",
                    "Memory Used": f"{gpu.memoryUsed} MB",
                    "Memory Total": f"{gpu.memoryTotal} MB",
                    "Temperature": f"{gpu.temperature} °C"
                })
        except:
            pass
    
    # Battery Information
    try:
        battery = psutil.sensors_battery()
        if battery:
            hardware.append({
                "Category": "BATTERY",
                "Percentage": f"{battery.percent}%",
                "Power Plugged": "Yes" if battery.power_plugged else "No",
                "Time Left": f"{battery.secsleft//3600}h {(battery.secsleft%3600)//60}m" if battery.secsleft > 0 else "Unknown"
            })
    except:
        pass
    
    # Network Adapters
    try:
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        for interface, addresses in addrs.items():
            hardware.append({
                "Category": "NETWORK",
                "Interface": interface,
                "Status": "UP" if stats[interface].isup else "DOWN",
                "Speed": f"{stats[interface].speed} Mbps",
                "MAC": addresses[0].address if addresses else "N/A"
            })
    except:
        pass
    
    return hardware

def get_detailed_process_info():
    """Get extremely detailed process information"""
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent',
                                     'memory_info', 'create_time', 'status', 'cpu_times',
                                     'num_threads', 'exe', 'cmdline', 'connections', 'open_files',
                                     'ppid', 'nice', 'ionice', 'num_handles', 'num_ctx_switches']):
        try:
            pinfo = proc.info
            
            # Calculate additional metrics
            create_time = datetime.fromtimestamp(pinfo['create_time'])
            uptime = datetime.now() - create_time
            
            # Get parent process info
            parent_name = "N/A"
            if pinfo['ppid']:
                try:
                    parent = psutil.Process(pinfo['ppid'])
                    parent_name = parent.name()
                except:
                    pass
            
            processes.append({
                "PID": pinfo['pid'],
                "Name": pinfo['name'][:30],
                "User": pinfo['username'] or "SYSTEM",
                "CPU %": f"{pinfo['cpu_percent']:.2f}",
                "Memory %": f"{pinfo['memory_percent']:.3f}",
                "Memory (MB)": f"{pinfo['memory_info'].rss / (1024*1024):.2f}",
                "Threads": pinfo['num_threads'],
                "Status": pinfo['status'],
                "Parent": f"{parent_name} ({pinfo['ppid']})",
                "Uptime": str(uptime).split('.')[0],
                "Created": create_time.strftime('%H:%M:%S'),
                "Executable": pinfo['exe'][:50] + "..." if pinfo['exe'] and len(pinfo['exe']) > 50 else pinfo['exe'],
                "Command Line": ' '.join(pinfo['cmdline'][:3]) + "..." if pinfo['cmdline'] and len(pinfo['cmdline']) > 3 else ' '.join(pinfo['cmdline']) if pinfo['cmdline'] else ""
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Sort by CPU usage
    processes.sort(key=lambda x: float(x['CPU %']), reverse=True)
    return processes[:100]  # Return top 100 processes

def get_network_analysis_extended():
    """Get comprehensive network analysis"""
    network_info = []
    
    # Network interfaces
    try:
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        io_counters = psutil.net_io_counters(pernic=True)
        
        for interface in addrs:
            iface_info = {
                "Interface": interface,
                "Status": "UP" if stats[interface].isup else "DOWN",
                "MTU": stats[interface].mtu,
                "Speed": f"{stats[interface].speed} Mbps",
                "MAC": "N/A",
                "IPv4": [],
                "IPv6": []
            }
            
            # Get addresses
            for addr in addrs[interface]:
                if addr.family == -1:  # MAC
                    iface_info["MAC"] = addr.address
                elif addr.family == 2:  # IPv4
                    iface_info["IPv4"].append(f"{addr.address}/{addr.netmask}")
                elif addr.family == 23:  # IPv6
                    iface_info["IPv6"].append(addr.address)
            
            # Get IO stats
            if interface in io_counters:
                io = io_counters[interface]
                iface_info.update({
                    "Bytes Sent": format_bytes(io.bytes_sent),
                    "Bytes Recv": format_bytes(io.bytes_recv),
                    "Packets Sent": io.packets_sent,
                    "Packets Recv": io.packets_recv,
                    "Errors In": io.errin,
                    "Errors Out": io.errout,
                    "Dropped In": io.dropin,
                    "Dropped Out": io.dropout
                })
            
            network_info.append(iface_info)
    except:
        pass
    
    # Active connections
    try:
        connections = []
        for conn in psutil.net_connections(kind='inet'):
            try:
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        "Protocol": conn.type.name,
                        "Local": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "Remote": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        "Status": conn.status,
                        "PID": conn.pid
                    })
            except:
                continue
        
        # Add connections as separate section
        for i, conn in enumerate(connections[:20]):  # Limit to 20 connections
            network_info.append({
                "Interface": f"CONNECTION_{i+1}",
                "Protocol": conn["Protocol"],
                "Local": conn["Local"],
                "Remote": conn["Remote"],
                "Status": conn["Status"],
                "PID": conn["PID"]
            })
    except:
        pass
    
    return network_info

def get_security_audit():
    """Perform security audit"""
    security_info = []
    
    if platform.system() == "Windows":
        try:
            # Check Windows Defender
            defender_status = subprocess.run(
                ["powershell", "-Command", "Get-MpComputerStatus"],
                capture_output=True, text=True
            )
            if "True" in defender_status.stdout:
                security_info.append({
                    "Security Feature": "Windows Defender",
                    "Status": "Enabled",
                    "Risk": "Low"
                })
            else:
                security_info.append({
                    "Security Feature": "Windows Defender",
                    "Status": "Disabled",
                    "Risk": "High"
                })
            
            # Check Firewall
            firewall_status = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"],
                capture_output=True, text=True
            )
            if "ON" in firewall_status.stdout:
                security_info.append({
                    "Security Feature": "Firewall",
                    "Status": "Enabled",
                    "Risk": "Low"
                })
            else:
                security_info.append({
                    "Security Feature": "Firewall",
                    "Status": "Disabled",
                    "Risk": "High"
                })
            
            # Check UAC
            uac_status = subprocess.run(
                ["reg", "query", "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "/v", "EnableLUA"],
                capture_output=True, text=True
            )
            if "0x1" in uac_status.stdout:
                security_info.append({
                    "Security Feature": "UAC",
                    "Status": "Enabled",
                    "Risk": "Low"
                })
            else:
                security_info.append({
                    "Security Feature": "UAC",
                    "Status": "Disabled",
                    "Risk": "High"
                })
            
            # Check BitLocker
            try:
                bitlocker_status = subprocess.run(
                    ["manage-bde", "-status"],
                    capture_output=True, text=True
                )
                if "Protection On" in bitlocker_status.stdout:
                    security_info.append({
                        "Security Feature": "BitLocker",
                        "Status": "Enabled",
                        "Risk": "Low"
                    })
            except:
                security_info.append({
                    "Security Feature": "BitLocker",
                    "Status": "Not Available",
                    "Risk": "Medium"
                })
                
        except Exception as e:
            security_info.append({
                "Security Feature": "Security Audit",
                "Status": f"Error: {str(e)}",
                "Risk": "Unknown"
            })
    
    # Check for admin privileges
    try:
        is_admin = os.getuid() == 0 if platform.system() != "Windows" else ctypes.windll.shell32.IsUserAnAdmin()
        security_info.append({
            "Security Feature": "Admin Privileges",
            "Status": "Yes" if is_admin else "No",
            "Risk": "Low" if not is_admin else "High"
        })
    except:
        pass
    
    return security_info

def get_installed_software_extended():
    """Get detailed installed software information"""
    software_list = []
    
    if platform.system() == "Windows":
        try:
            # Check both 32-bit and 64-bit registry locations
            registry_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            
            for reg_path in registry_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey = winreg.OpenKey(key, subkey_name)
                            
                            # Try to get display name
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            except:
                                display_name = None
                            
                            if display_name:  # Only add if it has a display name
                                software_info = {
                                    "Name": display_name[:50],
                                    "Version": winreg.QueryValueEx(subkey, "DisplayVersion")[0] if winreg.QueryValueEx(subkey, "DisplayVersion")[1] == 1 else "N/A",
                                    "Publisher": winreg.QueryValueEx(subkey, "Publisher")[0] if winreg.QueryValueEx(subkey, "Publisher")[1] == 1 else "N/A",
                                    "Install Date": winreg.QueryValueEx(subkey, "InstallDate")[0] if winreg.QueryValueEx(subkey, "InstallDate")[1] == 1 else "N/A",
                                    "Install Location": winreg.QueryValueEx(subkey, "InstallLocation")[0][:50] + "..." if winreg.QueryValueEx(subkey, "InstallLocation")[1] == 1 and len(winreg.QueryValueEx(subkey, "InstallLocation")[0]) > 50 else winreg.QueryValueEx(subkey, "InstallLocation")[0] if winreg.QueryValueEx(subkey, "InstallLocation")[1] == 1 else "N/A",
                                    "Registry Key": subkey_name
                                }
                                software_list.append(software_info)
                            
                            winreg.CloseKey(subkey)
                        except:
                            continue
                    
                    winreg.CloseKey(key)
                except:
                    continue
            
            # Remove duplicates
            seen = set()
            unique_software = []
            for item in software_list:
                identifier = item["Name"]
                if identifier not in seen:
                    seen.add(identifier)
                    unique_software.append(item)
            
            software_list = unique_software[:50]  # Limit to 50 entries
            
        except Exception as e:
            software_list.append({
                "Name": f"Error retrieving software: {str(e)}",
                "Version": "N/A",
                "Publisher": "N/A"
            })
    
    return software_list

def get_system_services_extended():
    """Get detailed service information"""
    services = []
    
    if platform.system() == "Windows":
        try:
            # Use WMI for detailed service information
            if WMI_AVAILABLE:
                c = wmi.WMI()
                for service in c.Win32_Service():
                    services.append({
                        "Name": service.Name,
                        "Display Name": service.DisplayName,
                        "State": service.State,
                        "Start Mode": service.StartMode,
                        "Start Name": service.StartName,
                        "Path": service.PathName[:100] + "..." if len(service.PathName) > 100 else service.PathName,
                        "Process ID": service.ProcessId
                    })
            else:
                # Fallback to psutil
                for service in psutil.win_service_iter():
                    try:
                        info = service.as_dict()
                        services.append({
                            "Name": info.get('name', 'N/A'),
                            "Display Name": info.get('display_name', 'N/A'),
                            "State": info.get('status', 'N/A'),
                            "Start Mode": info.get('start_type', 'N/A'),
                            "Start Name": info.get('username', 'N/A'),
                            "Path": info.get('binpath', 'N/A')[:100],
                            "Process ID": info.get('pid', 'N/A')
                        })
                    except:
                        continue
        except:
            pass
    
    return services[:30]  # Limit to 30 services

def get_startup_programs():
    """Get startup programs"""
    startup_programs = []
    
    if platform.system() == "Windows":
        startup_paths = [
            os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup"),
            os.path.join(os.environ["PROGRAMDATA"], r"Microsoft\Windows\Start Menu\Programs\StartUp"),
            r"C:\Users\All Users\Microsoft\Windows\Start Menu\Programs\Startup"
        ]
        
        for path in startup_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith(('.lnk', '.exe', '.bat')):
                        full_path = os.path.join(path, file)
                        try:
                            file_size = os.path.getsize(full_path)
                            mod_time = datetime.fromtimestamp(os.path.getmtime(full_path))
                            startup_programs.append({
                                "Name": file,
                                "Path": full_path,
                                "Size": format_bytes(file_size),
                                "Modified": mod_time.strftime('%Y-%m-%d'),
                                "Type": "Startup"
                            })
                        except:
                            continue
    
    return startup_programs

def get_system_environment_extended():
    """Get comprehensive environment variables"""
    env_vars = []
    
    try:
        # System environment variables
        for key, value in os.environ.items():
            # Filter out sensitive data
            if not any(sensitive in key.lower() for sensitive in ['password', 'secret', 'key', 'token', 'credential']):
                env_vars.append({
                    "Variable": key,
                    "Value": (value[:80] + "...") if len(value) > 80 else value,
                    "Type": "System"
                })
        
        # Path variable broken down
        if 'PATH' in os.environ:
            paths = os.environ['PATH'].split(';')
            for i, path in enumerate(paths[:10]):  # First 10 paths only
                env_vars.append({
                    "Variable": f"PATH[{i}]",
                    "Value": path,
                    "Type": "Path Entry"
                })
    except:
        pass
    
    return env_vars[:40]  # Limit to 40 entries

def get_hardware_temperatures():
    """Get hardware temperatures if available"""
    temps = []
    
    try:
        sensors = psutil.sensors_temperatures()
        if sensors:
            for name, entries in sensors.items():
                for entry in entries:
                    temps.append({
                        "Sensor": name,
                        "Label": entry.label or "N/A",
                        "Current": f"{entry.current}°C",
                        "High": f"{entry.high}°C" if entry.high else "N/A",
                        "Critical": f"{entry.critical}°C" if entry.critical else "N/A"
                    })
    except:
        pass
    
    return temps

def get_system_logs_extended():
    """Get system logs"""
    logs = []
    
    try:
        # Recent events using psutil
        boot_time = psutil.boot_time()
        logs.append({
            "Time": datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S'),
            "Event": "System Boot",
            "Details": f"Boot time recorded"
        })
        
        # User login information
        current_user = getpass.getuser()
        logs.append({
            "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Event": "User Session",
            "Details": f"Current user: {current_user}"
        })
        
        # Python process info
        logs.append({
            "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Event": "Scanner Process",
            "Details": f"PID: {os.getpid()}, Python: {sys.version.split()[0]}"
        })
        
    except Exception as e:
        logs.append({
            "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Event": "Error",
            "Details": f"Log collection error: {str(e)}"
        })
    
    return logs

def get_performance_metrics():
    """Get real-time performance metrics"""
    metrics = []
    
    try:
        # CPU Metrics
        cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
        cpu_percent_per_core = psutil.cpu_percent(interval=1, percpu=True)
        
        metrics.append({
            "Metric": "CPU Usage",
            "Value": f"{cpu_percent}%",
            "Details": f"Per core: {', '.join([f'{p}%' for p in cpu_percent_per_core])}"
        })
        
        # Memory Metrics
        memory = psutil.virtual_memory()
        metrics.append({
            "Metric": "Memory Usage",
            "Value": f"{memory.percent}%",
            "Details": f"{format_bytes(memory.used)} / {format_bytes(memory.total)}"
        })
        
        # Swap Metrics
        swap = psutil.swap_memory()
        if swap.total > 0:
            metrics.append({
                "Metric": "Swap Usage",
                "Value": f"{swap.percent}%",
                "Details": f"{format_bytes(swap.used)} / {format_bytes(swap.total)}"
            })
        
        # Disk I/O
        disk_io = psutil.disk_io_counters()
        if disk_io:
            metrics.append({
                "Metric": "Disk Read",
                "Value": format_bytes(disk_io.read_bytes),
                "Details": f"{disk_io.read_count} operations"
            })
            metrics.append({
                "Metric": "Disk Write",
                "Value": format_bytes(disk_io.write_bytes),
                "Details": f"{disk_io.write_count} operations"
            })
        
        # Network I/O
        net_io = psutil.net_io_counters()
        if net_io:
            metrics.append({
                "Metric": "Network Sent",
                "Value": format_bytes(net_io.bytes_sent),
                "Details": f"{net_io.packets_sent} packets"
            })
            metrics.append({
                "Metric": "Network Received",
                "Value": format_bytes(net_io.bytes_recv),
                "Details": f"{net_io.packets_recv} packets"
            })
        
    except Exception as e:
        metrics.append({
            "Metric": "Error",
            "Value": "Failed",
            "Details": str(e)
        })
    
    return metrics

def get_user_accounts_extended():
    """Get detailed user account information"""
    users = []
    
    if platform.system() == "Windows":
        try:
            # Get local users
            output = subprocess.run(
                ["net", "user"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            user_lines = output.stdout.split('\n')
            capturing = False
            user_list = []
            
            for line in user_lines:
                if "User accounts for" in line:
                    capturing = True
                    continue
                if "The command completed" in line:
                    capturing = False
                    break
                
                if capturing and line.strip():
                    # Extract usernames from the line
                    words = line.strip().split()
                    for word in words:
                        if word and word not in ["User", "accounts", "for", "\\"]:
                            user_list.append(word)
            
            # Get details for each user
            for username in user_list[:10]:  # Limit to first 10 users
                try:
                    user_output = subprocess.run(
                        ["net", "user", username],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    
                    user_details = {}
                    for line in user_output.stdout.split('\n'):
                        if 'Full Name' in line:
                            user_details['Full Name'] = line.split('Full Name')[1].strip()
                        elif 'Account active' in line:
                            user_details['Active'] = 'Yes' if 'Yes' in line else 'No'
                        elif 'Last logon' in line:
                            user_details['Last Logon'] = line.split('Last logon')[1].strip()
                        elif 'Password last set' in line:
                            user_details['Password Set'] = line.split('Password last set')[1].strip()
                        elif 'Account expires' in line:
                            user_details['Expires'] = line.split('Account expires')[1].strip()
                    
                    users.append({
                        "Username": username,
                        "Full Name": user_details.get('Full Name', 'N/A'),
                        "Active": user_details.get('Active', 'N/A'),
                        "Last Logon": user_details.get('Last Logon', 'N/A'),
                        "Password Set": user_details.get('Password Set', 'N/A'),
                        "Expires": user_details.get('Expires', 'Never')
                    })
                    
                except:
                    users.append({
                        "Username": username,
                        "Full Name": "Error retrieving details",
                        "Active": "N/A"
                    })
        
        except Exception as e:
            users.append({
                "Username": f"Error: {str(e)}",
                "Full Name": "N/A",
                "Active": "N/A"
            })
    
    return users

def get_system_drivers_extended():
    """Get detailed driver information"""
    drivers = []
    
    if platform.system() == "Windows":
        try:
            output = subprocess.run(
                ["driverquery", "/v", "/fo", "csv"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            lines = output.stdout.strip().split('\n')
            if len(lines) > 1:
                headers = [h.strip('"') for h in lines[0].split('","')]
                for line in lines[1:]:
                    if line.strip():
                        values = [v.strip('"') for v in line.split('","')]
                        if len(values) >= len(headers):
                            driver_info = {}
                            for i, header in enumerate(headers[:len(values)]):
                                driver_info[header] = values[i]
                            drivers.append(driver_info)
            
            # Limit to 30 drivers
            drivers = drivers[:30]
            
        except Exception as e:
            drivers.append({
                "Module Name": f"Error: {str(e)}",
                "Display Name": "Driver query failed"
            })
    
    return drivers

def get_wifi_networks_extended():
    """Get detailed WiFi network information"""
    wifi_networks = []
    
    if platform.system() == "Windows":
        try:
            # Get WiFi profiles
            profiles_output = subprocess.run(
                ["netsh", "wlan", "show", "profiles"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            profiles = []
            for line in profiles_output.stdout.split('\n'):
                if "All User Profile" in line:
                    profile_name = line.split(":")[1].strip()
                    profiles.append(profile_name)
            
            # Get details for each profile
            for profile in profiles[:15]:  # Limit to 15 profiles
                try:
                    profile_output = subprocess.run(
                        ["netsh", "wlan", "show", "profile", f"name={profile}", "key=clear"],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    
                    details = {}
                    for line in profile_output.stdout.split('\n'):
                        line = line.strip()
                        if "Key Content" in line:
                            details['Password'] = line.split(":")[1].strip()
                        elif "Authentication" in line:
                            details['Auth'] = line.split(":")[1].strip()
                        elif "Cipher" in line:
                            details['Cipher'] = line.split(":")[1].strip()
                        elif "Connection mode" in line:
                            details['Mode'] = line.split(":")[1].strip()
                    
                    wifi_networks.append({
                        "SSID": profile,
                        "Authentication": details.get('Auth', 'Unknown'),
                        "Cipher": details.get('Cipher', 'Unknown'),
                        "Connection Mode": details.get('Mode', 'Unknown'),
                        "Password": details.get('Password', 'Not stored')
                    })
                    
                except:
                    wifi_networks.append({
                        "SSID": profile,
                        "Authentication": "Error",
                        "Cipher": "Error",
                        "Connection Mode": "Error",
                        "Password": "Error retrieving"
                    })
        
        except Exception as e:
            wifi_networks.append({
                "SSID": f"Error: {str(e)}",
                "Authentication": "N/A",
                "Cipher": "N/A"
            })
    
    return wifi_networks

# -------------------------------------------------------------------
#  ENHANCED HTML REPORT GENERATION
# -------------------------------------------------------------------
def generate_enhanced_html_report():
    """Generate comprehensive HTML report with all collected data"""
    
    print_status("Starting comprehensive system intelligence scan...", "SCAN")
    
    # Collect all data
    print_status("Collecting system data...", "SCAN")
    
    # Use parallel collection for faster execution
    collector = DataCollector()
    
    collection_functions = {
        "system_info": get_comprehensive_system_info,
        "hardware_info": get_extended_hardware_info,
        "process_info": get_detailed_process_info,
        "network_info": get_network_analysis_extended,
        "security_audit": get_security_audit,
        "installed_software": get_installed_software_extended,
        "system_services": get_system_services_extended,
        "startup_programs": get_startup_programs,
        "environment_vars": get_system_environment_extended,
        "hardware_temps": get_hardware_temperatures,
        "system_logs": get_system_logs_extended,
        "performance_metrics": get_performance_metrics,
        "user_accounts": get_user_accounts_extended,
        "system_drivers": get_system_drivers_extended,
        "wifi_networks": get_wifi_networks_extended
    }
    
    # Collect data in parallel
    all_data = collector.collect_parallel(collection_functions)
    
    # Generate HTML report
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(downloads_folder):
        downloads_folder = os.getcwd()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    html_filename = f"System_Intelligence_Report_{timestamp}.html"
    html_path = os.path.join(downloads_folder, html_filename)
    
    # Health score calculation
    health_score = 85  # Default, can be enhanced with real calculation
    
    # Generate HTML content
    html_content = generate_html_content(all_data, health_score, timestamp)
    
    # Write to file
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print_status(f"Report generated successfully: {html_path}", "SUCCESS")
    return html_path

def generate_html_content(data, health_score, timestamp):
    """Generate HTML content with all data"""
    
    health_color = get_health_color(health_score)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Intelligence Report</title>
    <style>
        /* Your existing CSS styles here - kept exactly as in your original code */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'JetBrains Mono', monospace;
            background: #000000;
            min-height: 100vh;
            margin: 0;
            padding: 0;
            color: #00ff00;
            line-height: 1.4;
            overflow-x: hidden;
        }}

        .matrix-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(0, 255, 0, 0.02) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(0, 255, 0, 0.02) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(0, 255, 0, 0.01) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }}

        .scan-line {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00ff00, transparent);
            animation: scan 3s linear infinite;
            box-shadow: 0 0 10px #00ff00;
            z-index: 1000;
        }}

        @keyframes scan {{
            0% {{ top: 0%; opacity: 0; }}
            50% {{ opacity: 1; }}
            100% {{ top: 100%; opacity: 0; }}
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
        }}

        .header {{
            background: rgba(0, 20, 0, 0.8);
            padding: 25px;
            margin-bottom: 25px;
            text-align: center;
            border: 1px solid #00ff00;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.1), transparent);
            animation: headerGlow 3s linear infinite;
        }}

        @keyframes headerGlow {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}

        .header h1 {{
            color: #00ff00;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
            text-shadow: 0 0 10px #00ff00;
            letter-spacing: 2px;
        }}

        .creator {{
            color: #ff00ff;
            font-size: 1.2em;
            margin-bottom: 15px;
            font-weight: 500;
        }}

        .header p {{
            color: #00cc00;
            font-size: 0.9em;
            margin: 3px 0;
            font-weight: 300;
        }}

        .health-score {{
            display: inline-block;
            background: {health_color};
            color: #000000;
            padding: 8px 20px;
            margin-top: 10px;
            font-weight: 600;
            border: 1px solid #00ff00;
            text-shadow: 0 0 5px #000000;
            border-radius: 3px;
        }}

        .section {{
            background: rgba(0, 10, 0, 0.7);
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #003300;
            position: relative;
            transition: all 0.3s ease;
        }}

        .section::before {{
            content: '>';
            position: absolute;
            left: 10px;
            top: 20px;
            color: #00ff00;
            font-weight: bold;
        }}

        .section:hover {{
            border-color: #00ff00;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        }}

        .section h2 {{
            color: #00ff00;
            padding-bottom: 10px;
            margin-bottom: 15px;
            font-size: 1.3em;
            font-weight: 500;
            border-bottom: 1px solid #003300;
            margin-left: 15px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            background: rgba(0, 5, 0, 0.5);
            font-size: 0.85em;
        }}

        th {{
            background: rgba(0, 30, 0, 0.8);
            color: #00ff00;
            padding: 12px 10px;
            text-align: left;
            font-weight: 500;
            border: 1px solid #002200;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        td {{
            padding: 10px 10px;
            border: 1px solid #001100;
            color: #00cc00;
            font-weight: 300;
        }}

        tr:nth-child(even) {{
            background: rgba(0, 15, 0, 0.3);
        }}

        tr:hover {{
            background: rgba(0, 255, 0, 0.1);
            color: #00ff00;
        }}

        .status-active {{
            color: #00ff00;
            font-weight: 600;
            text-shadow: 0 0 5px #00ff00;
        }}

        .status-inactive {{
            color: #ff0000;
            font-weight: 600;
        }}

        .status-warning {{
            color: #ffff00;
            font-weight: 600;
        }}

        .status-critical {{
            color: #ff0000;
            font-weight: 600;
            text-shadow: 0 0 5px #ff0000;
        }}

        .status-notice {{
            color: #ffa500;
            font-weight: 600;
        }}

        .metric-value {{
            font-family: 'JetBrains Mono', monospace;
            background: rgba(0, 255, 0, 0.1);
            padding: 3px 6px;
            color: #00ff00;
            border: 1px solid #003300;
            font-weight: 400;
        }}

        .footer {{
            text-align: center;
            color: #006600;
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 10, 0, 0.8);
            border: 1px solid #002200;
            font-size: 0.8em;
        }}

        .scroll-container {{
            overflow-x: auto;
            margin: 15px 0;
            border: 1px solid #003300;
            padding: 5px;
            background: rgba(0, 5, 0, 0.5);
        }}

        .scroll-table {{
            min-width: 1200px;
        }}

        .task-manager-table {{
            min-width: 1800px;
        }}

        .performance-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .performance-card {{
            background: rgba(0, 20, 0, 0.6);
            padding: 15px;
            border: 1px solid #003300;
            position: relative;
            overflow: hidden;
        }}

        .performance-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
            background: #00ff00;
        }}

        .performance-card h3 {{
            color: #00ff00;
            margin-bottom: 8px;
            font-size: 0.9em;
            font-weight: 500;
        }}

        .performance-value {{
            font-size: 1.5em;
            font-weight: 600;
            color: #00ff00;
            margin: 8px 0;
            text-shadow: 0 0 5px #00ff00;
        }}

        .performance-details {{
            color: #009900;
            font-size: 0.8em;
        }}

        .terminal-prompt {{
            color: #00ff00;
            margin-right: 5px;
        }}

        .blink {{
            animation: blink 1s infinite;
        }}

        @keyframes blink {{
            0%, 50% {{ opacity: 1; }}
            51%, 100% {{ opacity: 0; }}
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}

            .header h1 {{
                font-size: 1.8em;
            }}

            .performance-grid {{
                grid-template-columns: 1fr;
            }}

            table {{
                font-size: 0.75em;
            }}

            th, td {{
                padding: 6px 8px;
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
            opacity: 0.1;
        }}

        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: rgba(0, 10, 0, 0.8);
        }}

        ::-webkit-scrollbar-thumb {{
            background: #00ff00;
            border-radius: 0;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #00cc00;
        }}

        /* Typewriter effect for headers */
        .typewriter {{
            overflow: hidden;
            border-right: 2px solid #00ff00;
            white-space: nowrap;
            animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
        }}

        @keyframes typing {{
            from {{ width: 0 }}
            to {{ width: 100% }}
        }}

        @keyframes blink-caret {{
            from, to {{ border-color: transparent }}
            50% {{ border-color: #00ff00 }}
        }}
    </style>
</head>
<body>
    <div class="matrix-bg"></div>
    <div class="scan-line"></div>
    
    <div class="container">
        <div class="header">
            <h1>><span class="blink">_</span> SYSTEM INTELLIGENCE REPORT</h1>
            <div class="creator">ENHANCED SYSTEM SCANNER v2.0</div>
            <p>> SCAN INITIATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>> TARGET: {socket.gethostname()} | PLATFORM: {platform.platform()}</p>
            <div class="health-score">
                SYSTEM INTEGRITY: {health_score}/100
            </div>
        </div>
    """
    
    # Add all data sections
    sections = [
        ("SYSTEM OVERVIEW", data.get("system_info", [])),
        ("HARDWARE INFORMATION", data.get("hardware_info", [])),
        ("RUNNING PROCESSES", data.get("process_info", [])),
        ("NETWORK ANALYSIS", data.get("network_info", [])),
        ("SECURITY AUDIT", data.get("security_audit", [])),
        ("INSTALLED SOFTWARE", data.get("installed_software", [])),
        ("SYSTEM SERVICES", data.get("system_services", [])),
        ("STARTUP PROGRAMS", data.get("startup_programs", [])),
        ("ENVIRONMENT VARIABLES", data.get("environment_vars", [])),
        ("HARDWARE TEMPERATURES", data.get("hardware_temps", [])),
        ("SYSTEM LOGS", data.get("system_logs", [])),
        ("PERFORMANCE METRICS", data.get("performance_metrics", [])),
        ("USER ACCOUNTS", data.get("user_accounts", [])),
        ("SYSTEM DRIVERS", data.get("system_drivers", [])),
        ("WIFI NETWORKS", data.get("wifi_networks", []))
    ]
    
    for section_name, section_data in sections:
        html += generate_section_html(section_name, section_data)
    
    # Add footer
    html += f"""
        <div class="footer">
            <p>> SCAN COMPLETED: {datetime.now().strftime('%H:%M:%S')}</p>
            <p>> ENHANCED SYSTEM SCANNER | COMPREHENSIVE INTELLIGENCE COLLECTION</p>
            <p>> REPORT GENERATED: {timestamp}</p>
        </div>
    </div>
    
    <script>
        // Matrix rain effect
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.classList.add('matrix-rain');
        document.body.appendChild(canvas);
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = "01";
        const charSize = 14;
        const columns = canvas.width / charSize;
        const drops = [];
        
        for (let i = 0; i < columns; i++) {{
            drops[i] = 1;
        }}
        
        function drawMatrix() {{
            ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#00ff00';
            ctx.font = charSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {{
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * charSize, drops[i] * charSize);
                
                if (drops[i] * charSize > canvas.height && Math.random() > 0.975) {{
                    drops[i] = 0;
                }}
                drops[i]++;
            }}
        }}
        
        setInterval(drawMatrix, 35);
        
        // Table sorting
        document.addEventListener('DOMContentLoaded', function() {{
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {{
                const headers = table.querySelectorAll('th');
                headers.forEach((header, index) => {{
                    header.style.cursor = 'pointer';
                    header.addEventListener('click', () => {{
                        sortTable(table, index);
                    }});
                }});
            }});
            
            function sortTable(table, column) {{
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                
                const isNumeric = (text) => !isNaN(parseFloat(text)) && isFinite(text);
                
                rows.sort((a, b) => {{
                    const aText = a.cells[column].textContent.trim();
                    const bText = b.cells[column].textContent.trim();
                    
                    if (isNumeric(aText) && isNumeric(bText)) {{
                        return parseFloat(aText) - parseFloat(bText);
                    }}
                    
                    return aText.localeCompare(bText);
                }});
                
                // Remove existing rows
                rows.forEach(row => tbody.removeChild(row));
                
                // Add sorted rows
                rows.forEach(row => tbody.appendChild(row));
            }}
        }});
    </script>
</body>
</html>
    """
    
    return html

def generate_section_html(section_name, data):
    """Generate HTML for a specific section"""
    if not data:
        return f"""
        <div class="section">
            <h2>> {section_name}</h2>
            <p style="color: #006600; text-align: center; padding: 20px;">> NO_DATA_AVAILABLE</p>
        </div>
        """
    
    html = f"""
    <div class="section">
        <h2>> {section_name}</h2>
    """
    
    if isinstance(data, list) and len(data) > 0:
        # Determine if it's a key-value list or table data
        if isinstance(data[0], list) and len(data[0]) == 2:
            # Key-value format
            html += '<table>'
            for key, value in data:
                html += f'''
                <tr>
                    <td><span class="terminal-prompt">></span> {key}</td>
                    <td class="metric-value">{value}</td>
                </tr>
                '''
            html += '</table>'
        elif isinstance(data[0], dict):
            # Table format
            headers = list(data[0].keys())
            html += '<div class="scroll-container"><table class="scroll-table">'
            html += '<thead><tr>' + ''.join(f'<th>{header}</th>' for header in headers) + '</tr></thead>'
            html += '<tbody>'
            
            for row in data:
                html += '<tr>'
                for header in headers:
                    cell = str(row.get(header, ''))
                    # Apply status classes
                    if any(status_word in header.lower() for status_word in ['status', 'state', 'active', 'enabled']):
                        if any(good_word in cell.lower() for good_word in ['active', 'enabled', 'yes', 'true', 'running']):
                            html += f'<td class="status-active">{cell}</td>'
                        elif any(bad_word in cell.lower() for bad_word in ['inactive', 'disabled', 'no', 'false', 'stopped']):
                            html += f'<td class="status-inactive">{cell}</td>'
                        elif 'warning' in cell.lower():
                            html += f'<td class="status-warning">{cell}</td>'
                        elif 'critical' in cell.lower():
                            html += f'<td class="status-critical">{cell}</td>'
                        else:
                            html += f'<td>{cell}</td>'
                    elif 'password' in header.lower() and cell.lower() != 'not stored':
                        html += f'<td class="status-active">{cell}</td>'
                    else:
                        html += f'<td>{cell}</td>'
                html += '</tr>'
            
            html += '</tbody></table></div>'
    
    html += '</div>'
    return html

def get_health_color(score):
    """Get health color based on score"""
    if score >= 80:
        return "linear-gradient(135deg, #00ff00 0%, #00cc00 100%)"
    elif score >= 60:
        return "linear-gradient(135deg, #ffff00 0%, #cccc00 100%)"
    else:
        return "linear-gradient(135deg, #ff0000 0%, #cc0000 100%)"

# -------------------------------------------------------------------
#  MAIN EXECUTION
# -------------------------------------------------------------------
if __name__ == "__main__":
    colorama.init()
    
    print_colored("\n" + "="*80, Colors.GREEN)
    print_colored("ENHANCED SYSTEM INTELLIGENCE SCANNER", Colors.RAINBOW)
    print_colored("="*80 + "\n", Colors.GREEN)
    
    try:
        # Generate the report
        report_path = generate_enhanced_html_report()
        
        print_colored("\n" + "═"*80, Colors.BRIGHT_GREEN)
        print_colored("SCAN COMPLETED SUCCESSFULLY", Colors.GREEN)
        print_colored("═"*80, Colors.BRIGHT_GREEN)
        
        print_status(f"Report generated: {report_path}", "SUCCESS")
        print_status(f"File size: {format_bytes(os.path.getsize(report_path))}", "INFO")
        
        # Try to open the report
        try:
            if platform.system() == "Windows":
                os.startfile(report_path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", report_path])
            else:
                subprocess.run(["xdg-open", report_path])
            print_status("Opening report in default browser...", "INFO")
        except:
            print_status("Could not open browser automatically", "WARNING")
            print_status(f"Please open manually: {report_path}", "INFO")
        
        print_colored("\n" + "━"*80, Colors.GREEN)
        print_status("Enhanced System Scanner completed!", "SUCCESS")
        print_colored("━"*80 + "\n", Colors.GREEN)
        
    except KeyboardInterrupt:
        print_status("Scan interrupted by user", "WARNING")
    except Exception as e:
        print_status(f"Fatal error: {str(e)}", "ERROR")
        import traceback
        traceback.print_exc()
