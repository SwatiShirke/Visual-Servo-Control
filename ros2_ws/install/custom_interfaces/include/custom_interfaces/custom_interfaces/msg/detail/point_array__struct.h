// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_interfaces:msg/PointArray.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__POINT_ARRAY__STRUCT_H_
#define CUSTOM_INTERFACES__MSG__DETAIL__POINT_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'point_array'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/PointArray in the package custom_interfaces.
typedef struct custom_interfaces__msg__PointArray
{
  geometry_msgs__msg__Point__Sequence point_array;
} custom_interfaces__msg__PointArray;

// Struct for a sequence of custom_interfaces__msg__PointArray.
typedef struct custom_interfaces__msg__PointArray__Sequence
{
  custom_interfaces__msg__PointArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interfaces__msg__PointArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__POINT_ARRAY__STRUCT_H_
