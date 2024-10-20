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


def detect_blue(img, lower_value, upper_value):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)         
    # Create a mask for blue color
    mask = cv2.inRange(hsv, lower_value, upper_value)    
    # Apply the mask to get the blue regions in the original image
    result = cv2.bitwise_and(img, img, mask=mask)    
    # Calculate the number of pixels of the color
    num_pixels = cv2.countNonZero(mask)
    # Find contours of the detected color
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    
    center = None
    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        # Calculate the moments of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            # Calculate the center of the detected part
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
    return result, mask, num_pixels, center


 
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

    self.client = self.create_client(FeaturesLoc, 'ref_feature_loc')
    while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
    self.request = FeaturesLoc.Request()

    # Create the publisher. This publisher will publish an Image
    # to the video_frames topic. The queue size is 10 messages.
    self.publisher_ = self.create_publisher(Image, 'output_image', 10)      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
  def listener_callback(self, data):
    """
    Callback function.
    """
    #get curren features 
    current_frame = self.br.imgmsg_to_cv2(data)
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    center_list = self.detect_colors(current_frame) 
    center_list = self.tuples_to_points(center_list)
    self.get_logger().info(f'Incoming request: {center_list}')


    ##get ref feature list
    future = self.client.call_async(self.request)
    rclpy.spin_until_future_complete( self, future)
    response = future.result()

    ##print
    self.get_logger().info(f'Incoming request: {response.points}')
    self.publisher_.publish(self.br.cv2_to_imgmsg(current_frame, encoding="bgr8"))

  def tuples_to_points(self, tuple_list):
        points = []
        for tup in tuple_list:
            point = Point(x=float(tup[0]), y= float(tup[1]), z=0.0)
            points.append(point)
        return points

  def detect_colors(self, img):
    #The order of the colors is blue, green, red  
    #img = cv2.cvtColor(cv2.imread('./image1.jpg'), cv2.COLOR_BGR2RGB)

    #detect blue
    #define HSV range for blue color
    center_list = []
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    result, mask_blue, num_pixels, center = detect_blue(img,lower_blue, upper_blue)
    self.get_logger().info("")
    self.get_logger().info('blue circle detected')
    self.get_logger().info(f"number of pixels = {num_pixels}")
    self.get_logger().info(f"center of the circle = {center}")
    center_list.append(center)
    #cv2.imshow('blue circle detected', result)
    

    #detect Red
    #define HSV range for blue color
    print("")
    lower_red = np.array([0, 100, 100])
    upper_red = np.array( [10, 255, 255])
    result, mask_red, num_pixels, center = detect_blue(img,lower_red, upper_red)
    self.get_logger().info('red circle detected')
    self.get_logger().info(f"number of pixels = {num_pixels}")
    self.get_logger().info(f"center of the circle = {center}")
    center_list.append(center)
    #cv2.imshow('red circle detected', result)

    ##detect green
    #define HSV range for green color
    print("")
    lower_green = np.array([40, 100, 100])
    upper_green = np.array( [80, 255, 255])
    result, mask_green, num_pixels, center = detect_blue(img,lower_green, upper_green)
    self.get_logger().info('green circle detected')
    self.get_logger().info(f"number of pixels = {num_pixels}")
    self.get_logger().info(f"center of the circle = {center}")
    center_list.append(center)
    #cv2.imshow('green circle detected', result)

    ##detect pink
    #define HSV range for pink color
    print("")
    lower_pink = np.array([140, 100, 100])
    upper_pink = np.array( [170, 255, 255])
    result, mask_pink, num_pixels, center = detect_blue(img,lower_pink, upper_pink)
    self.get_logger().info('pink circle detected')
    self.get_logger().info(f"number of pixels = {num_pixels}")
    self.get_logger().info(f"center of the circle = {center}")
    center_list.append(center)
    #cv2.imshow('pink circle detected', result)
   
    # ##combine all masks
    # masks = [mask_blue,mask_red, mask_green, mask_pink]
    
    # common_mask = sum(masks)
    # result = cv2.bitwise_and(img, img, mask=common_mask)
    # cv2.imshow('all colors detected', result)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()  
    return center_list

  
  
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
