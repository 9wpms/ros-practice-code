#include <ros/ros.h>
#include <std_msgs/String.h>

void inputCallback(const std_msgs::String::ConstPtr& msg) {
  ROS_INFO("Received input message: %s", msg->data.c_str());
}

int main(int argc, char** argv) {
  ros::init(argc, argv, "subTeensy");
  ros::NodeHandle nh;

  ros::Subscriber sub = nh.subscribe("teensy_sending", 10, inputCallback);

  ros::spin();

  return 0;
}

