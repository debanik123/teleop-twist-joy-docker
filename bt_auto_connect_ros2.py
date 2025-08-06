#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

import subprocess
import time

class BluetoothReconnectService(Node):
    def __init__(self):
        super().__init__('bluetooth_reconnect_node')
        
        # Declare ROS 2 parameter for the device MAC address
        self.declare_parameter('device_mac', '00:00:00:00:00:00')
        self.device_mac = self.get_parameter('device_mac').get_parameter_value().string_value
        
        # Create a ROS 2 service server to trigger the reconnection logic
        self.srv = self.create_service(Trigger, 'reconnect_bluetooth', self.reconnect_callback)
        self.get_logger().info(f'Bluetooth reconnect service is ready. Waiting for a service call on /reconnect_bluetooth...')
        self.get_logger().info(f'Configured device MAC address: {self.device_mac}')

    def turn_on_bluetooth(self):
        """Turns on Bluetooth using rfkill."""
        try:
            subprocess.run(["sudo", "rfkill", "unblock", "bluetooth"], check=True)
            self.get_logger().info("Bluetooth has been turned on.")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.get_logger().error(f"Error turning on Bluetooth: {e}")
            return False

    def check_and_connect_device(self, mac_address):
        """Checks device status and connects if not connected."""
        try:
            # Check if the device is already connected
            result = subprocess.run(["bluetoothctl", "info", mac_address], capture_output=True, text=True, check=True)
            if "Connected: yes" in result.stdout:
                self.get_logger().info(f"✅ Device {mac_address} is already connected.")
                return True
            else:
                self.get_logger().info(f"🎮 Device {mac_address} is not connected. Attempting to connect...")
                
                # Try to connect the device
                subprocess.run(["bluetoothctl", "connect", mac_address], check=True)
                self.get_logger().info(f"Successfully connected to {mac_address}.")
                
                # Restart the Docker 'joy' container after a successful reconnection
                self.get_logger().info("Restarting 'joy' Docker container...")
                subprocess.run(["docker", "compose", "restart", "joy"], check=True)
                self.get_logger().info("Docker compose restart successful.")
                
                return True
        except subprocess.CalledProcessError as e:
            self.get_logger().error(f"Error connecting to device {mac_address} or restarting Docker container: {e}")
            return False
        except FileNotFoundError:
            self.get_logger().error("Error: 'bluetoothctl' or 'docker' command not found. Ensure BlueZ and Docker are installed.")
            return False

    def reconnect_callback(self, request, response):
        """Callback for the ROS 2 service."""
        self.get_logger().info('Received request to reconnect Bluetooth device.')
        
        # Get the device MAC address from the ROS 2 parameter
        self.device_mac = self.get_parameter('device_mac').get_parameter_value().string_value
        
        # Execute the reconnection logic
        success = self.turn_on_bluetooth()
        if success:
            success = self.check_and_connect_device(self.device_mac)

        response.success = success
        if success:
            response.message = f"Bluetooth reconnection for {self.device_mac} successful."
        else:
            response.message = f"Bluetooth reconnection for {self.device_mac} failed."
            
        self.get_logger().info(response.message)
        return response

def main(args=None):
    rclpy.init(args=args)
    bluetooth_service = BluetoothReconnectService()
    rclpy.spin(bluetooth_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()