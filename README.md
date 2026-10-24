# TurtleBot3 navigation demo

ROS 2 Humble, Gazebo Sim Fortress, and Nav2. The arena contains a compact TurtleBot3 Burger style differential drive model, LiDAR, two fixed obstacles, and an 8 m occupancy map. Nav2 uses AMCL, NavFn, DWB, and LiDAR obstacle layers to reach map-frame goals.

## Requirements

On Ubuntu 22.04 with ROS 2 Humble and Gazebo Fortress:

```bash
sudo apt install ros-humble-ros-gz ros-humble-nav2-bringup ros-humble-rviz2
```

## Build and run

```bash
source /opt/ros/humble/setup.bash
cd tb3_nav_ws
colcon build --symlink-install
source install/setup.bash
ros2 launch tb3_nav_demo sim.launch.py
```

In a second terminal, source both setup files and start Nav2:

```bash
ros2 launch tb3_nav_demo navigation.launch.py
```

In a third terminal, source both setup files and send a goal across the obstacle arena:

```bash
ros2 run tb3_nav_demo send_goal.py 3 3 0
```

Use `ros2 launch tb3_nav_demo sim.launch.py headless:=true` without a Gazebo window. In RViz, set the fixed frame to `map`, add `Map` (`/map`), `LaserScan` (`/scan`), and `TF`, then use the Nav2 Goal tool. The initial pose is configured at `(-3, -3, 0)` in `config/nav2.yaml`; reset it with RViz's Initial Pose tool if localization is lost.

The local and global costmaps use the live LiDAR scan for obstacle marking and clearing. The global costmap also loads `maps/arena.yaml`; inflation keeps the robot clear of walls and blocks. The map image can be regenerated with `python3 src/tb3_nav_demo/scripts/make_map.py` after changing the geometry.

This workspace contains the simulation assets and Nav2 configuration. Nav2 itself remains an upstream binary dependency.
