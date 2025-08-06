import subprocess
import time
import os 

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

            print("🔄 Performing full Bluetooth reset...")
            # Remove the device
            subprocess.run(["bluetoothctl", "remove", mac_address], check=True)
            # Power cycle Bluetooth
            subprocess.run(["bluetoothctl", "power", "off"], check=True)
            # time.sleep(1)  # Short delay
            subprocess.run(["bluetoothctl", "power", "on"], check=True)
            # time.sleep(1)  # Allow time to power on
            
            # Scan for devices (timeout after 15 seconds)
            print("🔍 Scanning for devices...")
            scan_process = subprocess.Popen(["bluetoothctl", "scan", "on"])
            time.sleep(15)  # Scan for 15 seconds
            scan_process.terminate()
        

            subprocess.run(["bluetoothctl", "pair", mac_address], check=True)
            subprocess.run(["bluetoothctl", "trust", mac_address], check=True)
            subprocess.run(["bluetoothctl", "connect", mac_address], check=True)
            print(f"Successfully connected to {mac_address}.")
            
            # Restart the Docker 'joy' container after a successful reconnection
            print("Restarting 'joy' Docker container...")
            try:
                subprocess.run(["docker", "restart", "joy"], check=True)
                print("Docker compose restart successful.")
                # Restart the 'joy' Docker container    
            except subprocess.CalledProcessError as e:
                print(f"Error restarting 'joy' Docker container: {e}")
                # return False
            # subprocess.run(["docker", "compose", "restart", "teleop_twist_joy"], check=True)
            
           
            
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to device {mac_address} or restarting Docker container: {e}")
        return False
    except FileNotFoundError:
        print("Error: 'bluetoothctl' or 'docker' command not found. Ensure BlueZ and Docker are installed.")
        return False

if __name__ == "__main__":
    DEVICE_MAC = os.getenv("DEVICE_MAC", "90:B6:85:00:7D:B4") # Default if not set
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "3")) # Default if not set

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