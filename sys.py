import os
import platform
import psutil
import pwd
import time
import urllib.request
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv


DISK_THRESHOLD = 80
RAM_THRESHOLD = 80
CHECK_INTERVAL_SECONDS = 300 
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    """Sends an alert message to your Telegram chat."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print("   [TELEGRAM] Alert successfully sent to your phone!")
    except Exception as e:
        print(f"   [ERROR] Failed to send Telegram alert: {e}")

def run_system_check():
    print("=" * 60)
    print(f"          SYSTEM HEALTH CHECK RUN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. System Info
    print(f"🟢 Operating System: {platform.system()} {platform.release()}")
    
    # 2. Disk Check
    disk = psutil.disk_usage('/')
    print(f"💽 Disk Used: {disk.percent}% (Threshold: {DISK_THRESHOLD}%)")
    if disk.percent >= DISK_THRESHOLD:
        alert_msg = f"⚠️ *WARNING: High Disk Usage!*\nServer root partition is at *{disk.percent}%* capacity."
        print(f"   {alert_msg}")
        send_telegram_alert(alert_msg)
    else:
        print("   ✅ [STATUS] Disk usage is within safe limits.")
    
    # 3. Memory Check
    mem = psutil.virtual_memory()
    print(f"🧠 RAM Used: {mem.percent}% (Threshold: {RAM_THRESHOLD}%)")
    if mem.percent >= RAM_THRESHOLD:
        alert_msg = f"⚠️ *WARNING: High RAM Usage!*\nServer memory is at *{mem.percent}%* capacity."
        print(f"   {alert_msg}")
        send_telegram_alert(alert_msg)
    else:
        print("   ✅ [STATUS] Memory usage is within safe limits.")
        
    # 4. User Session Check (WSL-Safe)
    current_user = pwd.getpwuid(os.getuid()).pw_name
    print(f"👥 Current script runner: {current_user}")
    
    print("=" * 60)

if __name__ == "__main__":
    current_user = pwd.getpwuid(os.getuid()).pw_name
    print(f"Starting continuous system monitoring as user '{current_user}'...")
    print(f"Checking every {CHECK_INTERVAL_SECONDS} seconds. Press Ctrl+C to stop.\n")
    
    try:
        while True:
            run_system_check()
            time.sleep(CHECK_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user. Goodbye!")
