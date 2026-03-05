import rclpy
from rclpy.node import Node 
from std_msgs.msg import String

class SimpleSubscriber(Node):
    def __init__(self):
        super().__init__("simple_subscriber") #Nome do nó

        self.sub_ = self.create_subscription(String, "chatter", self.msgCallback, 10) #Criando o subscriber
    
    def msgCallback(self,msg):  #O que ele vai fazer toda vez que escutar algo do topico 
        self.get_logger().info("Eu escuto do topico 'Chater': %s " %msg.data)



def main(): 
    rclpy.init() #Inicia o ROS2
    simple_subscriber = SimpleSubscriber() #Cria o nó 
    rclpy.spin(simple_subscriber) #Faz com que o nó continue rodando ate o terminal morrer 
    simple_subscriber.destroy_node() #Destroi o nó depois que o terminal morra 
    rclpy.shutdown() #Desliga o ROS2



if __name__ == 'main':
    main()