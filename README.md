# Basic Mobile Robot - ROS 2 Workspace

## Overview

This repository contains a ROS 2 workspace used to build and simulate a basic differential-drive mobile robot from scratch.

The project was created as a practical ROS 2 learning project using:

- ROS 2 Jazzy
- Gazebo Sim
- URDF
- `robot_state_publisher`
- `ros_gz_bridge`
- Gazebo DiffDrive
- Python
- Custom keyboard teleoperation

The robot consists of a main base, two driven wheels, and one supporting caster.

---

## Workspace Structure

```text
basic_robot_ws/
├── .gitignore
├── README.md
└── src/
    └── basic_mobile_robot/
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