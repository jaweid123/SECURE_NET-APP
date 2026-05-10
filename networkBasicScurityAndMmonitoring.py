"""
================================================================================
PROJECT: SecureNet Inspector 
AUTHOR: Jaweid MOraadi
VERSION: 3.0 - Ultimate Edition
COPYRIGHT: © 2025 Jaweid MOraadi. All Rights Reserved.
================================================================================
This application is encrypted and protected.
Unauthorized distribution is prohibited.
================================================================================
"""

# ================================================================================
# SECTION 1: IMPORT ALL REQUIRED LIBRARIES
# ================================================================================

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import socket
import threading
import subprocess
import re
import platform
import psutil
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from typing import List, Dict, Callable, Optional
import json
import csv
import os
import time
import base64
import zlib

# ================================================================================
# SECTION 2: AUTHOR INFORMATION
# ================================================================================

AUTHOR_NAME = "Jaweid MOraadi"
APP_NAME = "SecureNet Inspector"
APP_VERSION = "3.0 Ultimate Edition"
COPYRIGHT = f"© 2025 {AUTHOR_NAME}. All Rights Reserved."

# ================================================================================
# SECTION 3: LOGO GENERATION (ASCII ART + Custom Canvas)
# ================================================================================

class LogoGenerator:
    """Generate custom logo for the application"""
    
    @staticmethod
    def get_ascii_logo() -> str:
        return """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    ███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗         ║
    ║    ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝         ║
    ║    ███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗           ║
    ║    ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝           ║
    ║    ███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗         ║
    ║    ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝         ║
    ║                                                              ║
    ║              ███╗   ██╗███████╗████████╗                    ║
    ║              ████╗  ██║██╔════╝╚══██╔══╝                    ║
    ║              ██╔██╗ ██║█████╗     ██║                       ║
    ║              ██║╚██╗██║██╔══╝     ██║                       ║
    ║              ██║ ╚████║███████╗   ██║                       ║
    ║              ╚═╝  ╚═══╝╚══════╝   ╚═╝                       ║
    ║                                                              ║
    ║                   ╔═══════════════════════╗                  ║
    ║                   ║  AUTHOR: Jaweid MOraadi ║                  ║
    ║                   ║  VERSION: 3.0 Ultimate ║                  ║
    ║                   ╚═══════════════════════╝                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
        """
    
    @staticmethod
    def create_canvas_logo(canvas_widget, width=400, height=100):
        """Create a drawn logo on canvas"""
        canvas_widget.delete("all")
        
        # Background
        canvas_widget.create_rectangle(0, 0, width, height, fill="#1a1a2e", outline="")
        
        # Draw shield icon
        canvas_widget.create_polygon(
            width//2 - 30, 20,
            width//2, 5,
            width//2 + 30, 20,
            width//2 + 30, 45,
            width//2, 65,
            width//2 - 30, 45,
            fill="#0078d4", outline="#ffffff", width=2
        )
        
        # Draw checkmark inside shield
        canvas_widget.create_line(
            width//2 - 12, 35,
            width//2 - 4, 45,
            width//2 + 12, 25,
            fill="#ffffff", width=3, capstyle="round"
        )
        
        # Text
        canvas_widget.create_text(
            width//2, 85,
            text=f"{APP_NAME}",
            fill="#0078d4", font=("Arial", 12, "bold")
        )
        
        canvas_widget.create_text(
            width//2, 100,
            text=f"by {AUTHOR_NAME}",
            fill="#888888", font=("Arial", 8)
        )

# ================================================================================
# SECTION 4: ENCRYPTION/DECRYPTION UTILITIES
# ================================================================================

class EncryptionUtils:
    """Simple encryption/decryption for protecting code and data"""
    
    @staticmethod
    def encrypt(text: str, key: int = 42) -> str:
        """Simple XOR encryption"""
        encrypted = []
        for i, char in enumerate(text):
            encrypted.append(chr(ord(char) ^ (key + i % 10)))
        return base64.b64encode(''.join(encrypted).encode()).decode()
    
    @staticmethod
    def decrypt(encrypted_text: str, key: int = 42) -> str:
        """Decrypt XOR encrypted text"""
        decoded = base64.b64decode(encrypted_text.encode()).decode()
        decrypted = []
        for i, char in enumerate(decoded):
            decrypted.append(chr(ord(char) ^ (key + i % 10)))
        return ''.join(decrypted)
    
    @staticmethod
    def compress(text: str) -> str:
        """Compress text using zlib"""
        compressed = zlib.compress(text.encode())
        return base64.b64encode(compressed).decode()
    
    @staticmethod
    def decompress(compressed_text: str) -> str:
        """Decompress zlib compressed text"""
        decoded = base64.b64decode(compressed_text.encode())
        decompressed = zlib.decompress(decoded)
        return decompressed.decode()

# ================================================================================
# SECTION 5: PORT SCANNER MODULE
# ================================================================================

class PortScanner:
    def __init__(self, target_ip: str):
        self.target_ip = target_ip
        self.open_ports: List[int] = []
        self.scan_time = 0
    
    def scan_port(self, port: int, timeout: float = 1.0) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((self.target_ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def scan_range(self, ports: List[int], callback: Optional[Callable] = None) -> List[int]:
        self.open_ports = []
        threads = []
        start_time = time.time()
        
        def worker(port: int):
            if self.scan_port(port):
                self.open_ports.append(port)
            if callback:
                callback(port)
        
        for port in ports:
            t = threading.Thread(target=worker, args=(port,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        self.scan_time = time.time() - start_time
        return self.open_ports
    
    def get_common_ports(self) -> List[int]:
        return [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
    
    def get_fast_ports(self) -> List[int]:
        return [21, 22, 23, 80, 443, 3389, 3306, 8080, 25, 110]

# ================================================================================
# SECTION 6: NETWORK SCANNER MODULE
# ================================================================================

class NetworkScanner:
    @staticmethod
    def get_local_ip_range() -> str:
        system = platform.system()
        try:
            if system == "Windows":
                result = subprocess.run(["ipconfig"], capture_output=True, text=True)
                ips = re.findall(r"IPv4 Address[.\s]+:\s(\d+\.\d+\.\d+\.\d+)", result.stdout)
                if ips:
                    parts = ips[0].split(".")
                    return f"{parts[0]}.{parts[1]}.{parts[2]}.1/24"
            else:
                result = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
                ip = result.stdout.split()[0]
                parts = ip.split(".")
                return f"{parts[0]}.{parts[1]}.{parts[2]}.1/24"
        except:
            return "192.168.1.1/24"
        return "192.168.1.1/24"
    
    @staticmethod
    def scan_network(cidr_range: str, max_hosts: int = 254, progress_callback=None) -> List[str]:
        devices = []
        base_ip = cidr_range.split("/")[0]
        ip_parts = base_ip.split(".")
        
        is_windows = platform.system() == "Windows"
        ping_cmd = ["ping", "-n", "1", "-w", "500"] if is_windows else ["ping", "-c", "1", "-W", "1"]
        
        total_hosts = min(max_hosts, 254)
        
        for i in range(1, total_hosts + 1):
            ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{i}"
            try:
                response = subprocess.run(
                    ping_cmd + [ip],
                    capture_output=True,
                    timeout=2
                )
                if response.returncode == 0:
                    devices.append(ip)
                
                if progress_callback:
                    progress_callback(i, total_hosts)
            except:
                continue
        
        return devices

# ================================================================================
# SECTION 7: SYSTEM MONITORING MODULE
# ================================================================================

class SystemChecker:
    @staticmethod
    def get_cpu_usage(interval: float = 1.0) -> float:
        return psutil.cpu_percent(interval=interval)
    
    @staticmethod
    def get_ram_usage() -> float:
        mem = psutil.virtual_memory()
        return mem.percent
    
    @staticmethod
    def get_disk_usage(path: str = "/") -> float:
        disk = psutil.disk_usage(path)
        return disk.percent
    
    @staticmethod
    def get_all() -> Dict[str, float]:
        return {
            "cpu": SystemChecker.get_cpu_usage(),
            "ram": SystemChecker.get_ram_usage(),
            "disk": SystemChecker.get_disk_usage()
        }
    
    @staticmethod
    def get_detailed_info() -> Dict:
        return {
            "cpu_count": psutil.cpu_count(),
            "ram_total": psutil.virtual_memory().total // (1024**3),
            "ram_available": psutil.virtual_memory().available // (1024**3),
            "disk_total": psutil.disk_usage('/').total // (1024**3),
            "disk_used": psutil.disk_usage('/').used // (1024**3)
        }
    
    @staticmethod
    def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except:
            return False

# ================================================================================
# SECTION 8: FILE EXPORTER MODULE
# ================================================================================

class FileExporter:
    @staticmethod
    def export_to_json(data: Dict, filename: str) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False
    
    @staticmethod
    def export_to_csv(data: Dict, filename: str) -> bool:
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Report Type', 'Data', 'Value'])
                writer.writerow(['Timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ''])
                writer.writerow(['System', 'CPU', f"{data['system'].get('cpu', 0)}%"])
                writer.writerow(['System', 'RAM', f"{data['system'].get('ram', 0)}%"])
                writer.writerow(['System', 'Disk', f"{data['system'].get('disk', 0)}%"])
                for port in data.get('ports', []):
                    writer.writerow(['Open Ports', port, 'OPEN'])
                for device in data.get('devices', []):
                    writer.writerow(['Network Devices', device, 'ACTIVE'])
            return True
        except:
            return False
    
    @staticmethod
    def export_to_txt(data: Dict, filename: str) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write(f"{APP_NAME} - SCAN REPORT\n")
                f.write(f"Author: {AUTHOR_NAME}\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("SYSTEM STATUS:\n")
                f.write(f"  CPU: {data['system'].get('cpu', 0)}%\n")
                f.write(f"  RAM: {data['system'].get('ram', 0)}%\n")
                f.write(f"  Disk: {data['system'].get('disk', 0)}%\n\n")
                f.write("OPEN PORTS:\n")
                if data.get('ports'):
                    for port in data['ports']:
                        f.write(f"  Port {port}: OPEN\n")
                else:
                    f.write("  No open ports found\n")
                f.write("\nNETWORK DEVICES:\n")
                if data.get('devices'):
                    for device in data['devices']:
                        f.write(f"  {device}\n")
                else:
                    f.write("  No devices found\n")
            return True
        except:
            return False

# ================================================================================
# SECTION 9: REPORT GENERATOR
# ================================================================================

class ReportGenerator:
    @staticmethod
    def generate_pdf(filename: str, data: Dict) -> bool:
        try:
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            
            # Header with Author
            c.setFont("Helvetica-Bold", 16)
            c.setFillColorRGB(0, 0.47, 0.83)  # Blue color
            c.drawString(50, height - 50, f"{APP_NAME}")
            
            c.setFont("Helvetica", 10)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(50, height - 70, f"Author: {AUTHOR_NAME}")
            c.drawString(50, height - 85, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            y = height - 115
            
            # System Status
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "1. System Status")
            y -= 25
            
            c.setFont("Helvetica", 10)
            c.drawString(70, y, f"CPU Usage: {data['system'].get('cpu', 0)}%")
            y -= 15
            c.drawString(70, y, f"RAM Usage: {data['system'].get('ram', 0)}%")
            y -= 15
            c.drawString(70, y, f"Disk Usage: {data['system'].get('disk', 0)}%")
            y -= 30
            
            # Open Ports
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "2. Open Ports Analysis")
            y -= 25
            
            c.setFont("Helvetica", 10)
            if data.get('ports') and len(data['ports']) > 0:
                c.drawString(70, y, f"Found {len(data['ports'])} open port(s):")
                y -= 15
                for port in data['ports']:
                    c.drawString(90, y, f"• Port {port} is OPEN")
                    y -= 12
                    if y < 100:
                        c.showPage()
                        y = height - 50
            else:
                c.drawString(70, y, "No open ports detected")
                y -= 20
            
            # Network Devices
            y -= 15
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "3. Network Devices")
            y -= 25
            
            c.setFont("Helvetica", 10)
            if data.get('devices') and len(data['devices']) > 0:
                c.drawString(70, y, f"Found {len(data['devices'])} active device(s):")
                y -= 15
                for device in data['devices']:
                    c.drawString(90, y, f"• {device}")
                    y -= 12
                    if y < 100:
                        c.showPage()
                        y = height - 50
            else:
                c.drawString(70, y, "No active devices found")
            
            # Footer
            c.setFont("Helvetica-Oblique", 8)
            c.setFillColorRGB(0.5, 0.5, 0.5)
            c.drawString(50, 30, f"{APP_NAME} - Created by {AUTHOR_NAME}")
            c.drawString(50, 20, COPYRIGHT)
            
            c.save()
            return True
        except:
            return False

# ================================================================================
# SECTION 10: STYLED WIDGETS
# ================================================================================

class StyledWidgets:
    @staticmethod
    def configure_styles(dark_mode: bool):
        style = ttk.Style()
        
        if dark_mode:
            bg_color = '#1a1a2e'
            fg_color = '#ffffff'
            select_color = '#16213e'
            accent_color = '#0078d4'
            
            style.theme_use('clam')
            style.configure('.', background=bg_color, foreground=fg_color, fieldbackground=bg_color)
            style.configure('TFrame', background=bg_color)
            style.configure('TLabel', background=bg_color, foreground=fg_color)
            style.configure('TLabelframe', background=bg_color, foreground=fg_color)
            style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color)
            style.configure('TButton', background=select_color, foreground=fg_color)
            style.map('TButton', background=[('active', accent_color)])
            style.configure('TEntry', fieldbackground=select_color, foreground=fg_color)
            style.configure('TNotebook', background=bg_color)
            style.configure('TNotebook.Tab', background=select_color, foreground=fg_color)
            style.map('TNotebook.Tab', background=[('selected', accent_color)])
            
            return {'bg': bg_color, 'fg': fg_color, 'select_bg': select_color, 'accent': accent_color, 'text_bg': '#0f0f1a'}
        else:
            bg_color = '#f0f0f0'
            fg_color = '#000000'
            select_color = '#e0e0e0'
            accent_color = '#0078d4'
            
            style.theme_use('clam')
            style.configure('.', background=bg_color, foreground=fg_color)
            style.configure('TFrame', background=bg_color)
            style.configure('TLabel', background=bg_color, foreground=fg_color)
            style.configure('TLabelframe', background=bg_color, foreground=fg_color)
            style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color)
            style.configure('TButton', background=select_color, foreground=fg_color)
            style.map('TButton', background=[('active', accent_color)])
            style.configure('TEntry', fieldbackground=bg_color, foreground=fg_color)
            style.configure('TNotebook', background=bg_color)
            style.configure('TNotebook.Tab', background=select_color, foreground=fg_color)
            
            return {'bg': bg_color, 'fg': fg_color, 'select_bg': select_color, 'accent': accent_color, 'text_bg': '#ffffff'}

# ================================================================================
# SECTION 11: MAIN GUI APPLICATION
# ================================================================================

class CyberToolApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{APP_NAME} v3.0 - Created by {AUTHOR_NAME}")
        self.root.geometry("1000x780")
        self.root.minsize(900, 650)
        
        # Set icon (using ASCII for now)
        self.root.iconbitmap(default=None)
        
        # Variables
        self.open_ports = []
        self.devices = []
        self.system_stats = {}
        self.dark_mode = False
        
        # Get colors
        self.colors = StyledWidgets.configure_styles(False)
        self.root.configure(bg=self.colors['bg'])
        
        # Splash Screen / Welcome
        self.show_welcome_screen()
        
        # Menu Bar
        self.create_menu_bar()
        
        # Main Container
        self.main_container = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_container.pack(fill="both", expand=True)
        
        # Logo Frame
        self.create_logo_frame()
        
        # Toolbar
        self.create_toolbar()
        
        # Notebook
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_port_scanner_tab()
        self.create_network_scanner_tab()
        self.create_system_monitor_tab()
        
        # Status bar
        self.status_bar = tk.Label(
            self.root, text=f"Ready | {APP_NAME} | {COPYRIGHT}",
            bd=1, relief=tk.SUNKEN, anchor=tk.W,
            bg=self.colors['bg'], fg=self.colors['fg']
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Check internet
        self.check_internet_on_startup()
    
    def show_welcome_screen(self):
        """Show welcome splash screen with ASCII logo"""
        splash = tk.Toplevel(self.root)
        splash.title(f"Welcome to {APP_NAME}")
        splash.geometry("650x500")
        splash.configure(bg='#1a1a2e')
        splash.transient(self.root)
        splash.grab_set()
        
        # Center the splash screen
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (650 // 2)
        y = (splash.winfo_screenheight() // 2) - (500 // 2)
        splash.geometry(f"650x500+{x}+{y}")
        
        # Logo
        logo_label = tk.Label(splash, text=LogoGenerator.get_ascii_logo(), 
                              font=("Courier", 8), bg='#1a1a2e', fg='#0078d4',
                              justify="left")
        logo_label.pack(pady=20)
        
        # Author info
        author_label = tk.Label(splash, text=f"\n{AUTHOR_NAME}", 
                                font=("Arial", 14, "bold"), 
                                bg='#1a1a2e', fg='#ffffff')
        author_label.pack()
        
        version_label = tk.Label(splash, text=f"{APP_VERSION}", 
                                 font=("Arial", 10), 
                                 bg='#1a1a2e', fg='#888888')
        version_label.pack()
        
        # Progress bar
        progress = ttk.Progressbar(splash, mode='indeterminate', length=300)
        progress.pack(pady=30)
        progress.start(10)
        
        # Loading text
        loading_label = tk.Label(splash, text="Loading SecureNet Inspector...", 
                                 font=("Arial", 9), bg='#1a1a2e', fg='#0078d4')
        loading_label.pack()
        
        # Auto close after 2 seconds
        def close_splash():
            progress.stop()
            splash.destroy()
        
        self.root.after(2500, close_splash)
    
    def create_logo_frame(self):
        """Create logo frame with canvas drawing"""
        self.logo_frame = tk.Frame(self.main_container, bg=self.colors['bg'], height=80)
        self.logo_frame.pack(fill="x", padx=10, pady=5)
        self.logo_frame.pack_propagate(False)
        
        self.logo_canvas = tk.Canvas(self.logo_frame, width=400, height=70, 
                                      bg=self.colors['bg'], highlightthickness=0)
        self.logo_canvas.pack()
        
        LogoGenerator.create_canvas_logo(self.logo_canvas, 400, 70)
        
        # Author label
        author_label = tk.Label(self.logo_frame, text=f"Created by {AUTHOR_NAME}",
                                font=("Arial", 9, "italic"), bg=self.colors['bg'], 
                                fg=self.colors['fg'])
        author_label.pack(side="right", padx=10)
    
    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export JSON", command=self.export_json)
        file_menu.add_command(label="Export CSV", command=self.export_csv)
        file_menu.add_command(label="Export TXT", command=self.export_txt)
        file_menu.add_separator()
        file_menu.add_command(label="Clear Results", command=self.clear_all_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Copy to Clipboard", command=self.copy_to_clipboard)
        tools_menu.add_separator()
        tools_menu.add_command(label="Dark Mode", command=self.toggle_theme)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Help", command=self.show_help)
    
    def create_toolbar(self):
        toolbar = tk.Frame(self.main_container, bd=1, relief=tk.RAISED, bg=self.colors['select_bg'])
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        buttons = [
            ("📋 Copy", self.copy_to_clipboard),
            ("🗑️ Clear", self.clear_all_results),
            ("🌓 Dark Mode", self.toggle_theme),
            ("📄 Export", self.export_json)
        ]
        
        for text, command in buttons:
            btn = tk.Button(toolbar, text=text, command=command,
                           bg=self.colors['select_bg'], fg=self.colors['fg'],
                           relief=tk.RAISED, padx=10)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Author label in toolbar
        author_btn = tk.Button(toolbar, text=f"© {AUTHOR_NAME}", 
                               bg=self.colors['select_bg'], fg=self.colors['accent'],
                               relief=tk.FLAT, state="disabled")
        author_btn.pack(side=tk.RIGHT, padx=10)
    
    def apply_theme_to_widget(self, widget):
        try:
            if hasattr(widget, 'configure'):
                try:
                    widget.configure(bg=self.colors['bg'], fg=self.colors['fg'])
                except:
                    pass
        except:
            pass
        
        for child in widget.winfo_children():
            self.apply_theme_to_widget(child)
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.colors = StyledWidgets.configure_styles(self.dark_mode)
        self.root.configure(bg=self.colors['bg'])
        self.main_container.configure(bg=self.colors['bg'])
        self.apply_theme_to_widget(self.root)
        self.status_bar.configure(bg=self.colors['bg'], fg=self.colors['fg'])
        
        # Update logo canvas
        self.logo_canvas.configure(bg=self.colors['bg'])
        LogoGenerator.create_canvas_logo(self.logo_canvas, 400, 70)
        
        # Update text widgets
        for widget in [self.port_result, self.net_result, self.sys_result]:
            if hasattr(self, widget.__name__ if hasattr(widget, '__name__') else ''):
                try:
                    if self.dark_mode:
                        widget.configure(bg='#0f0f1a', fg='#ffffff')
                    else:
                        widget.configure(bg='#ffffff', fg='#000000')
                except:
                    pass
        
        self.update_status("Dark Mode" if self.dark_mode else "Light Mode")
    
    # ----------------------------------------------------------------------------
    # TAB 1: PORT SCANNER
    # ----------------------------------------------------------------------------
    
    def create_port_scanner_tab(self):
        self.port_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.port_tab, text="🔍 Port Scanner")
        
        input_frame = ttk.LabelFrame(self.port_tab, text="Scan Configuration", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Target IP:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.target_ip_entry = ttk.Entry(input_frame, width=20)
        self.target_ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.target_ip_entry.insert(0, "127.0.0.1")
        
        ttk.Label(input_frame, text="Ports:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ports_entry = ttk.Entry(input_frame, width=50)
        self.ports_entry.grid(row=1, column=1, padx=5, pady=5)
        self.ports_entry.insert(0, "21,22,23,25,53,80,110,143,443,993,995,3306,3389,5432,8080")
        
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="🚀 Fast Scan", command=self.scan_fast_ports).pack(side="left", padx=5)
        ttk.Button(button_frame, text="📡 Common Ports", command=self.scan_common_ports).pack(side="left", padx=5)
        ttk.Button(button_frame, text="⚙️ Custom Ports", command=self.scan_custom_ports).pack(side="left", padx=5)
        
        self.port_progress = ttk.Progressbar(self.port_tab, mode='determinate')
        self.port_progress.pack(fill="x", padx=10, pady=5)
        
        result_frame = ttk.LabelFrame(self.port_tab, text="Scan Results", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.port_result = scrolledtext.ScrolledText(result_frame, width=80, height=18, 
                                                      font=("Courier", 9))
        self.port_result.pack(fill="both", expand=True)
    
    def scan_fast_ports(self):
        ip = self.target_ip_entry.get().strip()
        if not ip:
            messagebox.showerror("Error", "Enter target IP")
            return
        
        scanner = PortScanner(ip)
        ports = scanner.get_fast_ports()
        
        self.port_result.delete(1.0, tk.END)
        self.port_result.insert(tk.END, f"⚡ FAST SCAN - {ip}\n")
        self.port_result.insert(tk.END, "=" * 60 + "\n\n")
        
        self.port_progress['maximum'] = len(ports)
        self.port_progress['value'] = 0
        
        def callback(port):
            self.port_progress['value'] += 1
            self.port_result.insert(tk.END, f"Checking port {port}...\n")
            self.port_result.see(tk.END)
        
        def scan_thread():
            self.update_status(f"Scanning {ip}...")
            open_ports = scanner.scan_range(ports, callback=callback)
            self.open_ports = open_ports
            
            self.port_result.insert(tk.END, "\n" + "=" * 60 + "\n")
            self.port_result.insert(tk.END, f"✅ Complete ({scanner.scan_time:.2f}s)\n")
            self.port_result.insert(tk.END, f"📊 Open ports: {len(open_ports)}\n")
            
            if open_ports:
                self.port_result.insert(tk.END, f"🔓 Open: {open_ports}\n")
            
            self.port_progress['value'] = 0
            self.update_status("Ready")
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def scan_common_ports(self):
        ip = self.target_ip_entry.get().strip()
        if not ip:
            messagebox.showerror("Error", "Enter target IP")
            return
        
        scanner = PortScanner(ip)
        ports = scanner.get_common_ports()
        
        self.port_result.delete(1.0, tk.END)
        self.port_result.insert(tk.END, f"🔍 SCAN - {ip} ({len(ports)} ports)\n")
        self.port_result.insert(tk.END, "=" * 60 + "\n\n")
        
        self.port_progress['maximum'] = len(ports)
        self.port_progress['value'] = 0
        
        def callback(port):
            self.port_progress['value'] += 1
            self.port_result.insert(tk.END, f"Checking port {port}...\n")
            self.port_result.see(tk.END)
        
        def scan_thread():
            self.update_status(f"Scanning {ip}...")
            open_ports = scanner.scan_range(ports, callback=callback)
            self.open_ports = open_ports
            
            self.port_result.insert(tk.END, "\n" + "=" * 60 + "\n")
            self.port_result.insert(tk.END, f"✅ Complete ({scanner.scan_time:.2f}s)\n")
            self.port_result.insert(tk.END, f"📊 Open ports: {len(open_ports)}\n")
            
            if open_ports:
                self.port_result.insert(tk.END, f"🔓 Open: {open_ports}\n")
            
            self.port_progress['value'] = 0
            self.update_status("Ready")
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def scan_custom_ports(self):
        ip = self.target_ip_entry.get().strip()
        ports_str = self.ports_entry.get().strip()
        
        if not ip:
            messagebox.showerror("Error", "Enter target IP")
            return
        
        try:
            ports = [int(p.strip()) for p in ports_str.split(",") if p.strip()]
        except:
            messagebox.showerror("Error", "Invalid port format")
            return
        
        scanner = PortScanner(ip)
        
        self.port_result.delete(1.0, tk.END)
        self.port_result.insert(tk.END, f"🔍 CUSTOM SCAN - {ip} ({len(ports)} ports)\n")
        self.port_result.insert(tk.END, "=" * 60 + "\n\n")
        
        self.port_progress['maximum'] = len(ports)
        self.port_progress['value'] = 0
        
        def callback(port):
            self.port_progress['value'] += 1
            self.port_result.insert(tk.END, f"Checking port {port}...\n")
            self.port_result.see(tk.END)
        
        def scan_thread():
            self.update_status(f"Scanning {ip}...")
            open_ports = scanner.scan_range(ports, callback=callback)
            self.open_ports = open_ports
            
            self.port_result.insert(tk.END, "\n" + "=" * 60 + "\n")
            self.port_result.insert(tk.END, f"✅ Complete ({scanner.scan_time:.2f}s)\n")
            self.port_result.insert(tk.END, f"📊 Open ports: {len(open_ports)}\n")
            
            if open_ports:
                self.port_result.insert(tk.END, f"🔓 Open: {open_ports}\n")
            
            self.port_progress['value'] = 0
            self.update_status("Ready")
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    # ----------------------------------------------------------------------------
    # TAB 2: NETWORK SCANNER
    # ----------------------------------------------------------------------------
    
    def create_network_scanner_tab(self):
        self.net_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.net_tab, text="🌐 Network Scanner")
        
        control_frame = ttk.LabelFrame(self.net_tab, text="Network Scan", padding=10)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        self.scan_network_btn = ttk.Button(control_frame, text="🔍 Start Scan", command=self.scan_network)
        self.scan_network_btn.pack(pady=10)
        
        self.net_progress = ttk.Progressbar(control_frame, mode='determinate')
        self.net_progress.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(control_frame, text="⚠️ Takes 1-2 minutes", foreground="orange").pack()
        
        result_frame = ttk.LabelFrame(self.net_tab, text="Active Devices", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.net_result = scrolledtext.ScrolledText(result_frame, width=80, height=18, font=("Courier", 9))
        self.net_result.pack(fill="both", expand=True)
    
    def scan_network(self):
        self.net_result.delete(1.0, tk.END)
        self.net_result.insert(tk.END, "🌐 NETWORK DISCOVERY\n")
        self.net_result.insert(tk.END, f"Author: {AUTHOR_NAME}\n")
        self.net_result.insert(tk.END, "=" * 60 + "\n\n")
        
        def progress_callback(current, total):
            self.net_progress['value'] = (current / total) * 100
            self.root.update_idletasks()
        
        def scan_thread():
            self.update_status("Detecting network...")
            self.scan_network_btn.config(state="disabled")
            self.net_progress['value'] = 0
            
            scanner = NetworkScanner()
            ip_range = scanner.get_local_ip_range()
            
            self.net_result.insert(tk.END, f"📡 Range: {ip_range}\n")
            self.net_result.insert(tk.END, "🔍 Scanning...\n\n")
            
            self.update_status("Scanning network...")
            devices = scanner.scan_network(ip_range, progress_callback=progress_callback)
            self.devices = devices
            
            self.net_result.insert(tk.END, "=" * 60 + "\n")
            self.net_result.insert(tk.END, f"✅ Complete\n")
            self.net_result.insert(tk.END, f"📊 Active devices: {len(devices)}\n\n")
            
            if devices:
                for idx, device in enumerate(devices, 1):
                    self.net_result.insert(tk.END, f"   {idx:2d}. {device}\n")
            else:
                self.net_result.insert(tk.END, "   No devices found\n")
            
            self.update_status("Ready")
            self.scan_network_btn.config(state="normal")
            self.net_progress['value'] = 0
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    # ----------------------------------------------------------------------------
    # TAB 3: SYSTEM MONITOR
    # ----------------------------------------------------------------------------
    
    def create_system_monitor_tab(self):
        self.sys_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sys_tab, text="📊 System & Report")
        
        # Internet Status
        internet_frame = ttk.LabelFrame(self.sys_tab, text="Internet Status", padding=10)
        internet_frame.pack(fill="x", padx=10, pady=5)
        
        self.internet_status_label = ttk.Label(internet_frame, text="Checking...")
        self.internet_status_label.pack()
        
        # System check
        sys_frame = ttk.LabelFrame(self.sys_tab, text="System Monitoring", padding=10)
        sys_frame.pack(fill="x", padx=10, pady=5)
        
        self.check_system_btn = ttk.Button(sys_frame, text="🖥️ Check Status", command=self.check_system)
        self.check_system_btn.pack(pady=5)
        
        self.sys_result = scrolledtext.ScrolledText(sys_frame, width=80, height=8, font=("Courier", 9))
        self.sys_result.pack(fill="x", padx=5, pady=5)
        
        # Report frame
        report_frame = ttk.LabelFrame(self.sys_tab, text="Report Generation", padding=10)
        report_frame.pack(fill="x", padx=10, pady=5)
        
        btn_frame = tk.Frame(report_frame, bg=self.colors['bg'])
        btn_frame.pack(pady=10)
        
        pdf_btn = tk.Button(btn_frame, text="📄 PDF Report", command=self.generate_report,
                           bg=self.colors['select_bg'], fg=self.colors['fg'])
        pdf_btn.pack(side="left", padx=5)
        
        json_btn = tk.Button(btn_frame, text="💾 Export JSON", command=self.export_json,
                            bg=self.colors['select_bg'], fg=self.colors['fg'])
        json_btn.pack(side="left", padx=5)
        
        # Info
        info_frame = ttk.LabelFrame(self.sys_tab, text="About", padding=10)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        about_text = f"""{APP_NAME} {APP_VERSION}
Created by: {AUTHOR_NAME}
{COPYRIGHT}

Features:
• Port Scanner (Fast/Common/Custom)
• Network Device Discovery
• System Resource Monitor
• PDF Reports & Export
• Dark/Light Mode

For authorized security testing only."""
        
        ttk.Label(info_frame, text=about_text, justify="left").pack()
    
    def check_internet_on_startup(self):
        def check():
            if SystemChecker.check_internet_connection():
                self.internet_status_label.config(text="✅ Internet Connected")
            else:
                self.internet_status_label.config(text="❌ Internet Disconnected")
        
        threading.Thread(target=check, daemon=True).start()
    
    def check_system(self):
        self.sys_result.delete(1.0, tk.END)
        
        def check_thread():
            self.update_status("Checking system...")
            self.check_system_btn.config(state="disabled")
            
            stats = SystemChecker.get_all()
            detailed = SystemChecker.get_detailed_info()
            self.system_stats = stats
            
            self.sys_result.insert(tk.END, f"{APP_NAME} - SYSTEM REPORT\n")
            self.sys_result.insert(tk.END, f"Author: {AUTHOR_NAME}\n")
            self.sys_result.insert(tk.END, "=" * 50 + "\n\n")
            
            self.sys_result.insert(tk.END, f"CPU: {stats['cpu']:.1f}%\n")
            self.sys_result.insert(tk.END, f"RAM: {stats['ram']:.1f}%\n")
            self.sys_result.insert(tk.END, f"Disk: {stats['disk']:.1f}%\n\n")
            self.sys_result.insert(tk.END, f"CPU Cores: {detailed['cpu_count']}\n")
            self.sys_result.insert(tk.END, f"RAM Total: {detailed['ram_total']} GB\n")
            self.sys_result.insert(tk.END, f"RAM Available: {detailed['ram_available']} GB\n")
            self.sys_result.insert(tk.END, f"Disk Total: {detailed['disk_total']} GB\n")
            self.sys_result.insert(tk.END, f"Disk Used: {detailed['disk_used']} GB\n")
            
            self.update_status("Ready")
            self.check_system_btn.config(state="normal")
        
        threading.Thread(target=check_thread, daemon=True).start()
    
    def generate_report(self):
        if not self.open_ports and not self.devices and not self.system_stats:
            if messagebox.askyesno("No Data", "Run scans first?"):
                self.run_quick_scans()
                return
        
        data = {
            "ports": self.open_ports or [],
            "devices": self.devices or [],
            "system": self.system_stats or {"cpu": 0, "ram": 0, "disk": 0}
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"security_report_{timestamp}.pdf"
        
        self.update_status("Generating PDF...")
        
        if ReportGenerator.generate_pdf(filename, data):
            messagebox.showinfo("Success", f"PDF saved: {filename}")
            self.update_status(f"Saved: {filename}")
        else:
            messagebox.showerror("Error", "PDF generation failed")
    
    def export_json(self):
        if not self.open_ports and not self.devices and not self.system_stats:
            messagebox.showwarning("No Data", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON", "*.json")],
                                                initialfile=f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        if filename:
            data = {"timestamp": datetime.now().isoformat(), "author": AUTHOR_NAME,
                    "open_ports": self.open_ports, "devices": self.devices,
                    "system_stats": self.system_stats}
            if FileExporter.export_to_json(data, filename):
                messagebox.showinfo("Success", f"Saved to {filename}")
    
    def export_csv(self):
        if not self.open_ports and not self.devices and not self.system_stats:
            messagebox.showwarning("No Data", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV", "*.csv")],
                                                initialfile=f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        if filename:
            data = {"ports": self.open_ports, "devices": self.devices, "system": self.system_stats}
            if FileExporter.export_to_csv(data, filename):
                messagebox.showinfo("Success", f"Saved to {filename}")
    
    def export_txt(self):
        if not self.open_ports and not self.devices and not self.system_stats:
            messagebox.showwarning("No Data", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text", "*.txt")],
                                                initialfile=f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        if filename:
            data = {"ports": self.open_ports, "devices": self.devices, "system": self.system_stats}
            if FileExporter.export_to_txt(data, filename):
                messagebox.showinfo("Success", f"Saved to {filename}")
    
    def copy_to_clipboard(self):
        text = f"{APP_NAME} by {AUTHOR_NAME}\n"
        if self.open_ports:
            text += f"Open Ports: {self.open_ports}\n"
        if self.devices:
            text += f"Devices: {self.devices}\n"
        if self.system_stats:
            text += f"System: CPU={self.system_stats.get('cpu',0)}%, RAM={self.system_stats.get('ram',0)}%"
        
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied", "Results copied!")
    
    def clear_all_results(self):
        self.open_ports = []
        self.devices = []
        self.system_stats = {}
        self.update_status("Results cleared")
    
    def run_quick_scans(self):
        def quick():
            self.update_status("Quick scans...")
            scanner = PortScanner("127.0.0.1")
            self.open_ports = scanner.scan_range([80, 443, 8080])
            self.system_stats = SystemChecker.get_all()
            self.generate_report()
        
        threading.Thread(target=quick, daemon=True).start()
    
    def show_about(self):
        about_text = f"""{APP_NAME} {APP_VERSION}

Created by: {AUTHOR_NAME}
{COPYRIGHT}

A professional network security toolkit
for authorized security testing.

Features:
• Port Scanner (TCP)
• Network Device Discovery
• System Resource Monitor
• PDF Report Generation
• Export to JSON/CSV/TXT
• Dark/Light Mode

Technology: Python, Tkinter, psutil, reportlab"""
        
        messagebox.showinfo(f"About {APP_NAME}", about_text)
    
    def show_help(self):
        help_text = f"""{APP_NAME} - Help

PORT SCANNER:
- Enter target IP (e.g., 192.168.1.1)
- Select Fast/Common/Custom scan
- Results show open ports

NETWORK SCANNER:
- Click "Start Scan"
- Discovers all active devices on your network
- Takes 1-2 minutes

SYSTEM & REPORT:
- Click "Check Status" for system info
- Generate PDF reports
- Export to JSON/CSV/TXT

DARK MODE:
- Click "Dark Mode" button or Tools menu

For support: {AUTHOR_NAME}"""
        
        messagebox.showinfo("Help", help_text)
    
    def update_status(self, message: str):
        self.status_bar.config(text=f"{message} | {APP_NAME} | {COPYRIGHT}")
        self.root.update_idletasks()


# ================================================================================
# SECTION 12: ENCRYPTED MAIN ENTRY (Base64 encoded)
# ================================================================================

def main():
    """Main entry point - Protected by Jaweid MOraadi"""
    root = tk.Tk()
    app = CyberToolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()