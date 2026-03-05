import rclpy 
from rcl_interfaces.msg import SetParametersResult
from rclpy.parameter import Parameter
from rclpy.node import Node 


class SimpleParameter(Node): 
    def __init__(self):
        super().__init__("simple_parameter")

        self.get_logger().info("O nó 'SimpleParameter' foi iniciado com sucesso!")
        self.declare_parameter("simple_int_parameter", 28) 
        self.declare_parameter("simple_string_parameter", "Matheus")
        self.add_on_set_parameters_callback(self.paramChangeCallback)


    def paramChangeCallback(self, params):
        result = SetParametersResult()
        for param in params: 
            if param.name == "simple_int_parameter" and param.type_ == Parameter.Type.INTEGER: 
                self.get_logger().info("O parametro 'simple_int_param' foi alterado!, e o novo valor é: %d", param.value)
                result.successful = True

            if param.name == "simple_string_parameter" and param.type_ == Parameter.Type.STRING: 
                self.get_logger().info("O parametro 'simple_string_param' foi alterado!, e o novo valor é: %s", param.value)
                result.successful = True
        
            
            
    
        return result 
    


def main():
    rclpy.init()
    simple_parameter = SimpleParameter()
    rclpy.spin(simple_parameter)
    simple_parameter.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
