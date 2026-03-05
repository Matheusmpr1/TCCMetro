#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy

class LidarAlarm(Node):
    def __init__(self):
        super().__init__('lidar_alarm')
        
        # Configura QoS para garantir compatibilidade com o sensor do Gazebo
        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = ReliabilityPolicy.BEST_EFFORT

        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            qos_profile) # Usando o perfil de QoS aqui
        
        self.declare_parameter('threshold', 0.5)
        self.get_logger().info("Nó de Alerta do Lidar iniciado!")

    def listener_callback(self, msg):
        threshold = self.get_parameter('threshold').get_parameter_value().double_value
        
        # Filtra valores fora do range (como 0.0 ou inf)
        distances = [r for r in msg.ranges if msg.range_min < r < msg.range_max]
        
        if distances:
            min_distance = min(distances)
            if min_distance < threshold:
                self.get_logger().warn(f'OBSTÁCULO DETECTADO! Distância: {min_distance:.2f}m')
            # Removi o 'once=True' para você poder ver o status mudar no terminal
        else:
            self.get_logger().info("Lidar sem leituras válidas no momento.", once=True)

def main(args=None):
    rclpy.init(args=args)
    try:
        node = LidarAlarm()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Garante que o nó feche limpo ao dar Ctrl+C
        if 'node' in locals():
            node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()