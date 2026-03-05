# --- BLOCO 1: IMPORTAÇÕES ---
from launch import LaunchDescription
from launch_ros.actions import Node
# DeclareLaunchArgument: Permite criar variáveis que podem ser alteradas pelo terminal.
from launch.actions import DeclareLaunchArgument
# os: Biblioteca padrão do Python para manipular caminhos de arquivos (pastas).
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration 


def generate_launch_description():

    # --- BLOCO 2: ARGUMENTO DE ENTRADA ---
    # Define uma variável 'model' que aponta por padrão para o seu arquivo de robô.
    # Isso permite que você mude o robô no terminal sem editar este arquivo.
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(
            get_package_share_directory("bumperbot_description"), 
            "urdf", 
            "bumperbot.urdf.xacro"
        ),
        #Mensagem de ajuda que aparece quando você roda 'ros2 launch --help'
        description="Caminho absoluto para o arquivo URDF/Xacro do robô"
    )

    # --- BLOCO 3: PROCESSAMENTO DO ROBÔ (XACRO -> URDF) ---
    # Aqui o código executa o programa 'xacro' para converter o arquivo .xacro (macros)
    # em um XML puro (URDF) que o ROS consegue entender. O resultado é guardado como String.

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]),
        value_type=str
    )

    # --- BLOCO 4: NÓ ROBOT STATE PUBLISHER ---
    # Este nó é essencial: ele lê o 'robot_description' (URDF) e publica a estrutura 
    # física do robô (TFs). Ele diz ao sistema como as peças estão conectadas.
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}] # "robot_description" é o nome padrão que o robot_state_publisher espera para ler o URDF.
    )

    # --- BLOCO 5: NÓ JOINT STATE PUBLISHER GUI ---
    # Abre a interface gráfica com sliders (barras) para você mover as juntas 
    # do robô manualmente e testar se a árvore de transformações está correta.
    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    # --- BLOCO 6: NÓ RVIZ2 (VISUALIZAÇÃO) ---
    # Inicia a ferramenta de visualização 3D. 
    # O argumento '-d' aponta para um arquivo de configuração (.rviz) para que 
    # o RViz já abra com as câmeras e displays (como o RobotModel) configurados.
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(
            get_package_share_directory("bumperbot_description"),
            "rviz",
            "display.rviz"
        )] 
    )

    # --- BLOCO 7: RETORNO DA DESCRIÇÃO ---
    # Retorna a lista de todas as ações e nós que o ROS deve iniciar.
    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz_node
    ])