#!/bin/bash
# remove headphones and start fresh
bluetoothctl remove 90:B6:85:00:7D:B4
# turn bluetooth off
bluetoothctl power off
# turn blutooh on
bluetoothctl power on
# scan for devices for 15 secs so that our device gets discovered.
timeout 15s bluetoothctl scan on
# pair with headphones
bluetoothctl pair 90:B6:85:00:7D:B4
# trust headphones
bluetoothctl trust 90:B6:85:00:7D:B4
# connect to headphones
bluetoothctl connect 90:B6:85:00:7D:B4