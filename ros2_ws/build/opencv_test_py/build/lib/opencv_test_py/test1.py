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
from opencv_test_py.color_detection import detect_colors
#from color_detection import detect_colors

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

def edge_detection(img):
    #img = cv2.imread('image1.jpg', cv2.IMREAD_GRAYSCALE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(img, (5, 5), 1.4)
    # Gradient in x direction
    sobel_x = cv2.Sobel(blur_img, cv2.CV_64F, 1, 0, ksize=3)  
    # Gradient in y direction
    sobel_y = cv2.Sobel(blur_img, cv2.CV_64F, 0, 1, ksize=3)   

    #find gradient magnitude
    G_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    G_magnitude = cv2.convertScaleAbs(G_magnitude)

    #NMS
    kernel = np.ones((3, 3), np.uint8)
    max_value = cv2.dilate(G_magnitude, kernel)
    nms_result = np.where(G_magnitude == max_value, G_magnitude, 0)

    #thresholding
    low_th = 20
    high_th = 100

    strong_edges = (nms_result >= high_th).astype(np.uint8)
    weak_edges = ((nms_result >= low_th) & (nms_result < high_th)).astype(np.uint8) 

    combined_edges = (strong_edges + weak_edges).astype(np.uint8)
    final_edges = np.zeros_like(combined_edges, dtype=np.uint8)
    num_labels, labels = cv2.connectedComponents(combined_edges)


    for label in range(1, num_labels):  # Start from 1 since 0 is the background
        if np.any(strong_edges[labels == label]):
            final_edges[labels == label] = 1 *255
       
    return final_edges
 
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
      
    # Create the subscriber. This subscriber will receive an Image
    # from the video_frames topic. The queue size is 10 messages.

    self.subscription = self.create_subscription(
      Image, 
      '/camera1/image_raw', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning

    # Create the publisher. This publisher will publish an Image
    # to the video_frames topic. The queue size is 10 messages.
    self.publisher_ = self.create_publisher(Image, 'output_image', 10)

      
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
   
  def listener_callback(self, data):
    """
    Callback function.
    """
    # Display the message on the console
    #self.get_logger().info('Receiving video frame')
 
    # Convert ROS Image message to OpenCV image
    current_frame = self.br.imgmsg_to_cv2(data)
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    center_list = detect_colors(current_frame)

    #edge_img = edge_detection(current_frame)
    #cv2.imshow("output_image", edge_img)
    self.get_logger().info(f'center list: {center_list}')
    


    # PLACE YOUR CODE HERE. PROCESS THE CURRENT FRAME AND PUBLISH IT. IF YOU ARE HAVING DIFFICULTY PUBLISHING IT YOU CAN USE THE FOLLOWING LINES TO DISPLAY IT VIA OPENCV FUNCTIONS
    
    cv2.waitKey(1)
    

    # Publish the image.
    # The 'cv2_to_imgmsg' method converts an OpenCV
    # image to a ROS 2 image message
    
    self.publisher_.publish(self.br.cv2_to_imgmsg(current_frame, encoding="bgr8"))

  def detect_colors(self, img):
    #The order of the colors is blue, green, red  
    #img = cv2.cvtColor(cv2.imread('./image1.jpg'), cv2.COLOR_BGR2RGB)

    #detect blue
    #define HSV range for blue color
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    result, mask_blue, num_pixels, center = detect_blue(img,lower_blue, upper_blue)
    self.get_logger().info("")
    self.get_logger().info('blue circle detected')
    self.get_logger().info(f"number of pixels = {num_pixels}")
    self.get_logger().info(f"center of the circle = {center}")
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
    #cv2.imshow('pink circle detected', result)
   
    # ##combine all masks
    masks = [mask_blue,mask_red, mask_green, mask_pink]
    
    common_mask = sum(masks)
    result = cv2.bitwise_and(img, img, mask=common_mask)
    cv2.imshow('all colors detected', result)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()  





  
  
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
