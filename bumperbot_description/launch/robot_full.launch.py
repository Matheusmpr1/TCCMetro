import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node 

def generate_launch_description():
    pkg_description = get_package_share_directory('bumperbot_description')

    # 1. Inclui o seu arquivo de lançamento do Gazebo
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_description, 'launch', 'gazebo.launch.py')
        )
    )

    # 2. Inclui o display (RViz e Robot State Publisher)
    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_description, 'launch', 'display.launch.py')
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # 3. PONTE (BRIDGE) CORRIGIDA PARA O JAZZY
    # Aqui fazemos o mapeamento do caminho longo do Gazebo para o tópico /scan do ROS
    gz_ros_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # O caminho foi extraído diretamente do seu log de erro
            '/model/bumperbot/link/base_footprint/sensor/vlp16_sensor/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        remappings=[
            # Esta linha é vital: transforma o nome longo no nome que o seu script Python lê
            ('/model/bumperbot/link/base_footprint/sensor/vlp16_sensor/scan', '/scan')
        ],
        output='screen'
    )

    # 4. Nó do Alerta do Lidar
    lidar_alarm_node = Node(
        package='bumperbot_description', 
        executable='lidar_alarm.py',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    return LaunchDescription([
        gazebo_launch,
        rviz_launch,
        gz_ros_bridge,
        lidar_alarm_node
    ])