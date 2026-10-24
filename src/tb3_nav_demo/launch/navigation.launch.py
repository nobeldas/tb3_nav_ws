from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    demo = Path(get_package_share_directory('tb3_nav_demo'))
    bringup = Path(get_package_share_directory('nav2_bringup'))
    return LaunchDescription([
        DeclareLaunchArgument('map', default_value=str(demo / 'maps' / 'arena.yaml')),
        DeclareLaunchArgument('params_file', default_value=str(demo / 'config' / 'nav2.yaml')),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(bringup / 'launch' / 'bringup_launch.py')),
            launch_arguments={
                'map': LaunchConfiguration('map'),
                'params_file': LaunchConfiguration('params_file'),
                'use_sim_time': 'True',
                'autostart': 'True',
                'use_composition': 'False',
            }.items(),
        ),
    ])
