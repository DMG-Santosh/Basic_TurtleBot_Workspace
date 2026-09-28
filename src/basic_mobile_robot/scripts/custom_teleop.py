#!/usr/bin/env python3 

# Tells Linux to use Python 3 when this script is executed directly

import sys  # Provides access to the keyboard input stream
import select  # Lets the program check whether a keyboard key is waiting
import termios  # Provides terminal control functions on Linux
import tty  # Provides functions for changing the terminal keyboard mode
import time  # Provides timing functions for controlling the publishing frequency

import rclpy  # Imports the ROS 2 Python client library
from geometry_msgs.msg import Twist  # Imports the Twist message used for velocity commands


def main():  # Defines the main function of our keyboard teleoperation program
    rclpy.init()  # Initializes the ROS 2 system

    node = rclpy.create_node('custom_wasdx_teleop')  # Creates a ROS 2 node named custom_wasdx_teleop

    publisher = node.create_publisher(Twist, '/cmd_vel', 10)  # Creates a publisher that sends Twist messages to /cmd_vel

    old_settings = termios.tcgetattr(sys.stdin)  # Saves the terminal's original keyboard settings

    command = Twist()  # Creates a Twist message that will store the current movement command

    print('WASDX TurtleBot Control')  # Displays the name of our keyboard controller
    print('w = forward | x = backward')  # Displays the forward and backward controls
    print('a = left | d = right')  # Displays the turning controls
    print('s = stop | q = quit')  # Displays the stop and quit controls

    try:  # Starts a protected section so the terminal can be restored safely
        tty.setcbreak(sys.stdin.fileno())  # Changes the terminal so individual key presses can be read immediately

        while rclpy.ok():  # Keeps the teleoperation program running while ROS 2 is active
            key = ''  # Creates an empty key value for each loop iteration

            if select.select([sys.stdin], [], [], 0.1)[0]:  # Waits up to 0.1 seconds to see whether a key is pressed
                key = sys.stdin.read(1)  # Reads exactly one keyboard character

            if key == 'w':  # Checks whether the user pressed w
                command.linear.x = 0.2  # Sets forward velocity to 0.2 meters per second
                command.angular.z = 0.0  # Makes sure the robot does not rotate

            elif key == 'x':  # Checks whether the user pressed x
                command.linear.x = -0.2  # Sets backward velocity to -0.2 meters per second
                command.angular.z = 0.0  # Makes sure the robot does not rotate

            elif key == 'a':  # Checks whether the user pressed a
                command.linear.x = 0.0  # Stops forward or backward movement
                command.angular.z = 0.8  # Sets positive rotational velocity for left rotation

            elif key == 'd':  # Checks whether the user pressed d
                command.linear.x = 0.0  # Stops forward or backward movement
                command.angular.z = -0.8  # Sets negative rotational velocity for right rotation

            elif key == 's':  # Checks whether the user pressed s
                command.linear.x = 0.0  # Sets forward/backward velocity to zero
                command.angular.z = 0.0  # Sets rotational velocity to zero

            elif key == 'q':  # Checks whether the user pressed q
                break  # Leaves the keyboard-control loop

            publisher.publish(command)  # Publishes the current velocity command to /cmd_vel

            time.sleep(0.1)  # Waits approximately 0.1 seconds before the next loop iteration

    finally:  # Runs cleanup code even if the program is interrupted
        command.linear.x = 0.0  # Sets the final linear velocity to zero
        command.angular.z = 0.0  # Sets the final angular velocity to zero
        publisher.publish(command)  # Sends an explicit stop command before exiting
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)  # Restores the terminal's original keyboard settings
        node.destroy_node()  # Destroys the ROS 2 node
        rclpy.shutdown()  # Shuts down the ROS 2 system


if __name__ == '__main__':  # Checks whether this Python file is being run directly
    main()  # Starts the keyboard teleoperation program