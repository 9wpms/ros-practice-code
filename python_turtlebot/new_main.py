# import subprocess
# import rospy
# from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
# from tkinter import *
# import os

# class A:
#     def __init__(self):
#         rospy.init_node('turtlebot3_test', anonymous=True)
        
#         self.runto_callback = self.status_gazebo = False
#         self.gazebo_process = self.diag_process = self.slam_process = self.teleop_process = self.nav_process = None
#         self.status_gui = self.count_mode_map = self.map_count = self.open_one_time = 0
#         self.diag_launched = False

#         # Create the main Tkinter root window
#         self.root = Tk()
#         self.root.title("Turtlebot3 Main Menu")
#         self.root.geometry("450x300")

#         # Create label for the main menu
#         self.label1 = Label(self.root, text="Please select any choice:")
#         self.label1.pack()

#         # Create buttons for different functionalities
#         button1 = Button(self.root, text="Create Map", command=self.mode_map)
#         button1.pack()

#         button2 = Button(self.root, text="Navigate Map", command=self.mode_navi)
#         button2.pack()

#         button3 = Button(self.root, text="Exit", command=self.mode_exit)
#         button3.pack()

#         # Start the Tkinter event loop
#         self.root.mainloop()
    
#     def mode_map(self):
        
#         rospy.on_shutdown(self.run)
#         # Logic for map creation mode
#         if self.status_gazebo and self.count_mode_map == 0:
#             self.slam_process = subprocess.Popen(['gnome-terminal', '--', 'roslaunch', 'turtlebot3_slam', 'turtlebot3_slam.launch'])
#             self.count_mode_map = 1
#             if self.status_gazebo and self.count_mode_map == 1:
#                 self.teleop_process = subprocess.Popen(['gnome-terminal', '--', 'roslaunch', 'turtlebot3_teleop', 'turtlebot3_teleop_key.launch'])
#                 self.count_mode_map = 2
#             else:
#                 rospy.logerr(self.status_gazebo, self.count_mode_map)
#         else:
#             rospy.logerr(self.status_gazebo, self.count_mode_map)
            
#         if self.slam_process.wait() == 0 and self.teleop_process.wait() == 0:
#             self.second_menu()
#         else:
#             rospy.logerr('[Error]: Failed to pop-up second menu.')
            
#     def mode_navi(self):
#         # Logic for map navigation mode
#         self.root.withdraw()
#         self.windows_3 = Toplevel(self.root)
#         self.windows_3.title('Navigation Menu')
#         self.windows_3.geometry("450x300")

#         title = Label(master=self.windows_3, text='Please enter map name:')
#         title.pack()

#         self.input_address = Entry(master=self.windows_3)
#         self.input_address.pack()

#         submit_bt = Button(master=self.windows_3, text='Submit', command=self.input_map_name)
#         submit_bt.pack()

#         back_bt = Button(master=self.windows_3, text='Back', command=self.windows_3.destroy)
#         back_bt.pack()

#     def input_map_name(self):
#         map_name_input = self.input_address.get()
#         self.windows_3.destroy()
        
#         # Validate map name and launch navigation
#         map_file_path = f"$HOME/{map_name_input}.yaml"
#         if os.path.isfile(map_file_path):
#             rospy.logwarn(f'[Success]: Trying to open map: {map_name_input}')
#             self.nav_process = subprocess.Popen(["gnome-terminal", "--", "roslaunch", "turtlebot3_navigation", "turtlebot3_navigation.launch", f"map_file:={map_file_path}"])
#         else:
#             rospy.logerr(f'[Error]: Map file does not exist: {map_file_path}')

#     def mode_exit(self):
#         # Logic to exit the application
#         self.root.destroy()
        
#         try:
#             subprocess.Popen(['killall', 'gnome-terminal-server'])
#         except Exception as e:
#             rospy.logerr(f"[Error]: Terminating Gnome-terminal processes: {e}")

#         try:
#             if self.gazebo_process:
#                 subprocess.Popen(['killall', 'gzserver'])
#                 subprocess.Popen(['killall', 'gzclient'])
#                 self.status_gazebo = False
#         except Exception as e:
#             rospy.logerr(f"[Error]: Terminating Gazebo processes: {e}")
        
#         self.diag_process = self.slam_process = self.teleop_process = self.nav_process = None

#     def second_menu(self):
#         self.root.withdraw()
#         self.windows_2 = Toplevel(self.root)
#         self.windows_2.title('Alternative menu')
#         self.windows_2.geometry("450x300")

#         title = Label(master=self.windows_2, text='Please select any choice:')
#         title.pack()

#         save_bt = Button(master=self.windows_2, text='Save Map', command=self.save_map)
#         save_bt.pack()

#         back_bt = Button(master=self.windows_2, text='Back', command=self.windows_2.destroy)
#         back_bt.pack()

#     def save_map(self):
#         # self.windows_2.destroy()
        
#         if self.slam_process is None:
#             rospy.logerr('[Error]: Failed to save the map.')
#         else:
#             if self.map_count == 0:
#                 subprocess.Popen(["gnome-terminal", "--", "rosrun", "map_server", "map_saver", "-f", "~/map"])
#                 self.map_count += 1
#             else:
#                 subprocess.Popen(["gnome-terminal", "--", "rosrun", "map_server", "map_saver", "-f", "~/map({})".format(self.map_count)])
#             rospy.loginfo("--- Map has been saved ---")

#     def run(self):
#         # Set up subscriber to diagnostic topic
#         rospy.Subscriber('/diagnostic', DiagnosticArray, self.callback)
#         rate = rospy.Rate(1)
        
#         if self.open_one_time == 0:
#             if not self.status_gazebo:
#                 self.open_one_time = 1
#                 self.launch_gazebo()
#                 self.first_menu()
#             else:
#                 rospy.loginfo('--- Gazebo has already been opened ---')
        
#         while not rospy.is_shutdown():
#             rospy.loginfo(f'[Status] Callback is working: {self.runto_callback}')
#             if not self.runto_callback:
#                 if not self.diag_launched:
#                     self.diag_process = subprocess.Popen(['gnome-terminal', '--', 'rosrun', 'my_package', 'new_diag.py'])
#                     self.diag_launched = True
#                 else:
#                     rospy.loginfo('--- Diagnostic has already been launched ---')
#             else:
#                 if self.status_gui == 0:
#                     self.root.update()
#                     self.status_gui = 1
                
#                 # Check for termination of processes
#                 if self.diag_process and self.diag_process.poll() is not None:
#                     rospy.loginfo('--- Diagnostic process terminated ---')
#                     self.diag_process = None
#                 if self.slam_process and self.slam_process.poll() is not None:
#                     rospy.loginfo('--- SLAM process terminated ---')
#                     self.slam_process = None
#                 if self.teleop_process and self.teleop_process.poll() is not None:
#                     rospy.loginfo('--- Teleop process terminated ---')
#                     self.teleop_process = None
#                 if self.nav_process and self.nav_process.poll() is not None:
#                     rospy.loginfo('--- Navigation process terminated ---')
#                     self.nav_process = None
            
#             rate.sleep()


# # Example usage
# my_instance = A()
# my_instance.run()

import subprocess
import rospy
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
from tkinter import *
import os

class A:
    def __init__(self):
        rospy.init_node('turtlebot3_test', anonymous=True)
        self.windows_1 = self.windows_2 = self.windows_3 = Tk()
        self.runto_callback = self.status_gazebo = False
        self.gazebo_process = self.diag_process = self.slam_process = self.teleop_process = self.nav_process = None
        self.status_gui = self.count_mode_map = self.map_count = self.open_one_time = 0
        self.diag_launched = False

    def launch_gazebo(self):
        self.gazebo_process = subprocess.Popen(['gnome-terminal', '--', 'roslaunch', 'turtlebot3_gazebo', 'turtlebot3_world.launch'])
        if self.gazebo_process.wait() == 0:
            rospy.logwarn('[Finish]: Gazebo opened successfully.')
            self.status_gazebo = True
        else:
            rospy.logerr('[Failed]: Failed to launch Gazebo.')
            self.status_gazebo = False

    def callback(self, status_array):
        for status in status_array.status:
            if status.level == DiagnosticStatus.ERROR:
                rospy.logerr(f"Error in component '{status.name}': '{status.level}': {status.message}")
            else:
                rospy.logwarn(f"Check in component '{status.name}': '{status.level}': {status.message}")
                self.runto_callback = True

    def first_menu(self):
        self.status_gui = 1
        self.windows_1.title('Turtlebot3 Main Menu')
        self.windows_1.minsize(width=400, height=200)
        
        title = Label(master=self.windows_1, text='Please select any choice:')
        title.pack()
        
        create_bt = Button(master=self.windows_1, text='Create Map', command=self.mode_map)
        create_bt.pack()
        
        navigate_bt = Button(master=self.windows_1, text='Navigate Map', command=self.mode_navi)
        navigate_bt.pack()
        
        exit_bt = Button(master=self.windows_1, text='Exit', command=self.mode_exit)
        exit_bt.pack()
        
        self.windows_1.mainloop()

    def mode_map(self):
        # Logic for map creation mode
        if self.status_gazebo and self.count_mode_map == 0:
            self.slam_process = subprocess.Popen(['gnome-terminal', '--', 'roslaunch', 'turtlebot3_slam', 'turtlebot3_slam.launch'])
            self.count_mode_map = 1
            if self.status_gazebo and self.count_mode_map == 1:
                self.teleop_process = subprocess.Popen(['gnome-terminal', '--', 'roslaunch', 'turtlebot3_teleop', 'turtlebot3_teleop_key.launch'])
                self.count_mode_map = 2
            else:
                rospy.logerr(self.status_gazebo, self.count_mode_map)
        else:
            rospy.logerr(self.status_gazebo, self.count_mode_map)
            
        if self.slam_process.wait() == 0 and self.teleop_process.wait() == 0:
            self.second_menu()
        else:
            rospy.logerr('[Error]: Failed to pop-up second menu.')
            
    def mode_navi(self):
        # Logic for map navigation mode
        self.windows_3.title('Navigation Menu')
        self.windows_3.minsize(width=400, height=200)
        
        title = Label(master=self.windows_3, text='Please enter map name:')
        title.pack()
        
        self.input_address = Entry(master=self.windows_3)
        self.input_address.pack()
        
        submit_bt = Button(master=self.windows_3, text='Submit', command=self.input_map_name)
        submit_bt.pack()
        
        back_bt = Button(master=self.windows_3, text='Back', command=self.windows_3.destroy)
        back_bt.pack()

        self.windows_3.mainloop()
    
    def input_map_name(self):
        map_name_input = self.input_address.get()
        self.windows_3.destroy()
        
        # Validate map name and launch navigation
        map_file_path = f"$HOME/{map_name_input}.yaml"
        if os.path.isfile(map_file_path):
            rospy.logwarn(f'[Success]: Trying to open map: {map_name_input}')
            self.nav_process = subprocess.Popen(["gnome-terminal", "--", "roslaunch", "turtlebot3_navigation", "turtlebot3_navigation.launch", f"map_file:={map_file_path}"])
        else:
            rospy.logerr(f'[Error]: Map file does not exist: {map_file_path}')

    def mode_exit(self):
        # Logic to exit the application
        self.open_one_time = 0
        self.windows_1.destroy()
        
        processes = [self.diag_process, self.slam_process, self.teleop_process, self.nav_process]
        for process in processes:
            if process is not None:
                process.terminate()

        try:
            if self.gazebo_process:
                subprocess.Popen(['killall', 'gzserver'])
                subprocess.Popen(['killall', 'gzclient'])
                self.status_gazebo = False
        except Exception as e:
            rospy.logerr(f"[Error]: Terminating Gazebo processes: {e}")
        
        self.diag_process = self.slam_process = self.teleop_process = self.nav_process = None

    def second_menu(self):
        self.windows_2.title('Alternative menu')
        self.windows_2.minsize(width=400, height=200)
        
        title = Label(master=self.windows_2, text='Please select any choice:')
        title.pack()
        
        save_bt = Button(master=self.windows_2, text='Save Map', command=self.save_map)
        save_bt.pack()
        
        back_bt = Button(master=self.windows_2, text='Back', command=self.windows_2.destroy)
        back_bt.pack()

        self.windows_2.mainloop()
        
    def save_map(self):
        self.windows_2.destroy()
        
        if self.slam_process is None:
            rospy.logerr('[Error]: Failed to save the map.')
        else:
            if self.map_count == 0:
                subprocess.Popen(["gnome-terminal", "--", "rosrun", "map_server", "map_saver", "-f", "~/map"])
                self.map_count += 1
            else:
                subprocess.Popen(["gnome-terminal", "--", "rosrun", "map_server", "map_saver", "-f", "~/map({})".format(self.map_count)])
            rospy.loginfo("--- Map has been saved ---")
    
    def run(self):
        # Set up subscriber to diagnostic topic
        rospy.Subscriber('/diagnostic', DiagnosticArray, self.callback)
        rate = rospy.Rate(1)
        
        if self.open_one_time == 0:
            if not self.status_gazebo:
                self.open_one_time = 1
                self.launch_gazebo()
            else:
                rospy.loginfo('--- Gazebo has already been opened ---')
        
        count = 0
        
        while not rospy.is_shutdown():
            rospy.loginfo(f'[Status] Callback is working: {self.runto_callback}')
            if not self.runto_callback:
                if not self.diag_launched:
                    self.diag_process = subprocess.Popen(['gnome-terminal', '--', 'rosrun', 'my_package', 'new_diag.py'])
                    self.diag_launched = True
                else:
                    rospy.loginfo('--- Diagnostic has already been launched ---')
            else:
                if count == 0:
                    self.first_menu()
                    count = 1
            
            rate.sleep()

# Example usage
my_instance = A()
my_instance.run()