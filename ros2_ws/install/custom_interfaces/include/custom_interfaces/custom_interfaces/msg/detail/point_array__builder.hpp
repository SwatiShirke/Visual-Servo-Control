// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/PointArray.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__POINT_ARRAY__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__POINT_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/point_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_PointArray_point_array
{
public:
  Init_PointArray_point_array()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::msg::PointArray point_array(::custom_interfaces::msg::PointArray::_point_array_type arg)
  {
    msg_.point_array = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::PointArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::PointArray>()
{
  return custom_interfaces::msg::builder::Init_PointArray_point_array();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__POINT_ARRAY__BUILDER_HPP_
