#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <std_msgs/String.h>

std_msgs::String str_msg;
bool lidarWorking = false;

void lidarCallback(const sensor_msgs::LaserScan::ConstPtr& msg) {
  lidarWorking = true;
}

int main(int argc, char** argv) {
  // Initialize ROS node
  ros::init(argc, argv, "lidar_node");
  ros::NodeHandle nh;

  ros::Subscriber lidarSub = nh.subscribe("scan", 1, lidarCallback);
  ros::Publisher lidarStatus = nh.advertise<std_msgs::String>("lidarStat", 1);

  // Set loop rate
  ros::Rate loop_rate(10); // 10 Hz

  // Set string message to empty before entering the loop
  str_msg.data = "";

  while (ros::ok()) {
    ros::spinOnce();

    if (lidarWorking) {
      str_msg.data = "1"; // LiDAR is working
    } else {
      str_msg.data = "0"; // LiDAR is not working
    }

    lidarStatus.publish(str_msg);
    loop_rate.sleep();
  }

  return 0;
}