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
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np 

# REFERENCE_POINTS =  [[.511, .372], [.427, .371], [.510, .288], [.427, .288]]
REFERENCE_POINTS = [[0.5109629211425781, 0.3721192321777344], [0.4275, 0.3715], [.5107857055664062, 0.28821429443359375], [0.42755621337890626, 0.2880943908691406]]

L1, L2 = 1, 1

 
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

            self.image_subscription = self.create_subscription(
                  Image, 
                  '/camera1/image_raw', 
                  self.listener_callback, 
                  10)
            self.image_subscription # prevent unused variable warning

            self.joint_subscription = self.create_subscription(
                  JointState, 
                  '/joint_states', 
                  self.joint_callback, 
                  10)
            self.joint_subscription

            # Create the publisher. This publisher will publish an Image
            # to the video_frames topic. The queue size is 10 messages.
            self.publisher_ = self.create_publisher(Image, 'output_images', 10)
            self.joint_publisher = self.create_publisher(Float64MultiArray, '/forward_velocity_controller/commands', 10)
            self.theta1 = 0
            self.theta2 = 0
            self.lamda = 0.2
            self.f = 1
            self.Z = 1
            
            # Used to convert between ROS and OpenCV images
            self.br = CvBridge()

      def joint_callback(self, msg):
            """
            Receive the current joint states
            """
            self.theta1 = msg.position[0]
            self.theta2 = msg.position[1]
            # self.omega_z = msg.velocity[1]
            # print("theta1, theta2", self.theta1, self.theta2, len(msg.velocity)) #, self.omega_z)

      def calculate_error(self, centers):
            """
            Calculate the error vector
            """
            error = []
            for i in range(4):
                  x, y = centers[i]
                  error.append((np.array(REFERENCE_POINTS[i][0]) - np.array(x)))
                  error.append(np.array(REFERENCE_POINTS[i][1]) - np.array(y)) 
            return np.array(error)

      def calculate_image_jacobian(self, centers):
            """
            Calculate the image Jacobian
            """
            # J = np.zeros((8, 6))
            J = []
            for i in range(4):
                  x, y = centers[i]
                  _jx = [-1, 0, x, x*y, -(1+x**2), y]
                  _jy = [0, -1, y, 1+y**2, -x*y, -x]
                  # print("x, y", x, y)
                  # J_temp = [[-self.f/self.Z, 0, x/(self.Z), x*y/(self.f), -self.f - (x**2)/(self.f), y],
                  #          [0, -self.f/self.Z, y/(self.Z), self.f + (y**2)/(self.f), -x*y/(self.f), -x]]
                  # J_temp = [[self.f/self.Z, 0, -self.f*x/(self.Z**2), -self.f*x*y/(self.Z**2), self.f + (x**2)/(self.Z**2), -self.f*y/self.Z],
                  #          [0, self.f/self.Z, -self.f*y/(self.Z**2), -self.f - (self.f*y**2)/(self.Z**2), self.f*x*y/(self.Z**2), self.f*x/self.Z]]
                  # J[2*i:2*i+2, :] = J_temp
                  J.append(_jx)
                  J.append(_jy)
                  
            print("J", J)
            return J
      
      def get_vc(self, centers):
            """
            Calculate the vc vector / end effector / camera velocity
            """
            error = self.calculate_error(centers)
            print("Error", error)
            error = error.reshape((8, 1))
            Le = self.calculate_image_jacobian(centers)
            print("Image Jacobian (Le):\n", Le)
            vc = 0
            Le_inv = np.linalg.pinv(Le)
            # cond_num = np.linalg.cond(Le)
            # print("Condition Number of Le:", cond_num)
            # if cond_num > 1e5:  # This is an arbitrary threshold for ill-conditioning
            #       print("Warning: Jacobian is near-singular or poorly conditioned")
            # regularization_factor = 1e-1
            # Le_inv = np.linalg.pinv(Le.T @ Le + regularization_factor * np.eye(Le.shape[1])) @ Le.T
            vc = -self.lamda*Le_inv@error
            return vc
      
      def get_robot_jacobian(self):
            """
            Generate the inverse Jacobian Matrix
            """
            J = []
            print("theta1, theta2", self.theta1, self.theta2, np.sin(self.theta1), np.cos(self.theta1))
            J11 = -L1*np.sin(self.theta1) - L2*np.sin(self.theta1+self.theta2)
            J12 = -L2*np.sin(self.theta1+self.theta2)
            J21 = L1*np.cos(self.theta1) + L2*np.cos(self.theta1+self.theta2)
            J22 = L2*np.cos(self.theta1+self.theta2)
            print("J11, J12, J21, J22", J11, J12, J21, J22)
            J.append([J11, J12])
            J.append([J21, J22])
            J.append([0.0, 0.0])
            J.append([0.0, 0.0])
            J.append([0.0, 0.0])
            J.append([1.0, 1.0])
            print("Robot Jacobian (J):\n", J)
            J_inv = np.linalg.pinv(J)
            return J_inv

      def detect_circle_centers(self, image):
            """
            Detect circular objects in the image by finding contours.
            """
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            centers = []
            center_m = []
            unique_centers = set()
            
            for contour in contours:
                  # Fit a minimum enclosing circle around the contour
                  (center_x, center_y), radius = cv2.minEnclosingCircle(contour)
                  radius = int(radius)
                  
                  if radius > 10 and radius < 80:  # Ignore very small and big circles
                        if not any(np.linalg.norm(np.array([cx, cy]) - np.array([center_x, center_y])) < 10 for cx, cy in unique_centers):
                              centers.append((int(center_x), int(center_y)))
                              unique_centers.add((int(center_x), int(center_y)))
                              
                              cv2.circle(image, (int(center_x), int(center_y)), radius, (0, 255, 0), 2)
                              cv2.circle(image, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)
                              center_m.append(((center_x*10**-3), (center_y*10**-3)))
            return image, center_m
      
      def is_converged(self, centers):
            """
            Check if the centers are converged to the reference points
            """
            error = self.calculate_error(centers)
            # print("Error  =>>>>>", error.shape)
            error = error.reshape((4, 2))
            sum_x = 0
            sum_y = 0
            for i in range(4):
                  # import ipdb; ipdb.set_trace()
                  # print("error[i]", error[i])
                  x, y = error[i]
                  # print("x, y", x, y)
                  sum_x += x
                  sum_y += y
            print("sum_x, sum_y", sum_x, sum_y)

            if -.1 < sum_x < 0.1 and -0.1 < sum_y < 0.1:
                  return True
            else:
                  return False

      def listener_callback(self, data):
            """
            Callback function.
            """
            """Display the message on the console"""
            self.get_logger().info('Receiving video frame')
            """Convert ROS Image message to OpenCV image"""
            current_frame = self.br.imgmsg_to_cv2(data)
            """Process the image with different techniques"""
            image_with_centers, centers = self.detect_circle_centers(current_frame)
            print("centers", centers)
            # if len(centers) != 4:
            #       print("There should be 4 circles in the image") 
            #       centers = centers1
            # centers1 = centers.copy()
            print("REFERENCE_POINTS", REFERENCE_POINTS)
            vc = self.get_vc(centers)  
            # vc = vc[:2,:]
            print("vc", vc, vc.shape)
            J_inv = self.get_robot_jacobian()
            """ Calculate joint velocities """
            joint_vel = J_inv@vc
            """ Initialize and Publish the joint velocities """
            command_velocity = Float64MultiArray()
            # command_velocity.data = [0.0, 0.0]
            command_velocity.data = [joint_vel[0][0], joint_vel[1][0]]
            print("joint_vel", joint_vel)
            print("command_velocity", command_velocity.data)
            convergence = False
            convergence = self.is_converged(centers)
            print("convergence", convergence)
            if convergence:
                  command_velocity.data = [0.0, 0.0]
            self.joint_publisher.publish(command_velocity)
            """Publish the processed image"""
            self.publisher_.publish(self.br.cv2_to_imgmsg(image_with_centers, encoding="bgr8"))

  
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
