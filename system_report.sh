#!/bin/bash

# Define alert thresholds (%)
DISK_THRESHOLD=80
RAM_THRESHOLD=85

echo "===================================================="
echo "          DAILY SYSTEM HEALTH & INVENTORY REPORT    "
echo "          Generated on: $(date)"
echo "===================================================="

echo ""
echo "🟢 1. SYSTEM UPTIME & LOAD"
uptime -p
echo "   - Load Average: $(awk '{print $1, $2, $3}' /proc/loadavg)"

echo ""
echo "💽 2. DISK SPACE USAGE (Root Partition)"
DISK_USAGE_PCT=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
DISK_TOTAL=$(df -h / | awk 'NR==2 {print $2}')
DISK_USED=$(df -h / | awk 'NR==2 {print $3}')
DISK_FREE=$(df -h / | awk 'NR==2 {print $4}')

echo "   - Total Size: $DISK_TOTAL"
echo "   - Used Space: $DISK_USED ($DISK_USAGE_PCT%)"
echo "   - Free Space: $DISK_FREE"

if [ "$DISK_USAGE_PCT" -ge "$DISK_THRESHOLD" ]; then
    echo "   ⚠️ [WARNING] Disk usage has exceeded ${DISK_THRESHOLD}%!"
else
    echo "   ✅ [STATUS] Disk usage is within safe limits."
fi

echo ""
echo "🧠 3. MEMORY (RAM) STATUS"
# Calculate RAM percentage using free
RAM_INFO=$(free | grep Mem:)
RAM_TOTAL=$(echo $RAM_INFO | awk '{print $2}')
RAM_USED=$(echo $RAM_INFO | awk '{print $3}')
RAM_USAGE_PCT=$(( 100 * RAM_USED / RAM_TOTAL ))

free -h | awk '/Mem:/ {print "   - Total RAM: " $2 "\n   - Used RAM:  " $3 " (" "'$RAM_USAGE_PCT'%)\n   - Free RAM:  " $4}'

if [ "$RAM_USAGE_PCT" -ge "$RAM_THRESHOLD" ]; then
    echo "   ⚠️ [WARNING] RAM usage has exceeded ${RAM_THRESHOLD}%!"
else
    echo "   ✅ [STATUS] Memory usage is within safe limits."
fi

echo ""
echo "👥 4. USER ACCOUNTS & LOGINS"
TOTAL_USERS=$(wc -l < /etc/passwd)
LOGGED_IN=$(who | wc -l)
echo "   - Total registered user accounts: $TOTAL_USERS"
echo "   - Currently active logged-in sessions: $LOGGED_IN"
echo "   - Current user running this script: $(whoami)"

echo ""
echo "⚙️  5. PROCESS FORENSICS"
TOTAL_PROCS=$(ps -ef | wc -l)
echo "   - Total running processes on system: $TOTAL_PROCS"
echo "   - Top 3 CPU-consuming processes:"
ps -eo pid,%cpu,%mem,comm --sort=-%cpu | head -n 4 | sed 's/^/     /'

echo ""
echo "===================================================="
echo "   REPORT COMPLETED SUCCESSFULLY!"
echo "===================================================="
