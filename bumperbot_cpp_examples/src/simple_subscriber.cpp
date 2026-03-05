#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp> 
using namespace std::placeholders;

class SimpleSubscriber:public rclcpp::Node 
{

public: 
    SimpleSubscriber(): Node("simple_subscriber") //Nome do nó
    
    {
       sub_ = create_subscription<std_msgs::msg::String>(
        "chatter", 10, std::bind(&SimpleSubscriber::msgCallback, this, _1)); //Cria o "subscriber" passando o nome do topico,o tamanho do buffer, o tipo de interface, classe e o callback 
        RCLCPP_INFO(this->get_logger(),"O nó 'simple_subscriber' foi iniciado"); //Avisa que o "subscriber" foi iniciado
    }

private:

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_; //Instancia o "subscriber"

    void msgCallback(const std_msgs::msg::String &msg) const //Função callback que define o que deve ser feito toda vez que for chamada 
    {
        RCLCPP_INFO_STREAM(get_logger(), "Eu escuto do topico 'Chatter': " <<msg.data.c_str()); //Objetivo do callback
    }

};


int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv); //Inicializa a interface do ROS2
    auto node = std::make_shared<SimpleSubscriber>(); //Cria o objeto "nó"
    rclcpp::spin(node); //Faz com que o nó funcione até o terminal ser desligado 
    rclcpp::shutdown(); //Para o nó e desliga a interface do ROS2 
    return 0;
}