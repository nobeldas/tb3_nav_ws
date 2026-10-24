from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    world = str(Path(get_package_share_directory('tb3_nav_demo')) / 'worlds' / 'arena.sdf')
    headless = LaunchConfiguration('headless')
    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='false'),
        ExecuteProcess(cmd=['ign', 'gazebo', '-s', '-r', world], output='screen'),
        ExecuteProcess(cmd=['ign', 'gazebo', '-g'], condition=UnlessCondition(headless), output='screen'),
        Node(
            package='ros_gz_bridge', executable='parameter_bridge', output='screen',
            arguments=[
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            ],
        ),
        Node(
            package='ros_gz_bridge', executable='parameter_bridge', output='screen',
            arguments=['/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'],
            parameters=[{'override_frame_id': 'base_scan'}],
        ),
        Node(
            package='tf2_ros', executable='static_transform_publisher',
            arguments=['0', '0', '0.16', '0', '0', '0', 'base_link', 'base_scan'],
        ),
    ])
