#include <rclcpp/rclcpp.hpp> 
#include <string>
#include <vector>
#include <rcl_interfaces/msg/set_parameters_result.hpp>
#include <memory>
using namespace std; 
using namespace placeholders;

class SimpleParameter : public rclcpp::Node
{

public:
    SimpleParameter() : Node("simple_parameter")
    {   
        RCLCPP_INFO(this->get_logger(),"O nó 'SimpleParameter' foi iniciado com sucesso!");
        declare_parameter<int>("simple_int_param", 28); 
        declare_parameter<string>("simple_string_param", "Matheus");
        param_callback_handle_ = add_on_set_parameters_callback(bind
            (&SimpleParameter::paramChangeCallback, this, _1));


    }

private: 
    OnSetParametersCallbackHandle:: SharedPtr param_callback_handle_;

   rcl_interfaces ::msg::SetParametersResult paramChangeCallback(const vector<rclcpp::Parameter> & parameters)
    {
        rcl_interfaces::msg::SetParametersResult result;
        for(const auto& param: parameters)
        {
            if(param.get_name() == "simple_int_param" && param.get_type() == rclcpp::ParameterType::PARAMETER_INTEGER)
            {
                RCLCPP_INFO_STREAM(get_logger(),"Parametro 'int' foi trocado. Novo valor = " <<param.as_int());
                result.successful = true; 
            }

              if(param.get_name() == "simple_string_param" && param.get_type() == rclcpp::ParameterType::PARAMETER_STRING)
            {
                RCLCPP_INFO_STREAM(get_logger(),"Parametro 'string' foi trocado. Novo valor = " <<param.as_string());
                result.successful = true; 
            }


        }

        return result;

    }
};


int main (int argc, char* argv[])
{
    rclcpp::init(argc,argv);
    auto node = make_shared<SimpleParameter>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
