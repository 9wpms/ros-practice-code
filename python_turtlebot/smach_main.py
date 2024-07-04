import rospy
import select
import subprocess
import sys
import time
from enum import Enum, auto
from tkinter import Tk

class States(Enum):
    START = auto()          # process preparing
    IDLE = auto()           # process is waiting for command
    RUNNING = auto()        # process is running
    COMPLETED = auto()      # process has finished
    ERROR = auto()          # process has an error
    ABORTED = auto()        # process has interrupted

class StateMachine:
    def __init__(self):
        rospy.init_node('state_machine', anonymous=False)
        self.next_time_increment = time.time()
        self.state = States.START
        self.active_flag = True

    def new_window(self):
        new_window = Tk.Toplevel()
        new_window.title("Turtlebot3 Main Menu")
        label = Tk.Label(new_window, text="Please select any choice:")
        label.pack()
        
    def state_shifting(self):
        if self.state == States.START:
            self.state = self.handle_start()
        elif self.state == States.IDLE:
            self.state = self.handle_idle()
        elif self.state == States.RUNNING:
            self.state = self.handle_running()
        elif self.state == States.COMPLETED:
            self.state = self.handle_complete()
        elif self.state == States.ERROR:
            self.state = self.handle_error()
        elif self.state == States.ABORTED:
            self.state = self.handle_aborted()
    
    def system_check_shifting(self):
        pass
    
    def handle_start(self):
        rospy.loginfo("State is now operational at: [%s]", self.state)
        rospy.sleep(1)
        
        # Create the main window
        root = Tk.Tk()
        root.title("Main Window")

        # Button to create new window
        button = Tk.Button(root, text="Create New Window", command=self.new_window)
        button.pack()

        # Run the main event loop
        root.mainloop()

        return States.IDLE
    
    def handle_idle(self):
        rospy.loginfo("State is now operational at: [%s]", self.state)
        rospy.sleep(1)
        
        if self.active_flag:
            return States.RUNNING
        else:
            return States.IDLE

    def handle_running(self):
        rospy.loginfo("State is now operational at: [%s]", self.state)
        rospy.sleep(1)
        
        if self.active_flag:
            rospy.logwarn("[%s]: State has completed process.", self.state)
            return States.COMPLETED
        else:
            return States.RUNNING

    def handle_complete(self):
        rospy.loginfo("State is now operational at: [%s]", self.state)
        rospy.sleep(1)
        
        if self.active_flag:
            return States.IDLE
        else:
            return States.RUNNING
    
    def handle_error(self):
        rospy.logerr("[%s]: Process encountered an error.", self.state)
        rospy.sleep(1)
        return States.ERROR
    
    def handle_aborted(self):
        rospy.logerr("[%s]: Process aborted all process will terminate.", self.state)
        rospy.sleep(1)
        
        # def close_program(self):
        
        return States.ABORTED
    
    def main(self):
        while not rospy.is_shutdown():
            self.now = time.time()
            self.time_until_next = self.next_time_increment - self.now
            if (self.time_until_next < 0):
                self.time_until_next = 0
            self.inReady, self.outReady, self.exReady = select.select([sys.stdin], [], [], self.time_until_next)
            if (sys.stdin in self.inReady):  # check if there is something ready for us on stdin
                try:
                    self.user_input = input()
                    rospy.logwarn("You have entered: [%s]" % self.user_input)
                except UnicodeDecodeError as e:
                    rospy.logerr("Unable to decode input. Please make sure your input is correctly formatted.")
                if self.user_input.lower() == 'y':
                    while True:
                        self.state_shifting()
                        if self.state == States.COMPLETED:  # Check if the state transitions to COMPLETED
                            rospy.logwarn("Process has completed, return to ready or not.")
                            break
                elif self.user_input.lower() == 'n':
                    rospy.logwarn("Stop command received. Setting active flag to False.")
                    self.active_flag = False
                    self.state = States.ABORTED
                    self.state_shifting()
                    sys.exit(1)
            self.now = time.time()
            if (self.now >= self.next_time_increment):
                rospy.loginfo("Are you ready to launch [y/n]: ")
            
            rospy.sleep(1)
if __name__ == "__main__":
    test = StateMachine()
    test.main()

# import tkinter as tk

# def create_new_window():
#     new_window = tk.Toplevel()
#     new_window.title("New Window")
#     label = tk.Label(new_window, text="This is a new window")
#     label.pack()

# # Create the main window
# root = tk.Tk()
# root.title("Main Window")

# # Button to create new window
# button = tk.Button(root, text="Create New Window", command=create_new_window)
# button.pack()

# # Run the main event loop
# root.mainloop()
