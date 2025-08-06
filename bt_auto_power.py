import subprocess
import time

def turn_on_bluetooth():
    """Turns on Bluetooth using rfkill unblock bluetooth."""
    try:
        # Execute the command to unblock (turn on) Bluetooth
        subprocess.run(["sudo", "rfkill", "unblock", "bluetooth"], check=True)
        print("Bluetooth has been turned on.")
        return True  # Indicate success
    except subprocess.CalledProcessError as e:
        print(f"Error turning on Bluetooth: {e}")
        return False # Indicate failure
    except FileNotFoundError:
        print("Error: 'rfkill' command not found. Ensure rfkill is installed.")
        return False # Indicate failure

if __name__ == "__main__":
    while True:
        # Keep trying to turn on Bluetooth
        success = turn_on_bluetooth()
        if success:
            print("Successfully turned on Bluetooth. Looping again in 2 seconds...")
        else:
            print("Failed to turn on Bluetooth. Retrying in 2 seconds...")
        
        # Add a delay to prevent the loop from running too fast
        time.sleep(2)