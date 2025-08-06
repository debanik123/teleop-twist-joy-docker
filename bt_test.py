import subprocess
import time
import os

def turn_on_bluetooth():
    try:
        subprocess.run(["rfkill", "unblock", "bluetooth"], check=True)
        print("✅ Bluetooth turned on.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Error enabling Bluetooth: {e}")
        return False

def is_device_connected(mac_address):
    try:
        result = subprocess.run(["bluetoothctl", "info", mac_address], capture_output=True, text=True, check=True)
        return "Connected: yes" in result.stdout
    except subprocess.CalledProcessError:
        return False

def connect_device(mac_address):
    try:
        subprocess.run(["bluetoothctl", "connect", mac_address], check=True)
        print(f"✅ Successfully connected to {mac_address}.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to connect to {mac_address}: {e}")
        return False

def restart_docker_container(container_name="joy"):
    try:
        subprocess.run(["docker", "restart", container_name], check=True)
        print(f"♻️ Docker container '{container_name}' restarted.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to restart Docker container: {e}")

if __name__ == "__main__":
    DEVICE_MAC = os.getenv("DEVICE_MAC", "90:B6:85:00:7D:B4")
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))  # Default 5 seconds
    previously_connected = False

    while True:
        print("\n--- Checking Bluetooth connection status ---")

        if not turn_on_bluetooth():
            time.sleep(RETRY_DELAY)
            continue

        connected = is_device_connected(DEVICE_MAC)

        if connected:
            print(f"🎮 Device {DEVICE_MAC} is connected.")
            previously_connected = True
        else:
            print(f"⚠️ Device {DEVICE_MAC} is not connected.")
            if connect_device(DEVICE_MAC):
                # Only restart Docker if we just reconnected
                if not previously_connected:
                    restart_docker_container("joy")
                previously_connected = True
            else:
                previously_connected = False  # Reset so that next successful connection triggers restart

        print(f"Sleeping for {RETRY_DELAY} seconds...\n")
        time.sleep(RETRY_DELAY)
