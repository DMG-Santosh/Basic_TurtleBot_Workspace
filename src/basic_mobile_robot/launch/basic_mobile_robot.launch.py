from launch import LaunchDescription  # Imports the class used to describe the launch system

from launch.actions import ExecuteProcess, SetEnvironmentVariable, TimerAction  # Imports actions for starting processes, setting environment variables, and delaying actions

from launch_ros.actions import Node  # Imports the ROS 2 Node action used to start ROS 2 nodes

from launch_ros.parameter_descriptions import ParameterValue  # Imports ParameterValue so robot_description is treated as a string

from ament_index_python.packages import get_package_share_directory  # Imports a function to find our installed package directory

import os  # Imports Python's operating-system utilities


def generate_launch_description():  # Defines the function that creates the launch description

    package_dir = get_package_share_directory('basic_mobile_robot')  # Finds the installed location of our basic_mobile_robot package

    urdf_file = os.path.join(package_dir, 'urdf', 'basic_mobile_robot.urdf')  # Builds the complete path to our URDF file

    world_file = os.path.join(package_dir, 'worlds', 'slam_world.sdf')

    with open(urdf_file, 'r') as file:  # Opens the URDF file in read mode

        robot_description = file.read()  # Reads the complete URDF text into a Python variable

    return LaunchDescription([  # Returns the complete list of actions that ROS 2 should launch

        SetEnvironmentVariable(  # Sets an environment variable for Gazebo

            name='GZ_CONFIG_PATH',  # Specifies the name of the environment variable

            value='/usr/share/gz'  # Specifies the Gazebo configuration directory we already identified
        ),

        ExecuteProcess(  # Starts the Gazebo simulation process

            cmd=['gz', 'sim', '-r', world_file],  # Runs Gazebo Sim with the empty world and starts it immediately
            output='screen'  # Shows Gazebo output in the terminal
        ),

        Node(  # Starts the ROS 2 robot_state_publisher node

            package='robot_state_publisher',  # Uses the robot_state_publisher ROS 2 package

            executable='robot_state_publisher',  # Runs the robot_state_publisher executable

            parameters=[  # Provides parameters to robot_state_publisher

                {
                    'robot_description': ParameterValue(  # Provides our URDF as the robot_description parameter

                        robot_description,  # Passes the URDF text

                        value_type=str  # Explicitly tells ROS 2 that the value is a string
                    )
                }
            ],

            output='screen'  # Shows node output in the terminal
        ),

        Node( # Starts the ROS 2 ↔ Gazebo communication bridge

            package='ros_gz_bridge', # Uses the ros_gz_bridge ROS 2 package

            executable='parameter_bridge', # Runs the bridge executable

            arguments=[ # Provides the topic bridge configuration

                # ] — ROS to Gazebo, [ — Gazebo to ROS, @ — bidirectional bridging

                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist', # Bridges ROS 2 Twist to Gazebo Twist for /cmd_vel
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'
            ],

            output='screen' # Shows bridge messages in the terminal
        ),

        TimerAction(  # Delays the robot spawning slightly so Gazebo has time to start

            period=5.0,  # Waits for 5 seconds

            actions=[  # Actions to run after the delay

                Node(  # Starts the Gazebo ROS 2 spawning tool

                    package='ros_gz_sim',  # Uses the ros_gz_sim package

                    executable='create',  # Runs the create executable

                    arguments=[  # Arguments passed to the Gazebo spawn command

                        '-topic', 'robot_description',  # Tells Gazebo to create the robot from the robot_description topic

                        '-name', 'basic_mobile_robot',  # Gives the spawned robot its Gazebo entity name

                        '-z', '0.2'  # Spawns the robot 0.275 meters above the ground
                    ],

                    output='screen'  # Shows the spawn process output in the terminal
                )
            ]
        )
    ])