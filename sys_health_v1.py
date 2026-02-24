import os
import time
import random
import subprocess
import urllib.request
import ctypes
import win32gui
import win32con
import win32api
from PIL import Image
import tkinter as tk
from tkinter import Label
from PIL import ImageTk

# Colors configuration
class Colors:
    R = '\033[1;91m'     # Bright Red
    G = '\033[1;92m'     # Bright Green
    Y = '\033[1;93m'     # Bright Yellow
    B = '\033[1;94m'     # Bright Blue
    P = '\033[1;94m'     # Bright Purple
    C = '\033[1;96m'     # Bright Cyan
    W = '\033[1;97m'     # Bright White
    END = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fast_print(text, color=Colors.C, delay=0.02):
    print(f"{color}{text}{Colors.END}")
    time.sleep(delay)

def download_image_from_github(github_url, save_filename=None):
    """Download an image from GitHub raw URL"""
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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(raw_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(download_path, 'wb') as out_file:
                out_file.write(response.read())
        
        if os.path.exists(download_path) and os.path.getsize(download_path) > 0:
            print(f"{Colors.G}[✓] Download successful!{Colors.END}")
            return download_path
        else:
            return None
    except Exception as e:
        print(f"{Colors.R}[✗] Download failed: {e}{Colors.END}")
        return None

def show_image_fullscreen_zoom(image_path, zoom_percent=260):
    """
    Display image in full screen with specified zoom percentage
    Using Tkinter for maximum control
    """
    try:
        # Create fullscreen window
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.configure(bg='black')
        
        # Load and process image
        pil_image = Image.open(image_path)
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate zoomed dimensions (260% of original)
        original_width, original_height = pil_image.size
        zoomed_width = int(original_width * zoom_percent / 100)
        zoomed_height = int(original_height * zoom_percent / 100)
        
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
        
        # Bind escape key to close
        root.bind('<Escape>', lambda e: root.quit())
        
        # Auto close after 3 seconds
        root.after(3000, root.quit)
        
        print(f"{Colors.G}[✓] Image displayed in full screen at {zoom_percent}% zoom{Colors.END}")
        print(f"{Colors.Y}[i] Image will close automatically in 3 seconds{Colors.END}")
        print(f"{Colors.Y}[i] Press ESC to close manually{Colors.END}")
        
        root.mainloop()
        root.destroy()
        return True
        
    except Exception as e:
        print(f"{Colors.R}[✗] Failed to display image: {e}{Colors.END}")
        return False

def show_image_with_irfanview(image_path, zoom=260):
    """Method 2: Using IrfanView if installed (best for zoom control)"""
    try:
        # Check if IrfanView is installed in common locations
        irfan_paths = [
            r"C:\Program Files\IrfanView\i_view64.exe",
            r"C:\Program Files (x86)\IrfanView\i_view.exe",
            r"C:\Program Files\IrfanView\i_view.exe"
        ]
        
        irfan_path = None
        for path in irfan_paths:
            if os.path.exists(path):
                irfan_path = path
                break
        
        if irfan_path:
            # Open with IrfanView in full screen at specific zoom
            subprocess.run([
                irfan_path, 
                image_path, 
                f"/zoom={zoom}", 
                "/fullscreen", 
                "/hide=7",
                "/close_on_esc"
            ])
            return True
    except:
        pass
    return False

def show_image_with_powershell(image_path, zoom=260):
    """Method 3: Using PowerShell to control Windows Photo app"""
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
        
        $pictureBox = New-Object System.Windows.Forms.PictureBox
        $pictureBox.Dock = 'Fill'
        $pictureBox.SizeMode = 'Zoom'
        $pictureBox.Image = $img
        $form.Controls.Add($pictureBox)
        
        $form.Add_KeyDown({{ if ($_.KeyCode -eq 'Escape') {{ $form.Close() }} }})
        $timer = New-Object System.Windows.Forms.Timer
        $timer.Interval = 5000
        $timer.Add_Tick({{ $form.Close() }})
        $timer.Start()
        
        [System.Windows.Forms.Application]::Run($form)
        """
        
        ps_command = f'powershell -WindowStyle Hidden -Command "{ps_script}"'
        subprocess.Popen(ps_command, shell=True)
        return True
    except:
        return False

def show_hacker_art():
    """Display ASCII hacker art as fallback"""
    print(f"""{Colors.R}
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║     ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗  ║
    ║     ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝  ║
    ║     ███████║███████║██║     █████╔╝ █████╗    ║
    ║     ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝    ║
    ║     ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗  ║
    ║     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝  ║
    ║                                               ║
    ║          IN THE SYSTEM... WATCHING            ║
    ╚═══════════════════════════════════════════════╝
    {Colors.END}""")
    time.sleep(5)

def main():
    try:
        clear_screen()
        
        # Title
        print(f"{Colors.R}{Colors.BOLD}")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║              ADVANCED PENETRATION SEQUENCE                 ║")
        print("║                    SYSTEM BREACH v4.0                      ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        time.sleep(2)

        # 53 hacking steps
        steps = [
            ("[1/53] Scanning network ranges...", Colors.C, 0.02),
            ("[2/53] Identifying live hosts...", Colors.C, 0.02),
            ("[3/53] Detecting operating systems...", Colors.C, 0.02),
            ("[4/53] Mapping open ports...", Colors.C, 0.02),
            ("[5/53] Fingerprinting services...", Colors.C, 0.02),
            ("[6/53] Enumerating users...", Colors.Y, 0.02),
            ("[7/53] Gathering system information...", Colors.Y, 0.02),
            ("[8/53] Analyzing security posture...", Colors.Y, 0.02),
            ("[9/53] Scanning for known CVEs...", Colors.Y, 0.02),
            ("[10/53] Testing for weak credentials...", Colors.Y, 0.02),
            ("[11/53] Checking for misconfigurations...", Colors.Y, 0.02),
            ("[12/53] Analyzing service versions...", Colors.Y, 0.02),
            ("[13/53] Searching for exploits...", Colors.P, 0.02),
            ("[14/53] Prioritizing vulnerabilities...", Colors.P, 0.02),
            ("[15/53] Preparing exploit chain...", Colors.P, 0.02),
            ("[16/53] Validating attack vectors...", Colors.P, 0.02),
            ("[17/53] Bypassing firewall rules...", Colors.R, 0.02),
            ("[18/53] Circumventing IDS/IPS...", Colors.R, 0.02),
            ("[19/53] Injecting shellcode...", Colors.R, 0.02),
            ("[20/53] Establishing reverse shell...", Colors.R, 0.02),
            ("[21/53] Escalating privileges...", Colors.R, 0.02),
            ("[22/53] Dumping password hashes...", Colors.R, 0.02),
            ("[23/53] Cracking credentials...", Colors.R, 0.02),
            ("[24/53] Accessing SAM database...", Colors.R, 0.02),
            ("[25/53] Retrieving domain admin...", Colors.R, 0.02),
            ("[26/53] Patching kernel vulnerabilities...", Colors.R, 0.02),
            ("[27/53] Installing backdoor...", Colors.P, 0.02),
            ("[28/53] Creating hidden user...", Colors.P, 0.02),
            ("[29/53] Modifying registry...", Colors.P, 0.02),
            ("[30/53] Adding startup entries...", Colors.P, 0.02),
            ("[31/53] Deploying rootkit...", Colors.P, 0.02),
            ("[32/53] Hiding processes...", Colors.P, 0.02),
            ("[33/53] Clearing event logs...", Colors.P, 0.02),
            ("[34/53] Disabling security tools...", Colors.P, 0.02),
            ("[35/53] Locating sensitive files...", Colors.C, 0.02),
            ("[36/53] Extracting browser data...", Colors.C, 0.02),
            ("[37/53] Dumping credentials...", Colors.C, 0.02),
            ("[38/53] Accessing email databases...", Colors.C, 0.02),
            ("[39/53] Stealing SSH keys...", Colors.C, 0.02),
            ("[40/53] Copying documents...", Colors.C, 0.02),
            ("[41/53] Compressing stolen data...", Colors.C, 0.02),
            ("[42/53] Encrypting exfiltration...", Colors.C, 0.02),
            ("[43/53] Uploading to remote server...", Colors.C, 0.02),
            ("[44/53] Disabling recovery options...", Colors.Y, 0.02),
            ("[45/53] Modifying system files...", Colors.Y, 0.02),
            ("[46/53] Installing ransomware module...", Colors.R, 0.02),
            ("[47/53] Encrypting user files...", Colors.R, 0.02),
            ("[48/53] Creating ransom note...", Colors.R, 0.02),
            ("[49/53] Covering digital tracks...", Colors.R, 0.02),
            ("[50/53] Finalizing system takeover...", Colors.R, 0.02),
            ("[51/53] Establishing C2 channel...", Colors.B, 0.02),
            ("[52/53] Deploying payload...", Colors.B, 0.02),
            ("[53/53] Complete system compromise...", Colors.B, 0.4),
        ]

        for step_text, color, delay in steps:
            print(f"{color}{step_text}{Colors.END}")
            time.sleep(delay)
            if random.random() > 0.7:
                fast_print(f"  └─ Processing: {hex(random.randint(0x1000, 0xFFFF))}", Colors.G, 0.02)

        # Full system scan
        print(f"\n{Colors.Y}Running full system diagnostic...{Colors.END}")
        for i in range(20):
            progress = "█" * i + "░" * (20 - i)
            print(f"  {Colors.C}[{progress}] {i*5}%{Colors.END}", end="\r")
            time.sleep(0.02)
        print()

        # System compromised warning
        clear_screen()
        print(f"{Colors.R}{Colors.BOLD}")
        print("┌" + "─" * 60 + "┐")
        print("│" + " " * 60 + "│")
        print("│" + " " * 15 + "⚠  SYSTEM SUCCESSFULLY HACKED ⚠" + " " * 14 + "│")
        print("│" + " " * 60 + "│")
        print("│" + " " * 10 + "   Full administrative access granted" + " " * 13 + "│")
        print("│" + " " * 12 + "   Remote control established" + " " * 19 + "│")
        print("│" + " " * 60 + "│")
        print("└" + "─" * 60 + "┘")
        print(f"{Colors.END}")
        time.sleep(2)

        # Download and display image
        print(f"{Colors.Y}Downloading hacker image...{Colors.END}")
        github_url = "https://github.com/Sabari425/Others-Projects/blob/main/stock-photo-hacker-in-mask-on-dark-background.png"
        img_path = download_image_from_github(github_url)
        
        if img_path:
            print(f"{Colors.G}Image downloaded. Displaying in full screen ...{Colors.END}")
            
            # Method 1: Tkinter fullscreen with 260% zoom (most reliable)
            success = show_image_fullscreen_zoom(img_path, 120)
            
            if not success:
                # Method 2: Try PowerShell method
                success = show_image_with_powershell(img_path, 260)
            
            if not success:
                print(f"{Colors.R}Could not display image with zoom. Showing ASCII art instead.{Colors.END}")
                show_hacker_art()
        else:
            print(f"{Colors.R}Could not download image. Showing ASCII art.{Colors.END}")
            show_hacker_art()
        
        # Final countdown - 5 seconds
        print(f"\n{Colors.R}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════╗")
        print("║     SYSTEM RESTART INITIATED - DATA LOST             ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        for i in range(3, 0, -1):
            if i <= 3:
                color = Colors.B
            elif i <= 2:
                color = Colors.Y
            else:
                color = Colors.R
            print(f"{color}Restarting in {i} seconds...{Colors.END}")
            time.sleep(1)
        
        print(f"\n{Colors.R}⚠ SYSTEM REBOOTING NOW ⚠{Colors.END}")
        time.sleep(1)
        
        if os.name == 'nt':
            os.system('shutdown /r /t 0 /c "System compromised - Rebooting"')
        else:
            os.system('sudo reboot')
            
    except KeyboardInterrupt:
        print(f"\n{Colors.G}Hack sequence aborted. System remains safe.{Colors.END}")
        time.sleep(1)

if __name__ == "__main__":
    # Check for required libraries
    try:
        from PIL import Image
        import tkinter as tk
        from tkinter import Label
        from PIL import ImageTk
    except ImportError:
        print(f"{Colors.R}Required libraries not found. Installing Pillow...{Colors.END}")
        os.system('pip install pillow')
        print(f"{Colors.G}Please run the script again.{Colors.END}")
        time.sleep(3)
        exit()
    
    main()