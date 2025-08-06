#!/bin/bash
# sudo bash joy_auto_connect.sh
set -e

echo "🔧 Starting D-Bus and Bluetooth services..."
service dbus start
service bluetooth start

# Wait a moment for services to come up
sleep 2

# Ensure the Bluetooth interface is unblocked and powered on
if command -v rfkill &> /dev/null; then
    echo "🔓 Unblocking Bluetooth via rfkill..."
    rfkill unblock bluetooth
fi

echo "⚡ Forcing Bluetooth adapter power ON..."
bluetoothctl << EOF
power on
EOF

# Wait again to let the adapter come up
sleep 2

# Enable agent, pairable, discoverable, and scanning
echo "📡 Setting up Bluetooth pairing environment..."
bluetoothctl << EOF
agent on
default-agent
pairable on
discoverable on
scan on
EOF

# Give time to scan before pairing
sleep 5

# Attempt to pair and connect to your gamepad
DEVICE_MAC="90:B6:85:00:7D:B4"

echo "🎮 Attempting to pair, trust, and connect to $DEVICE_MAC..."
bluetoothctl << EOF
pair $DEVICE_MAC
trust $DEVICE_MAC
connect $DEVICE_MAC
EOF

# Continue with the container's CMD
exec "$@"
