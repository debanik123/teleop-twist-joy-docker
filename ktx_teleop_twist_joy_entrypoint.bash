#!/bin/bash
set -e

# # Start D-Bus and Bluetooth services
# service dbus start
# service bluetooth start

# # Wait for services to initialize
# sleep 2

# # Setup with bluetoothctl
# bluetoothctl << EOF
# power on
# agent on
# pairable on
# discoverable on
# scan on
# EOF

# sleep 2

# bluetoothctl << EOF
# pair 90:B6:85:01:11:BD
# trust 90:B6:85:01:11:BD
# connect 90:B6:85:01:11:BD
# EOF

source "/opt/ros/$ROS_DISTRO/setup.bash"
source "$KTX_WS/install/setup.bash"
exec "$@"
