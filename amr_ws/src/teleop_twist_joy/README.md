ros2/teleop_twist_joy
=====================



# To Run

ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps3-holonomic'

ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps3-holonomic' require_enable_button:=false  -- For Holomnomic

ros2 launch teleop_twist_joy teleop-launch.py joy_config:='ps3' require_enable_button:=false  -- For Four Wheel drive

# For Testing Joystick  buttons

sudo apt install joystick  # Install joystick testing tool

jstest /dev/input/js0  


# udev rules 
```
  For blooth joystick -->
  udevadm info -a -p $(udevadm info -q path -n /dev/input/js0) | grep 054C:0CE6
  udevadm info -a -p $(udevadm info -q path -n /dev/input/js0) | grep ATTRS{idVendor}
  udevadm info -a -p $(udevadm info -q path -n /dev/input/js0) | grep ATTRS{idProduct}

  sudo nano /etc/udev/rules.d/99-joystick.rules

  sudo udevadm control --reload-rules
  KERNEL=="js0", KERNELS=="*054C:0CE6*", MODE="0660", TAG+="uaccess", SYMLINK+="input/joy_ps"
  or,
  KERNEL=="js0", KERNELS=="0005:054C:0CE6.000B", MODE="0660", TAG+="uaccess", SYMLINK+="input/joy_ps"

  For manual joystick -->
  KERNEL=="js*", SUBSYSTEM=="input", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="4321", MODE="0660", TAG+="uaccess", SYMLINK+="input/joy_manual"

  sudo udevadm control --reload-rules
  sudo udevadm trigger
  ls -l /dev/input/joy_ps
  jstest /dev/input/joy_ps
  jstest /dev/input/joy_manual



  test -->
  KERNEL=="js1", KERNELS=="0005:054C:0CE6.000B", MODE="0660", TAG+="uaccess", SYMLINK+="input/joy_ps"
  KERNEL=="js0", SUBSYSTEM=="input", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="4321", MODE="0660", TAG+="uaccess", SYMLINK+="input/joy_manual"
  sudo udevadm control --reload-rules
  sudo udevadm trigger
  reboot


```

# Connecting Bluethooth Device From Terminal

Step 1 : bluetoothctl
 
Step 2 : power on

Step 3 : agent on

Step 4 : 

pairable on
discoverable on

Step 5 : Put the DualSense Controller in Pairing Mode

Step 6 : scan on

Step 7 : pair 90:B6:85:01:11:BD

Step 8 : trust 90:B6:85:01:11:BD

Step 9 : connect 90:B6:85:01:11:BD

Step 10 : exit



# Overview
The purpose of this package is to provide a generic facility for tele-operating Twist-based ROS 2 robots with a standard joystick.
It converts joy messages to velocity commands.

This node provides no rate limiting or autorepeat functionality.
It is expected that you take advantage of the features built into [joy](https://index.ros.org/p/joy/github-ros-drivers-joystick_drivers) for this.

## Executables
The package comes with the `teleop_node` that republishes `sensor_msgs/msg/Joy` messages as scaled `geometry_msgs/msg/Twist` messages.
The message type can be changed to `geometry_msgs/msg/TwistStamped` by the `publish_stamped_twist` parameter.

## Subscribed Topics
- `joy (sensor_msgs/msg/Joy)`
  - Joystick messages to be translated to velocity commands.

## Published Topics
- `cmd_vel (geometry_msgs/msg/Twist or geometry_msgs/msg/TwistStamped)`
  - Command velocity messages arising from Joystick commands.

## Parameters
- `require_enable_button (bool, default: true)`
  - Whether to require the enable button for enabling movement.

- `enable_button (int, default: 0)`
  - Joystick button to enable regular-speed movement.

- `enable_turbo_button (int, default: -1)`
  - Joystick button to enable high-speed movement (disabled when -1).

- `axis_linear.<axis>`
  - Joystick axis to use for linear movement control.
  - `axis_linear.x (int, default: 5)`
  - `axis_linear.y (int, default: -1)`
  - `axis_linear.z (int, default: -1)`

- `scale_linear.<axis>`
  - Scale to apply to joystick linear axis for regular-speed movement.
  - `scale_linear.x (double, default: 0.5)`
  - `scale_linear.y (double, default: 0.0)`
  - `scale_linear.z (double, default: 0.0)`

- `scale_linear_turbo.<axis>`
  - Scale to apply to joystick linear axis for high-speed movement.
  - `scale_linear_turbo.x (double, default: 1.0)`
  - `scale_linear_turbo.y (double, default: 0.0)`
  - `scale_linear_turbo.z (double, default: 0.0)`

- `axis_angular.<axis>`
  - Joystick axis to use for angular movement control.
  - `axis_angular.yaw (int, default: 2)`
  - `axis_angular.pitch (int, default: -1)`
  - `axis_angular.roll (int, default: -1)`

- `scale_angular.<axis>`
  - Scale to apply to joystick angular axis.
  - `scale_angular.yaw (double, default: 0.5)`
  - `scale_angular.pitch (double, default: 0.0)`
  - `scale_angular.roll (double, default: 0.0)`

- `scale_angular_turbo.<axis>`
  - Scale to apply to joystick angular axis for high-speed movement.
  - `scale_angular_turbo.yaw (double, default: 1.0)`
  - `scale_angular_turbo.pitch (double, default: 0.0)`
  - `scale_angular_turbo.roll (double, default: 0.0)`

- `inverted_reverse (bool, default: false)`
  - Whether to invert turning left-right while reversing (useful for differential wheeled robots).

- `publish_stamped_twist (bool, default: false)`
  - Whether to publish `geometry_msgs/msg/TwistStamped` for command velocity messages.

- `frame (string, default: 'teleop_twist_joy')`
  - Frame name used for the header of TwistStamped messages.


# Usage

## Install
For most users building from source will not be required, execute `apt-get install ros-<rosdistro>-teleop-twist-joy` to install.

## Run
A launch file has been provided which has three arguments which can be changed in the terminal or via your own launch file.
To configure the node to match your joystick a config file can be used.
There are several common ones provided in this package (atk3, ps3-holonomic, ps3, xbox, xd3), located here: https://github.com/ros2/teleop_twist_joy/tree/humble/config.

PS3 is default, to run for another config (e.g. xbox) use this:
````
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='xbox'
````

__Note:__ this launch file also launches the `joy` node so do not run it separately.


## Arguments
- `joy_config (string, default: 'ps3')`
  - Config file to use
- `joy_dev (string, default: '0')`
  - Joystick device to use
- `config_filepath (string, default: '/opt/ros/<rosdistro>/share/teleop_twist_joy/config/' + LaunchConfig('joy_config') + '.config.yaml')`
  - Path to config files
- `publish_stamped_twist (bool, default: false)`
  - Whether to publish `geometry_msgs/msg/TwistStamped` for command velocity messages.
