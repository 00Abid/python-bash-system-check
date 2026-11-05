import os
import platform
import psutil
import pwd
from datetime import datetime

# Define alert thresholds (%)
DISK_THRESHOLD = 80
RAM_THRESHOLD = 85

def print_banner():
    print("=" * 60)
    print("          DAILY SYSTEM HEALTH & INVENTORY REPORT (PYTHON)    ")
    print(f"          Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_system_info():
    print("\n🟢 1. SYSTEM UPTIME & OS")
    print(f"   - Operating System: {platform.system()} {platform.release()}")
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
    print(f"   - System Boot Time: {boot_time}")

def check_disk():
    print("\n💽 2. DISK SPACE USAGE (Root Partition)")
    disk = psutil.disk_usage('/')
    print(f"   - Total Size: {disk.total / (1024**3):.2f} GB")
    print(f"   - Used Space: {disk.used / (1024**3):.2f} GB ({disk.percent}%)")
    print(f"   - Free Space: {disk.free / (1024**3):.2f} GB")
    
    if disk.percent >= DISK_THRESHOLD:
        print(f"   ⚠️ [WARNING] Disk usage has exceeded {DISK_THRESHOLD}%!")
    else:
        print("   ✅ [STATUS] Disk usage is within safe limits.")

def check_memory():
    print("\n🧠 3. MEMORY (RAM) STATUS")
    mem = psutil.virtual_memory()
    print(f"   - Total RAM: {mem.total / (1024**3):.2f} GB")
    print(f"   - Used RAM:  {mem.used / (1024**3):.2f} GB ({mem.percent}%)")
    print(f"   - Free RAM:  {mem.available / (1024**3):.2f} GB")
    
    if mem.percent >= RAM_THRESHOLD:
        print(f"   ⚠️ [WARNING] RAM usage has exceeded {RAM_THRESHOLD}%!")
    else:
        print("   ✅ [STATUS] Memory usage is within safe limits.")

def check_users():
    print("\n👥 4. USER ACCOUNTS & SESSIONS")
    try:
        users = psutil.users()
        active_users = set(u.name for u in users)
        print(f"   - Currently active logged-in users: {list(active_users)}")
    except Exception:
        print("   - Unable to fetch active login sessions.")
    
    # Safely get current username across WSL and standard Linux
    current_user = pwd.getpwuid(os.getuid()).pw_name
    print(f"   - Current script runner: {current_user}")

def check_processes():
    print("\n⚙️  5. PROCESS FORENSICS (Top CPU Hogs)")
    print(f"   - Total running processes: {len(psutil.pids())}")
    print("   - Top 3 CPU-consuming processes:")
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    top_cpu = sorted(processes, key=lambda p: p['cpu_percent'] or 0.0, reverse=True)[:3]
    for p in top_cpu:
        print(f"     * PID: {p['pid']} | Name: {p['name']} | CPU: {p['cpu_percent']}%")

if __name__ == "__main__":
    print_banner()
    check_system_info()
    check_disk()
    check_memory()
    check_users()
    check_processes()
    print("\n" + "=" * 60)
    print("   REPORT COMPLETED SUCCESSFULLY!")
    print("=" * 60)
