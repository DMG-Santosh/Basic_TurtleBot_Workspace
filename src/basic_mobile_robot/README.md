# Basic Mobile Robot ROS 2 Package

## Overview

This package contains a basic differential-drive mobile robot created for practical ROS 2 learning and Gazebo simulation.

The package contains the robot description, Gazebo launch configuration, and a custom keyboard teleoperation program.

## Package Structure

```text
basic_mobile_robot/
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── basic_mobile_robot.launch.py
├── scripts/
│   └── custom_teleop.py
├── urdf/
│   └── basic_mobile_robot.urdf
├── include/
└── src/