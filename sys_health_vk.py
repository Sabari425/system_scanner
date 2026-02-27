#!/usr/bin/env python3
"""
SYSTEM VIBE - Advanced Penetration Sequence Simulation
Version: 4.5 Enhanced
Author: System Vibe
Description: A dramatic hacking simulation with visual effects
"""

import os
import sys
import time
import random
import subprocess
import urllib.request
import importlib
import platform
from typing import Optional, Tuple, List

# ==================== AUTO MODULE INSTALLER ====================

REQUIRED_MODULES = {
    'PIL': 'pillow',
    'tkinter': None,  # Usually built-in
    'ctypes': None,   # Built-in
    'win32gui': 'pywin32',  # For Windows-specific features
    'win32con': 'pywin32',
    'win32api': 'pywin32'
}

def install_missing_modules():
    """Automatically install required Python modules"""
    missing_modules = []
    
    print("\033[1;93m[*] Checking required modules...\033[0m")
    
    for module_name, pip_name in REQUIRED_MODULES.items():
        if pip_name:  # Only check modules that need installation
            try:
                importlib.import_module(module_name)
                print(f"\033[1;92m[✓] {module_name} is installed\033[0m")
            except ImportError:
                missing_modules.append(pip_name)
                print(f"\033[1;91m[✗] {module_name} not found\033[0m")
    
    if missing_modules:
        print(f"\033[1;93m[*] Installing missing modules: {', '.join(missing_modules)}\033[0m")
        for module in missing_modules:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', module])
                print(f"\033[1;92m[✓] Installed {module}\033[0m")
            except subprocess.CalledProcessError as e:
                print(f"\033[1;91m[✗] Failed to install {module}: {e}\033[0m")
                print(f"\033[1;93m[*] Please install manually: pip install {module}\033[0m")
        
        print("\033[1;92m[*] Module installation complete. Restarting script...\033[0m")
        time.sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        print("\033[1;92m[✓] All required modules are present\033[0m")
        time.sleep(1)

# Install missing modules before importing
install_missing_modules()

# Now import all required modules
from PIL import Image, ImageEnhance, ImageFilter
import tkinter as tk
from tkinter import Label, messagebox
from PIL import ImageTk
import ctypes

# Windows-specific imports (will work only on Windows)
IS_WINDOWS = os.name == 'nt'
if IS_WINDOWS:
    try:
        import win32gui
        import win32con
        import win32api
    except ImportError:
        print("\033[1;93m[!] pywin32 not fully loaded. Some Windows features may be limited.\033[0m")

# ==================== CONFIGURATION ====================

class Config:
    """Configuration settings for the script"""
    IMAGE_ZOOM_PERCENT = 120  # Default zoom for image display
    IMAGE_DISPLAY_TIME = 3000  # Milliseconds to show image
    HACKING_STEPS = 53  # Number of steps in sequence
    SCAN_STEPS = 20  # Steps in scan progress
    RESTART_DELAY = 3  # Seconds before restart
    GITHUB_IMAGE_URL = "https://github.com/Sabari425/Others-Projects/blob/main/vk.png"
    
    # Speed settings (all delays in seconds)
    STEP_DELAY_FAST = 0.02
    STEP_DELAY_NORMAL = 0.1
    STEP_DELAY_SLOW = 0.4
    SCAN_DELAY = 0.02

# ==================== COLOR CLASS ====================

class Colors:
    """ANSI color codes for terminal output"""
    R = '\033[1;91m'     # Bright Red
    G = '\033[1;92m'     # Bright Green
    Y = '\033[1;93m'     # Bright Yellow
    B = '\033[1;94m'     # Bright Blue
    P = '\033[1;95m'     # Bright Purple
    C = '\033[1;96m'     # Bright Cyan
    W = '\033[1;97m'     # Bright White
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Apply color to text"""
        return f"{color}{text}{cls.END}"

# ==================== UTILITY FUNCTIONS ====================

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if IS_WINDOWS else 'clear')

def print_unicode_safe(text: str, color: str = Colors.W, end: str = '\n'):
    """Print text safely handling Unicode characters"""
    try:
        # Try to encode in utf-8, fallback to ascii if needed
        safe_text = text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
        print(f"{color}{safe_text}{Colors.END}", end=end)
    except:
        # Ultimate fallback
        print(f"{color}[Text Display Error]{Colors.END}", end=end)

def fast_print(text: str, color: str = Colors.C, delay: float = Config.STEP_DELAY_FAST):
    """Print with delay for dramatic effect"""
    print_unicode_safe(text, color)
    time.sleep(delay)

def slow_print(text: str, color: str = Colors.R, delay: float = Config.STEP_DELAY_SLOW):
    """Print with slower delay for emphasis"""
    print_unicode_safe(text, color)
    time.sleep(delay)

def center_text(text: str, width: int = 80) -> str:
    """Center text for box drawing"""
    return text.center(width)

def draw_box(title: str, color: str = Colors.R, width: int = 60):
    """Draw a decorative box around text"""
    print(f"{color}┌{'─' * width}┐{Colors.END}")
    print(f"{color}│{center_text(title, width)}│{Colors.END}")
    print(f"{color}└{'─' * width}┘{Colors.END}")

# ==================== IMAGE HANDLING ====================

def download_image_from_github(github_url: str, save_filename: Optional[str] = None) -> Optional[str]:
    """Download an image from GitHub raw URL"""
    # Convert GitHub URL to raw URL
    if 'github.com' in github_url and '/blob/' in github_url:
        raw_url = github_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        print(f"{Colors.Y}Converted to raw URL: {raw_url}{Colors.END}")
    else:
        raw_url = github_url
    
    if not save_filename:
        save_filename = 'hacker_image.jpg'
    
    download_path = os.path.join(os.environ['TEMP'], save_filename)
    
    try:
        print(f"{Colors.C}[*] Downloading from GitHub...{Colors.END}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
        }
        req = urllib.request.Request(raw_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(download_path, 'wb') as out_file:
                out_file.write(response.read())
        
        if os.path.exists(download_path) and os.path.getsize(download_path) > 0:
            file_size = os.path.getsize(download_path) / 1024
            print(f"{Colors.G}[✓] Download successful! ({file_size:.2f} KB){Colors.END}")
            return download_path
        else:
            print(f"{Colors.R}[✗] Downloaded file is empty{Colors.END}")
            return None
            
    except urllib.error.HTTPError as e:
        print(f"{Colors.R}[✗] HTTP Error {e.code}: {e.reason}{Colors.END}")
        if e.code == 404:
            print(f"{Colors.Y}[!] File not found. Trying alternative URL...{Colors.END}")
            # Try with .jpg extension instead of .png
            alt_url = github_url.replace('.png', '.jpg')
            if alt_url != github_url:
                return download_image_from_github(alt_url, save_filename)
        return None
    except Exception as e:
        print(f"{Colors.R}[✗] Download failed: {e}{Colors.END}")
        return None

def enhance_image(image_path: str, zoom_percent: int) -> Image.Image:
    """Apply enhancements to the image for better display"""
    img = Image.open(image_path)
    
    # Enhance contrast and sharpness for better visibility
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.1)
    
    return img

def show_image_fullscreen_zoom(image_path: str, zoom_percent: int = Config.IMAGE_ZOOM_PERCENT) -> bool:
    """Display image in full screen with specified zoom percentage"""
    try:
        # Create fullscreen window
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.configure(bg='black')
        root.title("SYSTEM BREACH - HACKER DETECTED")
        
        # Set window to stay on top
        root.attributes('-topmost', True)
        
        # Load and enhance image
        pil_image = enhance_image(image_path, zoom_percent)
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate zoomed dimensions
        original_width, original_height = pil_image.size
        zoomed_width = int(original_width * zoom_percent / 100)
        zoomed_height = int(original_height * zoom_percent / 100)
        
        # Ensure image doesn't exceed screen bounds
        if zoomed_width > screen_width or zoomed_height > screen_height:
            ratio = min(screen_width/zoomed_width, screen_height/zoomed_height)
            zoomed_width = int(zoomed_width * ratio)
            zoomed_height = int(zoomed_height * ratio)
        
        # Resize image with high quality
        pil_image = pil_image.resize((zoomed_width, zoomed_height), Image.Resampling.LANCZOS)
        
        # Calculate position to center the zoomed image
        x_position = (screen_width - zoomed_width) // 2
        y_position = (screen_height - zoomed_height) // 2
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(pil_image)
        
        # Create label with image
        label = Label(root, image=photo, bg='black')
        label.place(x=x_position, y=y_position)
        
        # Add subtle glow effect with a secondary semi-transparent window
        # (optional enhancement)
        
        # Bind escape key to close
        root.bind('<Escape>', lambda e: root.quit())
        root.bind('<q>', lambda e: root.quit())
        root.bind('<Q>', lambda e: root.quit())
        
        # Auto close after specified time
        root.after(Config.IMAGE_DISPLAY_TIME, root.quit)
        
        print(f"{Colors.G}[✓] Image displayed in full screen at {zoom_percent}% zoom{Colors.END}")
        print(f"{Colors.Y}[i] Image will close automatically in {Config.IMAGE_DISPLAY_TIME//1000} seconds{Colors.END}")
        print(f"{Colors.Y}[i] Press ESC or Q to close manually{Colors.END}")
        
        root.mainloop()
        root.destroy()
        return True
        
    except Exception as e:
        print(f"{Colors.R}[✗] Failed to display image: {e}{Colors.END}")
        return False

def show_image_with_powershell(image_path: str, zoom: int = Config.IMAGE_ZOOM_PERCENT) -> bool:
    """Alternative method using PowerShell (Windows only)"""
    if not IS_WINDOWS:
        return False
        
    try:
        ps_script = f"""
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        
        $img = [System.Drawing.Image]::FromFile('{image_path}')
        $form = New-Object System.Windows.Forms.Form
        $form.WindowState = 'Maximized'
        $form.FormBorderStyle = 'None'
        $form.TopMost = $true
        $form.BackColor = 'Black'
        $form.Text = 'SYSTEM BREACH - HACKER DETECTED'
        
        $pictureBox = New-Object System.Windows.Forms.PictureBox
        $pictureBox.Dock = 'Fill'
        $pictureBox.SizeMode = 'Zoom'
        $pictureBox.Image = $img
        $form.Controls.Add($pictureBox)
        
        $form.Add_KeyDown({{ 
            if ($_.KeyCode -eq 'Escape' -or $_.KeyCode -eq 'Q') {{ 
                $form.Close() 
            }} 
        }})
        
        $timer = New-Object System.Windows.Forms.Timer
        $timer.Interval = {Config.IMAGE_DISPLAY_TIME}
        $timer.Add_Tick({{ $form.Close() }})
        $timer.Start()
        
        [System.Windows.Forms.Application]::Run($form)
        """
        
        ps_command = ['powershell', '-WindowStyle', 'Hidden', '-Command', ps_script]
        subprocess.Popen(ps_command, shell=True)
        return True
    except Exception as e:
        print(f"{Colors.R}[✗] PowerShell method failed: {e}{Colors.END}")
        return False

def show_hacker_art():
    """Display enhanced ASCII hacker art as fallback"""
    art = f"""
{Colors.R}
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║     ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗ ║
    ║     ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ║
    ║     ███████║███████║██║     █████╔╝ █████╗   ║
    ║     ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝   ║
    ║     ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗ ║
    ║     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ║
    ║                                               ║
    ║              {Colors.Y}⚠  IN THE SYSTEM  ╚╝  WATCHING  ⚠{Colors.R}           ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
{Colors.END}
"""
    print(art)
    time.sleep(Config.IMAGE_DISPLAY_TIME // 1000)

# ==================== HACKING SEQUENCE ====================

def get_hacking_steps() -> List[Tuple[str, str, float]]:
    """Generate the list of hacking steps with colors and delays"""
    steps = [
        # Reconnaissance Phase (1-8)
        ("[1/53] Scanning network ranges...", Colors.C, Config.STEP_DELAY_FAST),
        ("[2/53] Identifying live hosts...", Colors.C, Config.STEP_DELAY_FAST),
        ("[3/53] Detecting operating systems...", Colors.C, Config.STEP_DELAY_FAST),
        ("[4/53] Mapping open ports...", Colors.C, Config.STEP_DELAY_FAST),
        ("[5/53] Fingerprinting services...", Colors.C, Config.STEP_DELAY_FAST),
        ("[6/53] Enumerating users...", Colors.Y, Config.STEP_DELAY_FAST),
        ("[7/53] Gathering system information...", Colors.Y, Config.STEP_DELAY_FAST),
        ("[8/53] Analyzing security posture...", Colors.Y, Config.STEP_DELAY_FAST),
        
        # Vulnerability Analysis (9-16)
        ("[9/53] Scanning for known CVEs...", Colors.Y, Config.STEP_DELAY_FAST),
        ("[10/53] Testing for weak credentials...", Colors.Y, Config.STEP_DELAY_FAST),
        ("[11/53] Checking for misconfigurations...", Colors.Y, Config.STEP_DELAY_FAST),
        ("[12/53] Analyzing service versions...", Colors.Y, Config.STEP_DELAY_FAST),
        ("[13/53] Searching for exploits...", Colors.P, Config.STEP_DELAY_FAST),
        ("[14/53] Prioritizing vulnerabilities...", Colors.P, Config.STEP_DELAY_FAST),
        ("[15/53] Preparing exploit chain...", Colors.P, Config.STEP_DELAY_FAST),
        ("[16/53] Validating attack vectors...", Colors.P, Config.STEP_DELAY_FAST),
        
        # Exploitation Phase (17-26)
        ("[17/53] Bypassing firewall rules...", Colors.R, Config.STEP_DELAY_FAST),
        ("[18/53] Circumventing IDS/IPS...", Colors.R, Config.STEP_DELAY_FAST),
        ("[19/53] Injecting shellcode...", Colors.R, Config.STEP_DELAY_FAST),
        ("[20/53] Establishing reverse shell...", Colors.R, Config.STEP_DELAY_FAST),
        ("[21/53] Escalating privileges...", Colors.R, Config.STEP_DELAY_FAST),
        ("[22/53] Dumping password hashes...", Colors.R, Config.STEP_DELAY_FAST),
        ("[23/53] Cracking credentials...", Colors.R, Config.STEP_DELAY_FAST),
        ("[24/53] Accessing SAM database...", Colors.R, Config.STEP_DELAY_FAST),
        ("[25/53] Retrieving domain admin...", Colors.R, Config.STEP_DELAY_FAST),
        ("[26/53] Patching kernel vulnerabilities...", Colors.R, Config.STEP_DELAY_FAST),
        
        # Persistence (27-34)
        ("[27/53] Installing backdoor...", Colors.P, Config.STEP_DELAY_FAST),
        ("[28/53] Creating hidden user...", Colors.P, Config.STEP_DELAY_FAST),
        ("[29/53] Modifying registry...", Colors.P, Config.STEP_DELAY_FAST),
        ("[30/53] Adding startup entries...", Colors.P, Config.STEP_DELAY_FAST),
        ("[31/53] Deploying rootkit...", Colors.P, Config.STEP_DELAY_FAST),
        ("[32/53] Hiding processes...", Colors.P, Config.STEP_DELAY_FAST),
        ("[33/53] Clearing event logs...", Colors.P, Config.STEP_DELAY_FAST),
        ("[34/53] Disabling security tools...", Colors.P, Config.STEP_DELAY_FAST),
        
        # Data Extraction (35-43)
        ("[35/53] Locating sensitive files...", Colors.C, Config.STEP_DELAY_FAST),
        ("[36/53] Extracting browser data...", Colors.C, Config.STEP_DELAY_FAST),
        ("[37/53] Dumping credentials...", Colors.C, Config.STEP_DELAY_FAST),
        ("[38/53] Accessing email databases...", Colors.C, Config.STEP_DELAY_FAST),
        ("[39/53] Stealing SSH keys...", Colors.C, Config.STEP_DELAY_FAST),
        ("[40/53] Copying documents...", Colors.C, Config.STEP_DELAY_FAST),
        ("[41/53] Compressing stolen data...", Colors.C, Config.STEP_DELAY_FAST),
        ("[42/53] Encrypting exfiltration...", Colors.C, Config.STEP_DELAY_FAST),
        ("[43/53] Uploading to remote server...", Colors.C, Config.STEP_DELAY_FAST),
        
        # System Manipulation (44-50)
        ("[44/53] Disabling recovery options...", Colors.Y, Config.STEP_DELAY_FAST),
        ("[45/53] Modifying system files...", Colors.Y, Config.STEP_DELAY_FAST),
        ("[46/53] Installing ransomware module...", Colors.R, Config.STEP_DELAY_FAST),
        ("[47/53] Encrypting user files...", Colors.R, Config.STEP_DELAY_FAST),
        ("[48/53] Creating ransom note...", Colors.R, Config.STEP_DELAY_FAST),
        ("[49/53] Covering digital tracks...", Colors.R, Config.STEP_DELAY_FAST),
        ("[50/53] Finalizing system takeover...", Colors.R, Config.STEP_DELAY_FAST),
        
        # Bonus steps (51-53)
        ("[51/53] Establishing C2 channel...", Colors.B, Config.STEP_DELAY_FAST),
        ("[52/53] Deploying payload...", Colors.B, Config.STEP_DELAY_FAST),
        ("[53/53] Complete system compromise...", Colors.B, Config.STEP_DELAY_SLOW),
    ]
    return steps

def run_hacking_sequence():
    """Execute the hacking step sequence"""
    steps = get_hacking_steps()
    
    for step_text, color, delay in steps:
        print_unicode_safe(step_text, color)
        time.sleep(delay)
        
        # Randomly show additional processing details
        if random.random() > 0.7:
            fast_print(f"  └─ Processing: {hex(random.randint(0x1000, 0xFFFF))}", Colors.G)

def run_system_scan():
    """Display a fake system scan with progress bar"""
    print(f"\n{Colors.Y}Running full system diagnostic...{Colors.END}")
    for i in range(Config.SCAN_STEPS + 1):
        progress = "█" * i + "░" * (Config.SCAN_STEPS - i)
        percentage = i * 5
        print(f"  {Colors.C}[{progress}] {percentage}%{Colors.END}", end="\r")
        time.sleep(Config.SCAN_DELAY)
    print()

def show_compromised_warning():
    """Display the system compromised warning"""
    clear_screen()
    print(f"{Colors.R}{Colors.BOLD}")
    print("┌" + "─" * 60 + "┐")
    print("│" + " " * 60 + "│")
    print("│" + " " * 12 + "⚠  SYSTEM SUCCESSFULLY HACKED  ⚠" + " " * 13 + "│")
    print("│" + " " * 60 + "│")
    print("│" + " " * 10 + "   Full administrative access granted" + " " * 13 + "│")
    print("│" + " " * 12 + "   Remote control established" + " " * 19 + "│")
    print("│" + " " * 14 + "   All data compromised" + " " * 22 + "│")
    print("│" + " " * 60 + "│")
    print("└" + "─" * 60 + "┘")
    print(f"{Colors.END}")
    time.sleep(2)

def show_restart_countdown():
    """Display restart countdown with color effects"""
    print(f"\n{Colors.R}{Colors.BOLD}")
    print("┌" + "─" * 60 + "┐")
    print("│" + " " * 15 + "SYSTEM RESTART INITIATED" + " " * 16 + "│")
    print("│" + " " * 18 + "DATA LOST" + " " * 31 + "│")
    print("└" + "─" * 60 + "┘")
    print(f"{Colors.END}")
    
    for i in range(Config.RESTART_DELAY, 0, -1):
        if i <= 2:
            color = Colors.R
        elif i <= 4:
            color = Colors.Y
        else:
            color = Colors.G
        print(f"{color}Restarting in {i} seconds...{Colors.END}")
        time.sleep(1)

def restart_system():
    """Restart the computer"""
    print(f"\n{Colors.R}⚠  SYSTEM REBOOTING NOW  ⚠{Colors.END}")
    time.sleep(1)
    
    if IS_WINDOWS:
        os.system('shutdown /r /t 0 /c "System compromised - Rebooting"')
    else:
        os.system('sudo reboot')

# ==================== MAIN FUNCTION ====================

def main():
    """Main execution function"""
    try:
        # Check if running with appropriate permissions
        if IS_WINDOWS:
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                print(f"{Colors.Y}[!] Running without admin privileges. Some features may be limited.{Colors.END}")
                time.sleep(2)
        
        clear_screen()
        
        # Display title
        title = "ADVANCED PENETRATION SEQUENCE"
        subtitle = "SYSTEM BREACH v4.5 ENHANCED"
        print(f"{Colors.R}{Colors.BOLD}")
        print("┌" + "─" * 60 + "┐")
        print(f"│{center_text(title, 60)}│")
        print(f"│{center_text(subtitle, 60)}│")
        print("└" + "─" * 60 + "┘")
        print(f"{Colors.END}")
        time.sleep(2)

        # Run hacking sequence
        run_hacking_sequence()
        
        # Run system scan
        run_system_scan()
        
        # Show compromised warning
        show_compromised_warning()

        # Download and display image
        print(f"{Colors.Y}Downloading hacker image...{Colors.END}")
        img_path = download_image_from_github(Config.GITHUB_IMAGE_URL)
        
        if img_path:
            print(f"{Colors.G}Image downloaded. Displaying in full screen...{Colors.END}")
            
            # Try primary method
            success = show_image_fullscreen_zoom(img_path, Config.IMAGE_ZOOM_PERCENT)
            
            # Try fallback method if primary fails
            if not success and IS_WINDOWS:
                success = show_image_with_powershell(img_path, Config.IMAGE_ZOOM_PERCent)
            
            if not success:
                print(f"{Colors.R}Could not display image. Showing ASCII art instead.{Colors.END}")
                show_hacker_art()
        else:
            print(f"{Colors.R}Could not download image. Showing ASCII art.{Colors.END}")
            show_hacker_art()
        
        # Show restart countdown
        show_restart_countdown()
        
        # Restart system
        restart_system()
            
    except KeyboardInterrupt:
        print(f"\n{Colors.G}Hack sequence aborted. System remains safe.{Colors.END}")
        time.sleep(2)
    except Exception as e:
        print(f"\n{Colors.R}Unexpected error: {e}{Colors.END}")
        time.sleep(3)

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    # Display startup message
    print(f"{Colors.C}Initializing System Vibe Enhanced Edition...{Colors.END}")
    time.sleep(1)
    
    # Run main function
    main()