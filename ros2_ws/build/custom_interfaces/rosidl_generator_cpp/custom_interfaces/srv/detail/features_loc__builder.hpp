// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:srv/FeaturesLoc.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__FEATURES_LOC__BUILDER_HPP_
#define CUSTOM_INTERFACES__SRV__DETAIL__FEATURES_LOC__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/srv/detail/features_loc__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_FeaturesLoc_Request_input
{
public:
  Init_FeaturesLoc_Request_input()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::srv::FeaturesLoc_Request input(::custom_interfaces::srv::FeaturesLoc_Request::_input_type arg)
  {
    msg_.input = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::FeaturesLoc_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::FeaturesLoc_Request>()
{
  return custom_interfaces::srv::builder::Init_FeaturesLoc_Request_input();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_FeaturesLoc_Response_points
{
public:
  Init_FeaturesLoc_Response_points()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::srv::FeaturesLoc_Response points(::custom_interfaces::srv::FeaturesLoc_Response::_points_type arg)
  {
    msg_.points = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::FeaturesLoc_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::FeaturesLoc_Response>()
{
  return custom_interfaces::srv::builder::Init_FeaturesLoc_Response_points();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__FEATURES_LOC__BUILDER_HPP_
