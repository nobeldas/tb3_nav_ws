#!/usr/bin/env python3
"""Send a map-frame NavigateToPose goal to Nav2."""

import argparse
import math

import rclpy
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.parameter import Parameter


def main():
    parser = argparse.ArgumentParser(description='Navigate to a map-frame pose')
    parser.add_argument('x', type=float)
    parser.add_argument('y', type=float)
    parser.add_argument('yaw', type=float, nargs='?', default=0.0, help='heading in radians')
    args = parser.parse_args()

    rclpy.init()
    node = Node('send_nav_goal', parameter_overrides=[Parameter('use_sim_time', value=True)])
    client = ActionClient(node, NavigateToPose, 'navigate_to_pose')
    try:
        if not client.wait_for_server(timeout_sec=30.0):
            raise RuntimeError('Nav2 action server did not start within 30 seconds')
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = node.get_clock().now().to_msg()
        goal.pose.pose.position.x = args.x
        goal.pose.pose.position.y = args.y
        goal.pose.pose.orientation.z = math.sin(args.yaw / 2)
        goal.pose.pose.orientation.w = math.cos(args.yaw / 2)
        sent = client.send_goal_async(goal)
        rclpy.spin_until_future_complete(node, sent)
        handle = sent.result()
        if not handle.accepted:
            raise RuntimeError('Nav2 rejected the goal')
        node.get_logger().info(f'Navigating to ({args.x:.2f}, {args.y:.2f})')
        result = handle.get_result_async()
        rclpy.spin_until_future_complete(node, result)
        status = result.result().status
        if status != 4:
            raise RuntimeError(f'Navigation ended with action status {status}')
        node.get_logger().info('Goal reached')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
