# #!/usr/bin/env python3

# import rospy
# from std_msgs.msg import Int64
# from std_srvs.srv import SetBool
# from dynamic_reconfigure.server import Server
# from my_ros_package.cfg import TestConfig
# class NumberCounter:

#     def __init__(self):
#         self.counter = 0
#         self.pub = rospy.Publisher("/number_count", Int64, queue_size=10)
#         self.number_subscriber = rospy.Subscriber("/number", Int64, self.callback_number)
#         self.reset_service = rospy.Service("/reset_counter", SetBool, self.callback_reset_counter)

#         self.dynamics_server = Server(TestConfig, self.server_cb)
        
#         # self.number_int = rospy.get_param("~number_int")
#         self.int_param = rospy.get_param("~int_param")
#         self.enabled = True
        
#         rate = rospy.Rate(5)
#         while not rospy.is_shutdown():
#             rospy.loginfo("main controller --> "+ str(self.enabled) + str(self.int_param))
#             rate.sleep()
        
#     def server_cb(self, config, level):
#         # rospy.loginfo("""Reconfigure Request: {int_param}, {double_param},\ 
#         #   {str_param}, {bool_param}, {size}""".format(**config))
        
#         rospy.loginfo("from configure file --> " + str(config.enabled))
        
#         self.enabled = config.enabled
#         return config
    
#     def callback_number(self, msg):
#         self.counter += msg.data
#         new_msg = Int64()
#         new_msg.data = self.counter
#         self.pub.publish(new_msg)

#     def callback_reset_counter(self, req):
#         if req.data:
#             self.counter = 0
#             return True, "Counter has been successfully reset"
#         return False, "Counter has not been reset"

# if __name__ == '__main__':
#     rospy.init_node('number_counter')
#     NumberCounter()
#     rospy.spin()