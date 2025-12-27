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
from collections import OrderedDict
import webbrowser


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


for package in ["psutil", "tabulate", "blessings", "colorama"]:
    install_package(package)

import psutil
from tabulate import tabulate
from colorama import init, Fore, Back, Style
from blessings import Terminal

init(autoreset=True)
term = Terminal()


# -------------------------------------------------------------------
#  ENHANCED CONSOLE COLORS AND PROGRESS UTILITIES
# -------------------------------------------------------------------
class Colors:
    # Enhanced ANSI colors with gradients
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    # Lofi color palette
    LOFI_PINK = '\033[38;5;218m'
    LOFI_BLUE = '\033[38;5;117m'
    LOFI_GREEN = '\033[38;5;158m'
    LOFI_PURPLE = '\033[38;5;189m'
    LOFI_ORANGE = '\033[38;5;223m'
    LOFI_TEAL = '\033[38;5;86m'
    LOFI_LAVENDER = '\033[38;5;183m'
    
    @staticmethod
    def gradient(text, start_color, end_color):
        """Create gradient text effect"""
        result = ""
        length = len(text)
        for i, char in enumerate(text):
            ratio = i / max(1, length - 1)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            result += f'\033[38;2;{r};{g};{b}m{char}'
        return result + Colors.RESET
    
    @staticmethod
    def lofi_gradient(text):
        """Lofi-style gradient"""
        colors = [
            (255, 182, 193),  # Light Pink
            (173, 216, 230),  # Light Blue
            (152, 251, 152),  # Pale Green
            (221, 160, 221),  # Plum
            (255, 218, 185),  # Peach
        ]
        return Colors.gradient(text, colors[0], colors[-1])


def print_colored(text, color=Colors.WHITE, style="", end="\n"):
    """Enhanced print with styles"""
    styles = {
        "bold": '\033[1m',
        "italic": '\033[3m',
        "underline": '\033[4m',
        "blink": '\033[5m',
    }
    style_code = styles.get(style, "")
    print(f"{style_code}{color}{text}{Colors.RESET}", end=end)


def animate_text(text, delay=0.03, color=Colors.LOFI_BLUE):
    """Typewriter animation for text"""
    for char in text:
        print(f"{color}{char}{Colors.RESET}", end='', flush=True)
        time.sleep(delay)
    print()


def print_banner():
    """Enhanced Lofi-style banner with animations"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{Colors.LOFI_PURPLE}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗     ║
    ║    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║     ║
    ║    ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║     ║
    ║    ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║     ║
    ║    ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║     ║
    ║    ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝     ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.LOFI_GREEN}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        S Y S T E M   S C A N N E R   V 3 . 0                  ║
    ║                     ~ LOFI EDITION ~                          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    
    for line in banner.split('\n'):
        print_colored(line, Colors.LOFI_BLUE)
        time.sleep(0.01)
    
    print("\n" * 2)
    animate_text(" " * 20 + "✦  SABARI425 presents  ✦", 0.05, Colors.LOFI_PINK)
    animate_text(" " * 15 + "~ Lofi beats & system metrics ~", 0.04, Colors.LOFI_TEAL)
    print("\n" * 2)


# -------------------------------------------------------------------
#  ENHANCED PROGRESS BAR WITH LOFI STYLE
# -------------------------------------------------------------------
def lofi_progress_bar(iteration, total, prefix='', suffix='', length=40, 
                     fill='█', empty='░', color=Colors.LOFI_BLUE):
    """Lofi-style animated progress bar"""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled = int(length * iteration // total)
    bar = fill * filled + empty * (length - filled)
    
    # Create gradient effect
    gradient_bar = ""
    for i, char in enumerate(bar):
        if i < filled:
            ratio = i / max(1, length - 1)
            r = int(173 + (152 - 173) * ratio)  # Blue to Green
            g = int(216 + (251 - 216) * ratio)
            b = int(230 + (152 - 230) * ratio)
            gradient_bar += f'\033[38;2;{r};{g};{b}m{char}'
        else:
            gradient_bar += f'\033[38;5;236m{char}'
    
    sys.stdout.write(f'\r{prefix} │{gradient_bar}{Colors.RESET}│ {percent}% {suffix}')
    sys.stdout.flush()
    
    if iteration == total:
        print()


def simulate_scan_step(step_name, duration=0.5, steps=30):
    """Enhanced scan step with Lofi animations"""
    print()
    print_colored(f"   ↪  Scanning: {step_name}", Colors.LOFI_BLUE, "italic")
    
    for i in range(steps + 1):
        lofi_progress_bar(i, steps, 
                         prefix='   ', 
                         suffix=step_name[:20],
                         length=50,
                         fill='♬',
                         empty='·',
                         color=Colors.LOFI_PURPLE)
        time.sleep(duration / steps)
    
    print_colored(f"   ✓  Completed: {step_name}", Colors.LOFI_GREEN)
    time.sleep(0.1)


# -------------------------------------------------------------------
#  ENHANCED COMMAND EXECUTOR
# -------------------------------------------------------------------
command_cache = {}

def run_cmd(cmd, use_cache=True, task_name="Executing command"):
    cache_key = f"{cmd}_{platform.system()}"
    
    if use_cache and cache_key in command_cache:
        cached_time, output = command_cache[cache_key]
        if (datetime.now() - cached_time).seconds < 300:
            return output
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=15
        )
        
        output = result.stdout.strip()
        
        if use_cache:
            command_cache[cache_key] = (datetime.now(), output)
        
        return output
        
    except Exception as e:
        return f"[ERROR] {str(e)}"


# -------------------------------------------------------------------
#  ENHANCED DATA COLLECTION FUNCTIONS
# -------------------------------------------------------------------
def get_system_health_score():
    """Enhanced health scoring with detailed metrics"""
    score = 100
    metrics = []
    
    try:
        # CPU Health
        cpu_usage = psutil.cpu_percent(interval=0.5)
        cpu_score = max(0, 25 - (cpu_usage / 4))
        score += cpu_score - 25
        metrics.append(f"CPU: {cpu_usage:.1f}% ({cpu_score:.1f}/25)")
        
        # Memory Health
        memory = psutil.virtual_memory()
        mem_score = max(0, 25 - (memory.percent / 4))
        score += mem_score - 25
        metrics.append(f"RAM: {memory.percent:.1f}% ({mem_score:.1f}/25)")
        
        # Disk Health
        disk_score = 20
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                if usage.percent > 90:
                    disk_score -= 5
                elif usage.percent > 80:
                    disk_score -= 3
            except:
                pass
        score += disk_score - 20
        metrics.append(f"Disk: {disk_score:.1f}/20")
        
        # Temperature Health
        temp_score = 15
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for entries in temps.values():
                    for entry in entries:
                        if entry.current > 80:
                            temp_score -= 5
        except:
            temp_score = 10
        score += temp_score - 15
        metrics.append(f"Temp: {temp_score:.1f}/15")
        
        # Process Health
        proc_score = 15
        zombie_count = sum(1 for p in psutil.process_iter(['status']) 
                          if p.info['status'] == psutil.STATUS_ZOMBIE)
        proc_score -= min(zombie_count * 2, 10)
        score += proc_score - 15
        metrics.append(f"Process: {proc_score:.1f}/15")
        
    except Exception as e:
        print_colored(f"Health score error: {e}", Colors.RED)
    
    return max(0, min(100, int(score))), metrics


# -------------------------------------------------------------------
#  PASSWORD CHECK FUNCTION (KEEPING YOUR SECURITY)
# -------------------------------------------------------------------
p = "e1f7dv6i7yt4d"
f = "h8i6d7ch7fi"
y = "5gd3o6h37r2i"
e = "yg7ja83mf83"
t = "k7g83h7b6sk9j"
s = "t5ha7ui8je72"
r = "h7Sg0yt6yjH1"
a = "6y8ih4i8rg5"
g = "i47i8p69j3d"
w = "u4bdgt5h4f7k"

def check_password():
    """Enhanced password check with animations"""
    print_colored("\n" + "═" * 60, Colors.LOFI_PURPLE)
    print_colored("   🔐  ACCESS VERIFICATION REQUIRED", Colors.LOFI_PINK, "bold")
    print_colored("═" * 60, Colors.LOFI_PURPLE)
    
    attempts = 3
    for attempt in range(attempts):
        print_colored(f"\n   Attempt {attempt + 1}/{attempts}", Colors.LOFI_BLUE)
        
        # Animated password input
        password = ""
        print_colored("   Enter password: ", Colors.LOFI_GREEN, end='')
        
        # Simple input animation
        for _ in range(3):
            print_colored(".", Colors.LOFI_PURPLE, end='')
            time.sleep(0.3)
        
        # Get password (hidden input)
        import msvcrt if os.name == 'nt' else getpass
        if os.name == 'nt':
            while True:
                ch = msvcrt.getch()
                if ch == b'\r':
                    break
                elif ch == b'\x08':
                    password = password[:-1]
                else:
                    password += ch.decode()
                print('*', end='', flush=True)
            print()
        else:
            password = getpass.getpass("")
        
        correct_pwd = r[2]+e[4]+t[7]+s[3]+y[9]+f[2]+p[11]+w[8]+a[5]+g[1]
        
        if password == correct_pwd:
            print_colored("\n   ✓  ACCESS GRANTED", Colors.LOFI_GREEN, "bold")
            time.sleep(1)
            return True
        else:
            print_colored("   ✗  INCORRECT PASSWORD", Colors.RED)
            if attempt < attempts - 1:
                print_colored(f"   {attempts - attempt - 1} attempts remaining", Colors.YELLOW)
    
    print_colored("\n   ⚠  ACCESS DENIED - TOO MANY FAILED ATTEMPTS", Colors.RED, "bold")
    return False


# -------------------------------------------------------------------
#  ENHANCED HTML REPORT WITH LOFI ANIMATIONS
# -------------------------------------------------------------------
def generate_html_report():
    """Generate HTML report with smooth Lofi animations"""
    print_banner()
    
    # Enhanced scanning animation
    scan_steps = [
        ("Initializing Scanner", 0.3),
        ("Analyzing Hardware", 0.4),
        ("Scanning Memory", 0.3),
        ("Checking Storage", 0.4),
        ("Network Analysis", 0.5),
        ("Security Check", 0.3),
        ("Performance Metrics", 0.4),
        ("Generating Report", 0.6)
    ]
    
    for step, duration in scan_steps:
        simulate_scan_step(step, duration, 25)
    
    # Get system data
    health_score, metrics = get_system_health_score()
    
    # Create HTML with enhanced Lofi animations
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Scan Report | Lofi Edition</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500&family=Poppins:wght@300;400;500&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: #e0e0ff;
            min-height: 100vh;
            overflow-x: hidden;
            line-height: 1.6;
        }}
        
        /* Lofi Animation Background */
        .lofi-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            opacity: 0.3;
            background: 
                radial-gradient(circle at 20% 50%, rgba(173, 216, 230, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 182, 193, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(152, 251, 152, 0.1) 0%, transparent 50%);
        }}
        
        /* Floating Elements Animation */
        .floating-elements {{
            position: fixed;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
        }}
        
        .floating-element {{
            position: absolute;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            animation: float 15s infinite ease-in-out;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
            25% {{ transform: translate(100px, 50px) rotate(90deg); }}
            50% {{ transform: translate(50px, 100px) rotate(180deg); }}
            75% {{ transform: translate(-50px, 50px) rotate(270deg); }}
        }}
        
        /* Scan Line Animation */
        .scan-line {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(173, 216, 230, 0.8),
                rgba(255, 182, 193, 0.8),
                transparent);
            z-index: 1000;
            animation: scan 3s ease-in-out infinite;
            box-shadow: 0 0 20px rgba(173, 216, 230, 0.5);
        }}
        
        @keyframes scan {{
            0% {{ top: 0%; opacity: 0; }}
            50% {{ opacity: 1; }}
            100% {{ top: 100%; opacity: 0; }}
        }}
        
        /* Main Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
        }}
        
        /* Header with Glow Effect */
        .header {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(173, 216, 230, 0.1),
                rgba(255, 182, 193, 0.1),
                transparent
            );
            animation: rotate 20s linear infinite;
        }}
        
        @keyframes rotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .header-content {{
            position: relative;
            z-index: 1;
        }}
        
        h1 {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.8em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #add8e6, #ffb6c1, #98fb98);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 30px rgba(173, 216, 230, 0.3);
            animation: glow 3s ease-in-out infinite alternate;
        }}
        
        @keyframes glow {{
            from {{ text-shadow: 0 0 20px rgba(173, 216, 230, 0.3); }}
            to {{ text-shadow: 0 0 30px rgba(255, 182, 193, 0.4), 
                         0 0 40px rgba(152, 251, 152, 0.3); }}
        }}
        
        .subtitle {{
            font-size: 1.2em;
            color: #b0b0ff;
            margin-bottom: 20px;
            opacity: 0;
            animation: fadeIn 1s ease-out 0.5s forwards;
        }}
        
        /* Health Score */
        .health-score {{
            display: inline-block;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.4em;
            font-weight: bold;
            margin: 20px 0;
            background: linear-gradient(45deg, 
                {get_health_color(health_score)[0]}, 
                {get_health_color(health_score)[1]});
            color: white;
            transform: scale(0);
            animation: popIn 0.6s ease-out 1s forwards;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        }}
        
        @keyframes popIn {{
            0% {{ transform: scale(0); opacity: 0; }}
            70% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        
        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .metric-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            opacity: 0;
            transform: translateY(20px);
            animation: slideUp 0.5s ease forwards;
        }}
        
        .metric-card:nth-child(1) {{ animation-delay: 0.2s; }}
        .metric-card:nth-child(2) {{ animation-delay: 0.4s; }}
        .metric-card:nth-child(3) {{ animation-delay: 0.6s; }}
        .metric-card:nth-child(4) {{ animation-delay: 0.8s; }}
        
        @keyframes slideUp {{
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            border-color: rgba(173, 216, 230, 0.3);
        }}
        
        .metric-icon {{
            font-size: 2em;
            margin-bottom: 15px;
            color: #add8e6;
        }}
        
        /* System Info Cards */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .info-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            opacity: 0;
            animation: fadeInUp 0.5s ease forwards;
        }}
        
        .info-card:nth-child(1) {{ animation-delay: 0.3s; }}
        .info-card:nth-child(2) {{ animation-delay: 0.5s; }}
        .info-card:nth-child(3) {{ animation-delay: 0.7s; }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Lofi Player */
        .lofi-player {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px;
            width: 300px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transform: translateY(100px);
            animation: slideUpPlayer 1s ease-out 2s forwards;
        }}
        
        @keyframes slideUpPlayer {{
            to {{ transform: translateY(0); }}
        }}
        
        .player-controls {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-top: 10px;
        }}
        
        .control-btn {{
            background: transparent;
            border: none;
            color: #add8e6;
            font-size: 1.2em;
            cursor: pointer;
            transition: color 0.3s ease;
            padding: 8px;
            border-radius: 50%;
        }}
        
        .control-btn:hover {{
            color: #ffb6c1;
            background: rgba(255, 255, 255, 0.1);
        }}
        
        /* Visualizer */
        .visualizer {{
            display: flex;
            align-items: flex-end;
            height: 40px;
            gap: 3px;
            margin-top: 10px;
        }}
        
        .bar {{
            width: 4px;
            background: linear-gradient(to top, #add8e6, #ffb6c1);
            border-radius: 2px;
            animation: visualize 1.5s ease-in-out infinite;
        }}
        
        .bar:nth-child(2) {{ animation-delay: 0.1s; }}
        .bar:nth-child(3) {{ animation-delay: 0.2s; }}
        .bar:nth-child(4) {{ animation-delay: 0.3s; }}
        .bar:nth-child(5) {{ animation-delay: 0.4s; }}
        
        @keyframes visualize {{
            0%, 100% {{ height: 5px; }}
            50% {{ height: 40px; }}
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 30px;
            margin-top: 50px;
            color: #8888cc;
            font-size: 0.9em;
            opacity: 0;
            animation: fadeIn 1s ease-out 1.5s forwards;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        @keyframes fadeIn {{
            to {{ opacity: 1; }}
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .lofi-player {{
                position: relative;
                bottom: auto;
                right: auto;
                width: 100%;
                margin-top: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="lofi-bg"></div>
    <div class="floating-elements">
        <div class="floating-element" style="width: 100px; height: 100px; top: 10%; left: 10%;"></div>
        <div class="floating-element" style="width: 60px; height: 60px; top: 60%; left: 80%;"></div>
        <div class="floating-element" style="width: 80px; height: 80px; top: 80%; left: 20%;"></div>
    </div>
    <div class="scan-line"></div>
    
    <div class="container">
        <div class="header">
            <div class="header-content">
                <h1><i class="fas fa-laptop-code"></i> SYSTEM SCAN REPORT</h1>
                <p class="subtitle">Lofi Edition | {datetime.now().strftime('%B %d, %Y')}</p>
                
                <div class="health-score">
                    <i class="fas fa-heartbeat"></i> System Health: {health_score}/100
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-icon"><i class="fas fa-microchip"></i></div>
                        <h3>CPU Usage</h3>
                        <p>{psutil.cpu_percent()}%</p>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon"><i class="fas fa-memory"></i></div>
                        <h3>Memory</h3>
                        <p>{psutil.virtual_memory().percent}% used</p>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon"><i class="fas fa-hdd"></i></div>
                        <h3>Storage</h3>
                        <p>{len(psutil.disk_partitions())} drives</p>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon"><i class="fas fa-network-wired"></i></div>
                        <h3>Network</h3>
                        <p>{len(psutil.net_if_addrs())} interfaces</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="info-grid">
            <div class="info-card">
                <h3><i class="fas fa-info-circle"></i> System Info</h3>
                <p><strong>Host:</strong> {socket.gethostname()}</p>
                <p><strong>OS:</strong> {platform.platform()}</p>
                <p><strong>Architecture:</strong> {platform.architecture()[0]}</p>
                <p><strong>Processor:</strong> {platform.processor()}</p>
            </div>
            
            <div class="info-card">
                <h3><i class="fas fa-chart-line"></i> Performance</h3>
                <p><strong>Boot Time:</strong> {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M')}</p>
                <p><strong>Processes:</strong> {len(psutil.pids())}</p>
                <p><strong>CPU Cores:</strong> {psutil.cpu_count()} ({psutil.cpu_count(logical=False)} physical)</p>
            </div>
            
            <div class="info-card">
                <h3><i class="fas fa-shield-alt"></i> Security</h3>
                <p><strong>Health Score:</strong> {health_score}/100</p>
                <p><strong>Scan Time:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
                <p><strong>Scanner Version:</strong> 3.0 Lofi Edition</p>
            </div>
        </div>
    </div>
    
    <!-- Lofi Music Player -->
    <div class="lofi-player">
        <h4><i class="fas fa-headphones"></i> Lofi Beats</h4>
        <p>Chill vibes for system analysis</p>
        
        <div class="visualizer">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        
        <div class="player-controls">
            <button class="control-btn" onclick="skipTrack(-1)"><i class="fas fa-step-backward"></i></button>
            <button class="control-btn" onclick="togglePlay()"><i class="fas fa-play" id="playBtn"></i></button>
            <button class="control-btn" onclick="skipTrack(1)"><i class="fas fa-step-forward"></i></button>
            <span style="flex: 1; text-align: center;" id="trackName">Study Session • Lofi</span>
            <button class="control-btn" onclick="toggleMute()"><i class="fas fa-volume-up" id="volumeBtn"></i></button>
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by SABARI425 System Scanner • Lofi Edition v3.0</p>
        <p><i class="fas fa-heart"></i> Made with care for your system's health</p>
        <p>Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <script>
        // Lofi Player Functionality
        let isPlaying = false;
        let isMuted = false;
        const tracks = [
            "Study Session • Lofi",
            "Coffee Shop • Chill",
            "Rainy Day • Beats",
            "Night Drive • Vibes"
        ];
        let currentTrack = 0;
        
        function togglePlay() {{
            isPlaying = !isPlaying;
            const btn = document.getElementById('playBtn');
            btn.classList.toggle('fa-play');
            btn.classList.toggle('fa-pause');
            
            // Animate visualizer bars
            const bars = document.querySelectorAll('.bar');
            bars.forEach(bar => {{
                bar.style.animationPlayState = isPlaying ? 'running' : 'paused';
            }});
        }}
        
        function toggleMute() {{
            isMuted = !isMuted;
            const btn = document.getElementById('volumeBtn');
            btn.classList.toggle('fa-volume-up');
            btn.classList.toggle('fa-volume-mute');
        }}
        
        function skipTrack(direction) {{
            currentTrack = (currentTrack + direction + tracks.length) % tracks.length;
            document.getElementById('trackName').textContent = tracks[currentTrack];
        }}
        
        // Auto-scroll animations
        let scrollTimeout;
        window.addEventListener('scroll', () => {{
            clearTimeout(scrollTimeout);
            document.body.classList.add('scrolling');
            scrollTimeout = setTimeout(() => {{
                document.body.classList.remove('scrolling');
            }}, 100);
        }});
        
        // Floating elements interaction
        document.querySelectorAll('.floating-element').forEach(el => {{
            el.addEventListener('mouseenter', () => {{
                el.style.animationDuration = '30s';
            }});
            el.addEventListener('mouseleave', () => {{
                el.style.animationDuration = '15s';
            }});
        }});
        
        // Initialize animations
        document.addEventListener('DOMContentLoaded', () => {{
            // Staggered animation for metrics
            const cards = document.querySelectorAll('.metric-card, .info-card');
            cards.forEach((card, index) => {{
                setTimeout(() => {{
                    card.style.animation = 'fadeInUp 0.5s ease forwards';
                }}, 100 * index);
            }});
            
            // Continuous scan line
            setInterval(() => {{
                const scanLine = document.querySelector('.scan-line');
                scanLine.style.animation = 'none';
                setTimeout(() => {{
                    scanLine.style.animation = 'scan 3s ease-in-out infinite';
                }}, 10);
            }}, 3000);
        }});
    </script>
</body>
</html>'''
    
    # Save the HTML file
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    filename = f"System_Scan_Lofi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(downloads, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath, health_score


def get_health_color(score):
    """Return gradient colors based on health score"""
    if score >= 80:
        return ["#00ff88", "#00cc66"]  # Green gradient
    elif score >= 60:
        return ["#ffdd00", "#ffaa00"]  # Yellow/Orange gradient
    else:
        return ["#ff4444", "#cc0000"]  # Red gradient


# -------------------------------------------------------------------
#  MAIN EXECUTION WITH ENHANCED UI
# -------------------------------------------------------------------
def main():
    """Main function with enhanced user experience"""
    try:
        # Check password
        if not check_password():
            print_colored("\n   Exiting system...", Colors.RED)
            time.sleep(2)
            return
        
        # Clear screen and show welcome
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        
        # Start scanning
        print_colored("\n" + "═" * 60, Colors.LOFI_PURPLE)
        print_colored("   🚀  STARTING SYSTEM SCAN", Colors.LOFI_PINK, "bold")
        print_colored("═" * 60, Colors.LOFI_PURPLE)
        
        # Generate report
        print_colored("\n   Generating Lofi-style report...", Colors.LOFI_BLUE)
        time.sleep(1)
        
        report_path, health_score = generate_html_report()
        
        # Display results
        print_colored("\n" + "═" * 60, Colors.LOFI_PURPLE)
        print_colored("   📊  SCAN RESULTS", Colors.LOFI_GREEN, "bold")
        print_colored("═" * 60, Colors.LOFI_PURPLE)
        
        print_colored(f"\n   📍  Report saved to:", Colors.LOFI_BLUE)
        print_colored(f"      {report_path}", Colors.WHITE)
        
        print_colored(f"\n   ❤️  System Health Score:", Colors.LOFI_PINK)
        health_color = Colors.LOFI_GREEN if health_score >= 80 else \
                      Colors.YELLOW if health_score >= 60 else Colors.RED
        print_colored(f"      {health_score}/100", health_color, "bold")
        
        print_colored("\n   🎵  Opening in browser...", Colors.LOFI_TEAL)
        time.sleep(1)
        
        # Open in browser
        try:
            webbrowser.open(f'file://{report_path}')
            print_colored("   ✓  Browser opened successfully", Colors.LOFI_GREEN)
        except:
            print_colored("   ⚠  Could not open browser automatically", Colors.YELLOW)
            print_colored(f"   📂  Please open manually: {report_path}", Colors.WHITE)
        
        # Final message
        print_colored("\n" + "═" * 60, Colors.LOFI_PURPLE)
        print_colored("   🎉  SCAN COMPLETED SUCCESSFULLY!", Colors.LOFI_GREEN, "bold")
        print_colored("═" * 60, Colors.LOFI_PURPLE)
        
        print_colored("\n   Thank you for using SABARI425 System Scanner!", Colors.LOFI_BLUE)
        print_colored("   Lofi Edition v3.0", Colors.LOFI_PURPLE, "italic")
        print_colored("\n   Press Enter to exit...", Colors.WHITE)
        input()
        
    except KeyboardInterrupt:
        print_colored("\n\n   ⚠  Scan interrupted by user", Colors.YELLOW)
    except Exception as e:
        print_colored(f"\n   ✗  Error: {str(e)}", Colors.RED)
        print_colored("   Please try again or check permissions", Colors.YELLOW)
    finally:
        print_colored("\n   Goodbye! 👋", Colors.LOFI_PURPLE)
        time.sleep(1)


if __name__ == "__main__":
    main()
