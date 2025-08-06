import subprocess
import time

def turn_on_bluetooth():
    """Turns on Bluetooth using rfkill."""
    try:
        subprocess.run(["sudo", "rfkill", "unblock", "bluetooth"], check=True)
        print("Bluetooth has been turned on.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error turning on Bluetooth: {e}")
        return False

def check_and_connect_device(mac_address):
    """Checks device status and connects if not connected."""
    try:
        # Check if the device is already connected
        result = subprocess.run(["bluetoothctl", "info", mac_address], capture_output=True, text=True, check=True)
        if "Connected: yes" in result.stdout:
            print(f"✅ Device {mac_address} is already connected.")
            return True
        else:
            print(f"🎮 Device {mac_address} is not connected. Attempting to connect...")
            # Try to connect the device
            subprocess.run(["bluetoothctl", "connect", mac_address], check=True)
            print(f"Successfully connected to {mac_address}.")
            
            # Restart the Docker 'joy' container after a successful reconnection
            print("Restarting 'joy' Docker container...")
            subprocess.run(["docker", "compose", "restart", "joy"], check=True)
            # subprocess.run(["docker", "compose", "restart", "teleop_twist_joy"], check=True)
            
            print("Docker compose restart successful.")
            
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to device {mac_address} or restarting Docker container: {e}")
        return False
    except FileNotFoundError:
        print("Error: 'bluetoothctl' or 'docker' command not found. Ensure BlueZ and Docker are installed.")
        return False

if __name__ == "__main__":
    DEVICE_MAC = "90:B6:85:00:7D:B4"
    RETRY_DELAY = 1 # seconds

    while True:
        print("\n--- Starting Bluetooth check and connect cycle ---")
        
        # Step 1: Ensure Bluetooth is enabled
        if not turn_on_bluetooth():
            print("Failed to enable Bluetooth. Retrying...")
            time.sleep(RETRY_DELAY)
            continue
        
        # Step 2: Check and connect to the specific device and restart Docker container if needed
        check_and_connect_device(DEVICE_MAC)

        # Pause before the next check
        print(f"Loop finished. Waiting for {RETRY_DELAY} seconds before next check.")
        time.sleep(RETRY_DELAY)