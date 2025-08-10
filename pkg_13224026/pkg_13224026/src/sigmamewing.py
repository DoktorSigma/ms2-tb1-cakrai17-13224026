#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class CommandBridgeNode(Node):
    def __init__(self):
        super().__init__('command_bridge_node')
        self.get_logger().info('Command Bridge Node started!')

        self.cmd_vel_publisher = self.create_publisher(
            Twist, 
            'cmd_vel', 
            10
        )
        self.cmd_type_publisher = self.create_publisher(
            String, 
            'cmd_type', 
            10
        )

        self.autonomous_vel_subscriber = self.create_subscription(
            Twist, 
            'autonomous_vel', 
            self.autonomous_vel_callback, 
            10
        )
        
        self.get_logger().info('Subscribed to: /autonomous_vel (Twist)')
        self.get_logger().info('Publishing to: /cmd_vel (Twist) and /cmd_type (String)')
        self.get_logger().info('=' * 60)

    def autonomous_vel_callback(self, msg):
        self.cmd_vel_publisher.publish(msg)

        cmd_type_msg = String()
        cmd_type_msg.data = 'autonomous'
        self.cmd_type_publisher.publish(cmd_type_msg)
        
        self.get_logger().debug(f'Received autonomous command. Forwarded Twist and published type: {cmd_type_msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = CommandBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
