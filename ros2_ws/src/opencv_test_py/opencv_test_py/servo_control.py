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
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
 
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

    self.joint_sub = self.create_subscription(
      JointState, 
      '/joint_states', 
      self.joint_callback, 
      10)
    self.joint_sub
    self.subscription # prevent unused variable warning

    self.joint_pub = self.create_publisher(Float64MultiArray, '/forward_velocity_controller/commands', 10)
    self.joint_pub

    self.br = CvBridge()
    self.path = '/home/swati/VBM/ros2_ws/src/opencv_test_py/opencv_test_py/image1.jpg'
    image = cv2.imread(self.path)  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      
    self.ref_feature_list = detect_colors(image)
    
    self.z = 1 #depth
    self.f = 1  ##focal length
    self.K_mat = np.array([[self.f,0,0], [0,self.f,0], [0,0,1]])
    self.lambda_1 = 0.0008
    self.l1 = 1
    self.l2 = 1

  def joint_callback(self, data):
    self.theta1 = data.position[0]
    self.theta2 = data.position[1]

   
  def listener_callback(self, data):
    """
    Callback function.
    """    
    #get curren features 
    current_frame = self.br.imgmsg_to_cv2(data)    
    #self.get_logger().info(f"reference features: {current_frame}")
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    #cv2.imwrite(self.path, current_frame)
    self.current_feature_list = detect_colors(current_frame) 
    error = np.array([[a-c,b-d] for (a,b), (c,d) in zip(self.current_feature_list, self.ref_feature_list)])
    self.error = error.flatten()    
    self.cal_robot_vel()
    self.cal_joint_vel()
    vel_cmd = Float64MultiArray()
    vel_cmd.data = [float(self.joint_vel[0]), float(self.joint_vel[0])]
    self.joint_pub.publish(vel_cmd)
    self.get_logger().info(f"reference features: {self.ref_feature_list}")
    self.get_logger().info(f"current features: {self.current_feature_list}")
    self.get_logger().info(f"error: {self.error}")
    self.get_logger().info(f"image_jacobian: {self.img_jacob}")
    self.get_logger().info(f"robot_jacobian: {self.robot_jacob}")
    self.get_logger().info(f"robot vel: {self.robot_vel.T}")
    self.get_logger().info(f"joint_vel: {self.joint_vel.T}")
    

   
  def cal_robot_vel(self):
    #create image jacobian first 
    f = self.f
    z = self.z
    row_list = []
    for pixel in self.current_feature_list:
      #v_vector = np.array([pixel[0], pixel[1], 0])
      #x_vector = np.matmul(self.K_mat, v_vector)
      x,y = pixel
      # J_row_1 = [-1, 0, x, x*y, -(1+x**2), y]
      # J_row_1 = [0, -1, y, 1+y**2, -x*y, -x]
      J_row_1 = [-f/ z,   0,   x/z,  x*y/f, -(f+ x**2/f),  y  ]
      J_row_2 = [0, -f/z, y/z,   (f+ y**2/f) , (-x*y/f), -x]
      row_list.append(J_row_1)
      row_list.append(J_row_2)
    self.img_jacob = np.mat(row_list)
    #self.get_logger().info(f"feature error: {img_jacob}")
    self.robot_vel = -self.lambda_1 * np.matmul(np.linalg.pinv(self.img_jacob), self.error.T)
    
  def cal_joint_vel(self):
    J_w1 = [0,0,1]
    J_w2 = [0,0,1]
    # r1 = [self.l1 * np.cos(self.theta1), -self.l1 * np.sin(self.theta1), 0 ]
    # r2 = [self.l1 * np.cos(self.theta1) + self.l2 * np.cos(self.theta1+ self.theta2),   
    #      -self.l1 * np.sin(self.theta1) -self.l2 * np.sin(self.theta1+ self.theta2) ,0 ]
    r1 = [self.l1 * np.cos(self.theta1), self.l1 * np.sin(self.theta1), 0  ]
    r2 = [self.l1 * np.cos(self.theta1) + self.l2 * np.cos(self.theta1+ self.theta2),   
          self.l1 * np.sin(self.theta1) + self.l2 * np.sin(self.theta1+ self.theta2) ,0 ]

    J_v1 = np.cross(J_w1, r1)
    J_v2 = np.cross(J_w2, r2)
    
    self.robot_jacob = np.array([[J_v1[0], J_v2[0]],
                     [J_v1[1], J_v2[1]],
                     [J_v1[2], J_v2[2]],
                     [J_w1[0], J_w2[0]],
                     [J_w1[1], J_w2[1]],
                     [J_w1[2], J_w2[2]]])
    self.joint_vel =np.matmul(np.linalg.pinv(self.robot_jacob), self.robot_vel.T)
    









  
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
