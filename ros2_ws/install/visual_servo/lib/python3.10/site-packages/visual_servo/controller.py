import sys
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node
from custom_interfaces.srv import FeaturesLoc
import numpy as np
import time
import asyncio

class MinimalControl(Node):

    def __init__(self):
        super().__init__('minimal_control')
        timer_period = 5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.client1 = self.create_client(FeaturesLoc, 'ref_feature_loc')        
        self.client2 = self.create_client(FeaturesLoc, 'current_feature_loc')

        while not self.client1.wait_for_service(timeout_sec=1.0):
            self.get_logger()().info('ef_feature_loc not available, waiting again...')
        while not self.client1.wait_for_service(timeout_sec=1.0):
            self.get_logger()().info('current_feature_loc not available, waiting again...')   
        self.req1 = FeaturesLoc.Request()
        self.req2 = FeaturesLoc.Request()
        self.ref_feature_loc = []
        self.current_feature_loc =[]
        self.client_futures = {}


    # def timer_callback(self):
    #     # Run the async function to send requests and gather responses
    #     asyncio.ensure_future(self.send_request())

    def timer_callback(self):
        future1 = self.client1.call_async(self.req1)        
        self.client_futures[""].append(future1)
        future2 = self.client2.call_async(self.req2)   
        self.client_futures.append(future2) 
        
        # future1.add_done_callback(self.client1_response_callback)
        # future2.add_done_callback(self.client2_response_callback)

        
        
        #time.sleep(3)
        #response1, response2 = await asyncio.gather(future1, future2)
        # Log the responses
        # self.get_logger().info(f'Service1 Response: {future1.response1}')
        # self.get_logger().info(f'Service2 Response: {response2}')
        #time.sleep(1)
        camera_vel = self.controller()

    def client1_response_callback(self, response):
        self.ref_feature_loc = response.result()
        #self.get_logger().info(f"error vector is: {self.ref_feature_loc}")
        
    def client2_response_callback(self,response):
        self.current_feature_loc = response.result()
        #self.get_logger().info(f"error vector is: {self.current_feature_loc}")

    # def spin(self):
    #     while rclpy.ok():
    #         rclpy.spin_once(self)
    #         incomplete_futures = []
    #         for f in self.client_futures:
    #             if f.done():                    
    #                 # res = f.result()
    #                 # if isinstance(res, GetPosition.Response):
    #                 #     self.cur_angle_ticks = res.position
    #                 #     self.get_logger().info(f"Joint Positions: \t  {self.cur_angle_ticks}")
    #                 # elif isinstance(res, GetRefAngle.Response):
    #                 #     self.ref_angle_ticks = res.angle
    #                 #     self.get_logger().info(f"Ref Angle Ticks: \t  {self.ref_angle_ticks}")
    #                 # elif isinstance(res, GetCurrent.Response):
    #                 #     self.robot_motor_current = res.current
    #                 #     self.get_logger().info(f"current: \t  {self.robot_motor_current}")
    #             else:
    #                 incomplete_futures.append(f)
    #         self.client_futures = incomplete_futures


    def controller(self):
        error_vector = np.zeros((len(self.ref_feature_loc),1)) 
        for i in range(len(self.ref_feature_loc)):
            error_vector[i] = np.norm(self.ref_feature_loc[i], self.current_feature_loc[i])
        self.get_logger().info(f"error vector is: {error_vector}")


    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        return self.cli.call_async(self.req)

    

    

def main():
    rclpy.init()

    minimal_control = MinimalControl()    
    rclpy.spin(minimal_control)
    
    rclpy.shutdown()


if __name__ == '__main__':
    main()