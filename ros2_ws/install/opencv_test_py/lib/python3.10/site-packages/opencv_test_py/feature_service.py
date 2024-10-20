# Basic ROS 2 program to subscribe to real-time streaming 
# video from your built-in webcam
# This code is modified by Berk Calli from the following author.
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
  
# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np
from custom_interfaces.srv import FeaturesLoc
from geometry_msgs.msg import Point
from opencv_test_py.color_detection import detect_colors


 
class ImageSubscriber(Node):
  """
  Create an ImageSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_subscriber')      
    self.subscription = self.create_subscription(
      Image, 
      '/camera1/image_raw', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning


    self.srv = self.create_service(FeaturesLoc, 'current_feature_loc', self.srv_callback)    
    
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
    self.current_frame = None
   
  def listener_callback(self, data):
    """
    Callback function.
    """
    #get curren features 
    self.current_frame = self.br.imgmsg_to_cv2(data)    

    
  def srv_callback(self, request, response):
    current_frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
    center_list = detect_colors(current_frame) 
    response.points = self.tuples_to_points(center_list)
    self.get_logger().info(f'Incoming request: {response.points}')
    return response


  def tuples_to_points(self, tuple_list):
        points = []
        for tup in tuple_list:
            point = Point(x=float(tup[0]), y= float(tup[1]), z=0.0)
            points.append(point)
        return points


  
  
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_subscriber = ImageSubscriber()
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_subscriber)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
