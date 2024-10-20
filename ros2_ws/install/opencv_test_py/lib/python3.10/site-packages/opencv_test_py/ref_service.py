from custom_interfaces.srv import FeaturesLoc
import cv2
import rclpy
from rclpy.node import Node
import numpy as np
from geometry_msgs.msg import Point
from opencv_test_py.color_detection import detect_colors

class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(FeaturesLoc, 'ref_feature_loc', self.srv_callback)
        self.path = '/home/swati/VBM/ros2_ws/src/opencv_test_py/opencv_test_py/image1.jpg'
        image = cv2.imread(self.path)        
        feature_list = detect_colors(image)
        #self.get_logger().info(f'Incoming request: {feature_list}')
        self.feature_list = self.tuples_to_points(feature_list)

    def srv_callback(self, request, response):
        
        self.get_logger().info(f'Incoming request: {response.points}')
        response.points = self.feature_list
        return response

    def tuples_to_points(self, tuple_list):
        points = []
        for tup in tuple_list:
            point = Point(x=float(tup[0]), y= float(tup[1]), z=0.0)
            points.append(point)
        return points


def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()