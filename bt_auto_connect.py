import subprocess
import time

def run_btctl_cmd(*args, suppress_error=False):
    """Helper to run bluetoothctl commands."""
    try:
        return subprocess.run(["bluetoothctl", *args], capture_output=True, text=True, check=not suppress_error)
    except subprocess.CalledProcessError as e:
        if suppress_error:
            return e
        raise

def turn_on_bluetooth():
    """Turns on Bluetooth using rfkill and ensures the service is running and powered."""
    try:
        subprocess.run(["sudo", "rfkill", "unblock", "bluetooth"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "bluetooth"], check=True)
        subprocess.run(["bluetoothctl", "power", "on"], check=True)
        print("✅ Bluetooth has been turned on and powered up.")
        time.sleep(2)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Error turning on Bluetooth: {e}")
        return False

def clean_pairing(mac):
    """Removes previous pairing (if any)."""
    print(f"🧹 Removing old pairing for {mac} (if any)...")
    run_btctl_cmd("remove", mac, suppress_error=True)

def scan_device(duration=15):
    """Scans for Bluetooth devices for the given duration (in seconds)."""
    print(f"🔍 Scanning for devices for {duration} seconds...")
    scan_proc = subprocess.Popen(["bluetoothctl", "scan", "on"])
    time.sleep(duration)
    scan_proc.terminate()
    print("🔍 Scan complete.")

def pair_and_trust(mac):
    """Pairs and trusts the device."""
    print(f"🤝 Pairing with device {mac}...")
    result = run_btctl_cmd("pair", mac, suppress_error=True)
    if "Pairing successful" in result.stdout or "already paired" in result.stdout:
        print("✅ Device paired.")
    else:
        print(f"⚠️ Pairing may have failed:\n{result.stdout}")
    
    run_btctl_cmd("trust", mac)
    print("🔒 Device trusted.")

def connect_and_restart(mac):
    """Connects to the device and restarts Docker container if needed."""
    result = run_btctl_cmd("info", mac)
    if "Connected: yes" in result.stdout:
        print(f"✅ Device {mac} is already connected.")
        return True

    print(f"🔌 Connecting to {mac}...")
    connect_result = run_btctl_cmd("connect", mac, suppress_error=True)
    if "Connection successful" in connect_result.stdout:
        print(f"🎉 Successfully connected to {mac}.")
        print("🔄 Restarting 'joy' Docker container...")
        subprocess.run(["docker", "compose", "restart", "joy"], check=True)
        print("✅ Docker container restarted.")
        return True
    else:
        print(f"❌ Failed to connect: {connect_result.stdout}")
        return False

if __name__ == "__main__":
    DEVICE_MAC = "90:B6:85:00:7D:B4"
    RETRY_DELAY = 5  # seconds

    while True:
        print("\n--- 🔄 Starting Bluetooth connection cycle ---")

        if not turn_on_bluetooth():
            print("⚠️ Failed to turn on Bluetooth. Retrying...")
            time.sleep(RETRY_DELAY)
            continue

        clean_pairing(DEVICE_MAC)
        scan_device(duration=15)
        pair_and_trust(DEVICE_MAC)

        if connect_and_restart(DEVICE_MAC):
            print("✅ Full connection cycle completed.")
        else:
            print("⚠️ Connection failed.")

        print(f"⏳ Waiting {RETRY_DELAY} seconds before next attempt...")
        time.sleep(RETRY_DELAY)
