# Importing required libraries
import subprocess
import rospy
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
from tkinter import *

# Global variables
window = Tk()
wait_to_sub = getCallback = False
run_diagnostic = launch_gazebo = launch_node_1 = launch_node_2 = None
status_gui = 0
count = 0

# Function to launch Gazebo
def launch_gazebo_process():
    global launch_gazebo
    launch_gazebo = subprocess.Popen(['gnome-terminal', '--', 'roslaunch', 'turtlebot3_gazebo', 'turtlebot3_world.launch'])
    
    if launch_gazebo.wait() == 0:
        return True

# Callback function for diagnostics
def callback(status_array):
    global getCallback
    for status in status_array.status:
        if status.level == DiagnosticStatus.ERROR:
            debug_callback = f"Error in component '{status.name}': '{status.level}': {status.message}"
            rospy.logerr(debug_callback)
    getCallback = True
    return getCallback

# Main menu function
def first_main_menu():
    global status_gui
    status_gui = 1
    
    window.title('Turtlebot3 Main Menu')
    
    title = Label(master=window, text='Please select any choice:')
    title.pack()
    
    create_map_bt = Button(master=window, text='Create Map', command=create_map_def)
    create_map_bt.pack()
    
    navigate_bt = Button(master=window, text='Navigate Map', command=navigate_map_def)
    navigate_bt.pack()
    
    exit_bt = Button(master=window, text='Exit', command=exit_def)
    exit_bt.pack()
    
    window.mainloop()

# Function to create a map
def create_map_def():
    rospy.loginfo("Selected mode: Create Map")
    
    if launch_gazebo_process() == True:
        
        global launch_node_1, launch_node_2
        
        launch_node_1 = subprocess.Popen(['gnome-terminal', '--', 'roslaunch', 'turtlebot3_slam', 'turtlebot3_slam.launch'])
        
        if launch_node_1.wait() == 0:
            
            launch_node_2 = subprocess.Popen(['gnome-terminal', '--', 'roslaunch', 'turtlebot3_teleop', 'turtlebot3_teleop_key.launch'])
    else:
        rospy.logerr('--- Gazebo is not ready ---')
        
    if launch_node_2.wait() == 0:
        second_menu()
             
# Function for navigation map
def navigate_map_def():
    global input_address
    rospy.loginfo("Selected mode: Navigation")
    
    window.title('Navigate Menu')
    
    title = Label(master=window, text='Please enter map name:')
    title.pack()
    
    input_address = Entry(master=window)
    input_address.pack()
    
    submit_bt = Button(master=window, text='Submit', command=map_name)
    submit_bt.pack()
    
    window.mainloop()

# Function to get map name
def map_name():
    global input_address
    map_name_input = input_address.get()
    subprocess.Popen(["gnome-terminal", "--", "roslaunch", "turtlebot3_navigation", "turtlebot3_navigation.launch", "map_file:=$HOME/{}.yaml".format(map_name_input)])
   
# Secondary menu function
def second_menu():
    window.title('Alternative menu')
    
    title = Label(master=window, text='Select to Save map or Exit:')
    title.pack()
    
    create_map_bt = Button(master=window, text='Save', command=save_def)
    create_map_bt.pack()
    
    navigate_bt = Button(master=window, text='Exit', command=exit_def)
    navigate_bt.pack()
    
    window.mainloop()

# Function to save the map
def save_def():
    global count
    if count == 0:
        subprocess.Popen(["gnome-terminal", "--", "rosrun", "map_server", "map_saver", "-f", "~/map"])
        count += 1
    else:
        subprocess.Popen(["gnome-terminal", "--", "rosrun", "map_server", "map_saver", "-f", "~/map({})".format(count)])
    rospy.loginfo("--- Map has been saved ---")

def exit_def():
    global launch_node_1, launch_node_2, launch_gazebo, run_diagnostic, status_gui
    status_gui = 0

    # Terminate subprocesses if they are running
    if launch_node_1 is not None:
        pass
    
    if launch_node_2 is not None:
        pass

    if launch_gazebo is not None:
        subprocess.Popen(['killall', 'gzserver'])
        subprocess.Popen(['killall', 'gzclient'])
        
    if run_diagnostic is not None:
        pass
    
    window.destroy()  # Destroy the Tkinter window before exiting
    exit_command = "exit"
    subprocess.run(exit_command, shell=True)

# Main function for the main user task
def main_task():
    global wait_to_sub  # Add this line to access the global variable

    # Initialize wait_to_sub
    wait_to_sub = False

    rospy.init_node('turtlecot3_test', anonymous=True)
    rospy.Subscriber('/diagnostic', DiagnosticArray, callback)
    
    if launch_gazebo_process() is False:
        rospy.loginfo('--- Try to run Gazebo ---')
        launch_gazebo_process()

    try:
        while True:
            if wait_to_sub is False and getCallback is False:
                if launch_gazebo.wait() == 0:
                    run_diagnostic = subprocess.Popen(['gnome-terminal', '--', 'rosrun', 'my_package', 'new_diag.py'])
                    wait_to_sub = True
                else:
                    rospy.loginfo('--- Waiting for open Gazebo ---')
            elif launch_gazebo.wait() == 0 and wait_to_sub is True:
                rospy.loginfo('--- Gazebo and Diagnostic are ready: [Start] Main menu ---')
                first_main_menu()
                break
            else:
                rospy.logerr('--- Gazebo and Diagnostic not ready: [Stop] Main menu ---')

        rate = rospy.Rate(1)
        while not rospy.is_shutdown():     
            if status_gui == 0:
                first_main_menu()
            else:
                pass
            rate.sleep()
    except KeyboardInterrupt:
        pass

# Start the main task
main_task()
