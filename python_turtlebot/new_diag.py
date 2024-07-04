# import rospy
# from sensor_msgs.msg import LaserScan, Imu, Image
# from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus

# class SensorDiagnostics:
#     def __init__(self):
#         rospy.init_node("sensor_diagnostics", anonymous=True)
        
#         # Dictionary to store topic timestamps
#         self.stamps = {"/imu": 0, "/scan": 0, "/camera/rgb/image_raw": 0}
        
#         # Initialize subscribers for sensor topics
#         rospy.Subscriber("/imu", Imu, self.callback_imu)
#         rospy.Subscriber("/scan", LaserScan, self.callback_scan)
#         rospy.Subscriber("/camera/rgb/image_raw", Image, self.callback_image)
        
#         # Publisher for diagnostic messages
#         self.diagnostic_pub = rospy.Publisher("/diagnostic", DiagnosticArray, queue_size=10)
        
#         self.rate = rospy.Rate(1)

#     def callback_imu(self, data):
#         self.update_stamp("/imu", data.header.stamp.to_sec())

#     def callback_scan(self, data):
#         self.update_stamp("/scan", data.header.stamp.to_sec())

#     def callback_image(self, data):
#         self.update_stamp("/camera/rgb/image_raw", data.header.stamp.to_sec())

#     def update_stamp(self, topic, timestamp):
#         self.stamps[topic] = timestamp

#     def run_diagnostics(self):
#         rospy.loginfo('At diagnostics node open: [Success]')
#         while not rospy.is_shutdown():
#             current_time = rospy.Time.now().to_sec()
                        
#             diagnostic_array = DiagnosticArray()
#             diagnostic_array.header.stamp = rospy.Time.now()
#             diagnostic_array.status = []  # Initialize as a list
            
#             for topic, stamp in self.stamps.items():
#                 status = DiagnosticStatus()
#                 status.name = topic
#                 status.hardware_id = topic.split("/")[-1]
                
#                 if current_time - stamp > 1:
#                     status.level = DiagnosticStatus.WARN
#                     status.message = f"No data received on {topic} in the last second"
#                 else:
#                     status.level = DiagnosticStatus.OK
#                     status.message = f"Data received on {topic}"
                
#                 diagnostic_array.status.append(status)  # Append DiagnosticStatus to the list
            
#             self.diagnostic_pub.publish(diagnostic_array)
#             self.rate.sleep()  # Sleep to maintain the loop rate

# if __name__ == '__main__':
#     sensor_diagnostics = SensorDiagnostics()
#     sensor_diagnostics.run_diagnostics()

import rospy
from sensor_msgs.msg import LaserScan, Imu, Image
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
import threading

class SensorDiagnostics:
    def __init__(self):
        rospy.init_node('turtlebot_diagnostics', anonymous=False)
        
        # Dictionary to store topic timestamps
        self.stamps = {"/imu": 0, "/scan": 0, "/camera/rgb/image_raw": 0}
        
        # Initialize subscribers for sensor topics
        rospy.Subscriber("/imu", Imu, self.callback_imu)
        rospy.Subscriber("/scan", LaserScan, self.callback_scan)
        rospy.Subscriber("/camera/rgb/image_raw", Image, self.callback_image)
        
        # Publisher for diagnostic messages
        self.diagnostic_pub = rospy.Publisher("/my_diagnostics", DiagnosticArray, queue_size=10)
        
        self.rate = rospy.Rate(1)

        # Start a separate thread for sensor data collection
        self.sensor_thread = threading.Thread(target=self.run_sensor_collection)
        self.sensor_thread.start()

    def callback_imu(self, data):
        self.update_stamp("/imu", data.header.stamp.to_sec())

    def callback_scan(self, data):
        self.update_stamp("/scan", data.header.stamp.to_sec())

    def callback_image(self, data):
        self.update_stamp("/camera/rgb/image_raw", data.header.stamp.to_sec())

    def update_stamp(self, topic, timestamp):
        self.stamps[topic] = timestamp

    def run_sensor_collection(self):
        while not rospy.is_shutdown():
            self.callback_time = rospy.Time.now().to_sec()
            for topic, stamp in self.stamps.items():
                # Access the latest timestamp for each topic
                self.latest_timestamp = self.stamps[topic]
                # Now you can collect sensor data using the latest timestamp
                # Example: If topic == '/imu', you can access IMU data from its callback function
                # Example: If topic == '/scan', you can access LaserScan data from its callback function
                # Example: If topic == '/camera/rgb/image_raw', you can access Image data from its callback function
            self.rate.sleep()  # Sleep to maintain the loop rate

    def run_diagnostics(self):
        rospy.loginfo('--- Diagnostics node open: [Success] ---')
        while not rospy.is_shutdown():

            current_time = rospy.Time.now().to_sec()
                        
            diagnostic_array = DiagnosticArray()
            diagnostic_array.header.stamp = rospy.Time.now()
            diagnostic_array.status = []  # Initialize as a list
                        
            for topic, stamp in self.stamps.items():
                status = DiagnosticStatus()
                status.name = topic
                status.hardware_id = topic.split("/")[-1]
                
                if current_time - stamp > 1:
                    status.level = DiagnosticStatus.WARN
                    status.message = f"No data received on {topic} in the last second"
                else:
                    status.level = DiagnosticStatus.OK
                    status.message = f"Data received on {topic}"
                
                diagnostic_array.status.append(status)  # Append DiagnosticStatus to the list
                
            self.diagnostic_pub.publish(diagnostic_array)
            
            if self.callback_time < current_time:
                rospy.loginfo('Debugging: [Sending] new data from callback')
            else:
                rospy.loginfo('Debugging: [Losting] new data from callback')
            print(self.callback_time, current_time)
            self.rate.sleep()  # Sleep to maintain the loop rate

if __name__ == '__main__':
    sensor_diagnostics = SensorDiagnostics()
    sensor_diagnostics.run_diagnostics()
