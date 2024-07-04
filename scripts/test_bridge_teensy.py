# #!/usr/bin/env python3
# import rospy
# from std_msgs.msg import String

# begin_stamp, count, error, keep = 0, 0, 0, 0.0

# status_teensy = rospy.Publisher("status_teensy", String, queue_size=10)
# frq_teensy = rospy.Publisher("frq_teensy", String, queue_size=10)

# class Colors:
#     RED = '\033[91m'
#     GREEN = '\033[92m'
#     YELLOW = '\033[93m'
#     BLUE = '\033[94m'
#     MAGENTA = '\033[95m'
#     CYAN = '\033[96m'
#     END = '\033[0m'
    
# def callback_teensy(data):
#     global begin_stamp, count, error, keep
#     new_stamp = rospy.Time.now().to_sec()
#     diff = round(new_stamp - begin_stamp, 1)

#     if count == 0 and diff == round(keep, 1):
#         print("Teensy working normal")
#         keep += 0.1
#         count += 1
#     else:
#         error += 1
#         if error >= 10:
#             print("Teensy has many errors")
#         keep = diff + 0.1    
#         count = 0
        
# def main():
#     global begin_stamp, count, error, keep
    
#     rospy.init_node("Bridge_teensy", anonymous=True)
#     rospy.Subscriber("teensy" , String, callback_teensy)
    
#     begin_stamp = rospy.Time.now().to_sec()
#     rate = rospy.Rate(10)
    
#     while not rospy.is_shutdown():
#         if count > 0:
#             frq_teensy.publish("10")
#             count = 0
#             error = 0
#         else:
#             frq_teensy.publish("---")
        
#         rate.sleep()

# if __name__ == '__main__':
#     main()