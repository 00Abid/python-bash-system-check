# 🐧 Linux & WSL Automated System Health Reporter

A lightweight, production-grade automation suite built in **Python** to
monitor server resource utilization (Disk, RAM, CPU usage per core,
Uptime, and User Sessions) on Linux and WSL environments, featuring
real-time alerting via the **Telegram Bot API**.

------------------------------------------------------------------------

## 🚀 Features

-   **Cross-platform compatibility:** Tested on Ubuntu via WSL2 and
    standard Linux distributions.
-   **Resource threshold monitoring:** Checks disk, RAM, and CPU usage
    against configurable safety limits.
-   **Per-core CPU tracking:** Reports usage for every logical CPU core
    using `psutil`.
-   **Real-time Telegram alerts:** Sends Markdown-formatted warnings
    using the Telegram Bot API.
-   **WSL-safe user lookup:** Uses Python's `pwd` module to avoid
    platform-specific username issues.
-   **Production service support:** Includes a systemd service unit for
    automatic startup, restart, and logging.
-   **Lightweight:** Uses only Python standard libraries plus `psutil`.

------------------------------------------------------------------------

## 📂 Repository Structure

``` text
python-bash-system-check/
├── sys.py       # Python monitoring script with Telegram alerts
├── system_report.sh      # Native Bash system health reporter
├── requirements.txt      # Python dependencies
├── sys-telegram.service  # systemd service file
└── README.md             # Project documentation
```

## 🛠️ Prerequisites & Dependencies

Install Python 3, pip, and psutil:

``` bash
sudo apt update
sudo apt install -y python3 python3-pip python3-psutil
```

Alternatively, install dependencies using a virtual environment and
requirements.txt:

``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Configuration

Open `sys.py` and update your thresholds and Telegram
credentials:

``` python
DISK_THRESHOLD = 80
RAM_THRESHOLD = 85
CPU_THRESHOLD = 85
CHECK_INTERVAL_SECONDS = 300

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
```

  -----------------------------------------------------------------------------
  Setting                                         Default Meaning
  -------------------------- ---------------------------- ---------------------
  `DISK_THRESHOLD`                                     80 Send an alert when
                                                          disk usage is at or
                                                          above this percentage

  `RAM_THRESHOLD`                                      85 Send an alert when
                                                          RAM usage is at or
                                                          above this percentage

  `CPU_THRESHOLD`                                      85 Send an alert when
                                                          overall CPU usage is
                                                          at or above this
                                                          percentage

  `CHECK_INTERVAL_SECONDS`                            300 Time between checks,
                                                          in seconds

  `TELEGRAM_BOT_TOKEN`                               None Telegram bot token
                                                          from @BotFather

  `TELEGRAM_CHAT_ID`                                 None Telegram chat or
                                                          channel ID that
                                                          receives alerts
  -----------------------------------------------------------------------------


``` python
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
```

Export them before running:

``` bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
python3 sys.py
```

## 🏃 Usage & Execution

### 1. Run one manual check

``` bash
python3 sys.py
```

### 2. Run continuously in the background using nohup

``` bash
nohup python3 sys.py > monitor.log 2>&1 &
```

View live logs:

``` bash
tail -f monitor.log
```

Find and stop the background process:

``` bash
pgrep -f sys.py
kill <PID_NUMBER>
```

## ⚙️ Run Automatically at Boot with systemd

For native Linux or WSL2 with systemd enabled, use a systemd service for
reliable 24/7 background execution.

### 1. Copy files to a stable location

``` bash
sudo mkdir -p /opt/system-monitor
sudo cp sys.py requirements.txt /opt/system-monitor/
```

### 2. Create the service file

``` bash
sudo nano /etc/systemd/system/sys-telegram.service
```

Add the following configuration:

``` ini
[Unit]
Description=Linux and WSL System Health Telegram Monitor
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/opt/system-monitor
ExecStart=/usr/bin/python3 /opt/system-monitor/sys_telegram.py
Restart=always
RestartSec=10
User=your_username
Environment=TELEGRAM_BOT_TOKEN=your_bot_token
Environment=TELEGRAM_CHAT_ID=your_chat_id
StandardOutput=journal
StandardError=journal
SyslogIdentifier=sys-telegram

[Install]
WantedBy=multi-user.target
```

### 3. Enable and start the service

``` bash
sudo systemctl daemon-reload
sudo systemctl enable sys-telegram.service
sudo systemctl start sys-telegram.service
```

### 4. Check status and logs

``` bash
sudo systemctl status sys-telegram.service
sudo journalctl -u sys-telegram.service -f
```

## 📡 Telegram Setup

1.  Open Telegram and search for @BotFather.

2.  Send `/newbot` and follow the prompts to create your bot.

3.  Copy your Bot Token.

4.  Send a message to your bot in Telegram.

5.  Retrieve your Chat ID by opening:

    `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

## 👤 Author

Abid Khan\
Cloud & DevOps Engineering Learning Journey\
GitHub: @00Abid

------------------------------------------------------------------------

