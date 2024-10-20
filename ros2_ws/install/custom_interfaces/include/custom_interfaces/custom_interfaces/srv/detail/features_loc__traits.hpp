// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_interfaces:srv/FeaturesLoc.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__FEATURES_LOC__TRAITS_HPP_
#define CUSTOM_INTERFACES__SRV__DETAIL__FEATURES_LOC__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_interfaces/srv/detail/features_loc__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const FeaturesLoc_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: input
  {
    out << "input: ";
    rosidl_generator_traits::value_to_yaml(msg.input, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FeaturesLoc_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: input
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "input: ";
    rosidl_generator_traits::value_to_yaml(msg.input, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FeaturesLoc_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use custom_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_interfaces::srv::FeaturesLoc_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_interfaces::srv::FeaturesLoc_Request & msg)
{
  return custom_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_interfaces::srv::FeaturesLoc_Request>()
{
  return "custom_interfaces::srv::FeaturesLoc_Request";
}

template<>
inline const char * name<custom_interfaces::srv::FeaturesLoc_Request>()
{
  return "custom_interfaces/srv/FeaturesLoc_Request";
}

template<>
struct has_fixed_size<custom_interfaces::srv::FeaturesLoc_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_interfaces::srv::FeaturesLoc_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_interfaces::srv::FeaturesLoc_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'points'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace custom_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const FeaturesLoc_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: points
  {
    if (msg.points.size() == 0) {
      out << "points: []";
    } else {
      out << "points: [";
      size_t pending_items = msg.points.size();
      for (auto item : msg.points) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const FeaturesLoc_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: points
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.points.size() == 0) {
      out << "points: []\n";
    } else {
      out << "points:\n";
      for (auto item : msg.points) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const FeaturesLoc_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use custom_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_interfaces::srv::FeaturesLoc_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_interfaces::srv::FeaturesLoc_Response & msg)
{
  return custom_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_interfaces::srv::FeaturesLoc_Response>()
{
  return "custom_interfaces::srv::FeaturesLoc_Response";
}

template<>
inline const char * name<custom_interfaces::srv::FeaturesLoc_Response>()
{
  return "custom_interfaces/srv/FeaturesLoc_Response";
}

template<>
struct has_fixed_size<custom_interfaces::srv::FeaturesLoc_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_interfaces::srv::FeaturesLoc_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_interfaces::srv::FeaturesLoc_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_interfaces::srv::FeaturesLoc>()
{
  return "custom_interfaces::srv::FeaturesLoc";
}

template<>
inline const char * name<custom_interfaces::srv::FeaturesLoc>()
{
  return "custom_interfaces/srv/FeaturesLoc";
}

template<>
struct has_fixed_size<custom_interfaces::srv::FeaturesLoc>
  : std::integral_constant<
    bool,
    has_fixed_size<custom_interfaces::srv::FeaturesLoc_Request>::value &&
    has_fixed_size<custom_interfaces::srv::FeaturesLoc_Response>::value
  >
{
};

template<>
struct has_bounded_size<custom_interfaces::srv::FeaturesLoc>
  : std::integral_constant<
    bool,
    has_bounded_size<custom_interfaces::srv::FeaturesLoc_Request>::value &&
    has_bounded_size<custom_interfaces::srv::FeaturesLoc_Response>::value
  >
{
};

template<>
struct is_service<custom_interfaces::srv::FeaturesLoc>
  : std::true_type
{
};

template<>
struct is_service_request<custom_interfaces::srv::FeaturesLoc_Request>
  : std::true_type
{
};

template<>
struct is_service_response<custom_interfaces::srv::FeaturesLoc_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__FEATURES_LOC__TRAITS_HPP_
