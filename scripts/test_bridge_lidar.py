# import rospy
# from std_msgs.msg import Bool, String, Float32
# from sensor_msgs.msg import LaserScan

# from dynamic_reconfigure.server import Server
# from my_ros_package.cfg import testParamConfig

# class LidarSystem:
#     def __init__(self):
#         rospy.init_node("Bridge_lidar", anonymous=True)

#         self.status_pub = rospy.Publisher("status_lidar", Bool, queue_size=10)
#         self.frq_pub = rospy.Publisher("frq_lidar", Float32, queue_size=10)  # Use Float32 for frequency
#         self.laser_scan_data = LaserScan()
#         self.keep_data = LaserScan()
#         self.error_count = 0
#         self.last_stamp = 0.0  # Initialize with float time

#         self.lidar_system = False
#         #self.mode = 0  # [0 auto, 1 true only, 2 false only]
#         self.srv = Server(testParamConfig, self.serverCallback)

#     def serverCallback(self, config, level):
#         self.mode = config.mode
#         rospy.loginfo("Lidar has changed configure: [{}]".format(self.mode))
#         return config

#     def lidar_callback(self, data):
#         self.laser_scan_data = data
#         self.last_stamp = rospy.Time.now().to_sec()

#         if not self.laser_scan_data.ranges:
#             self.lidar_system = False
#             self.error_count = 0
#             return

#         if self.mode == 0:
#             # Check for valid data in both scans
#             if self.keep_data.ranges and self.laser_scan_data.ranges:
#                 if self.keep_data.ranges[0] < self.laser_scan_data.ranges[0]:
#                     self.lidar_system = True
#                     self.error_count = 0
#                 else:
#                     self.error_count += 1
#                     if self.error_count >= 10:
#                         self.lidar_system = False
#                         self.error_count = 0
#         elif self.mode == 1:
#             self.lidar_system = True
#         elif self.mode == 2:
#             self.lidar_system = False

#         self.keep_data = self.laser_scan_data

#     def run(self):
#         rospy.Subscriber("scan", LaserScan, self.lidar_callback)
#         rate = rospy.Rate(10)  # 10 Hz

#         while not rospy.is_shutdown():
#             now_stamp = rospy.Time.now().to_sec()
#             time_diff = now_stamp - self.last_stamp

#             if self.mode == 0:
#                 if time_diff >= 5:  # Time out
#                     self.lidar_system = False
#             elif self.mode == 1:
#                 self.lidar_system = True
#             elif self.mode == 2:
#                 self.lidar_system = False
                
#             # Publish frequency as a float (assuming Hz)
#             if self.lidar_system:
#                 self.frq_pub.publish(10.0)  # Replace with actual frequency
#             else:
#                 self.frq_pub.publish(0.0)

#             self.status_pub.publish(self.lidar_system)

#             rospy.loginfo("Lidar system is working: [{}] Mode: [{}]".format(self.lidar_system, self.mode))
#             rate.sleep()


# if __name__ == '__main__':
#     lidar_system = LidarSystem()
#     lidar_system.run()
