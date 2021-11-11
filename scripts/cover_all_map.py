#!/usr/bin/env python3
# ################################################################################################################################################
# Author : Stefano Mulargia
# Update :  Nov 7 2021

# ################################################################################################################################################
import rospy
import numpy as np
# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from  move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from  nav_msgs.msg import Odometry

# #################################################################################################################################################

# TABLE CONSTRUCTION 
# At the beginning it has only                                  x y cost
# the I'll attach on the right the Energy it beocmes            x y cost Energy
# finally I need the distance form where I am so                x y cost Energy distance distance_x distance_y

# #################################################################################################################################################

import time
coordinates = np.loadtxt('/home/user/Projects/Mobile_robotics/get_cost_from_world_x_y.txt', delimiter=',', unpack=False)
coordinates = coordinates[coordinates[:, -1] == 0.00]
np.savetxt("/home/user/Projects/Mobile_robotics/coordinates.txt", coordinates, fmt='%.2f',delimiter=',')
[row, column]= coordinates.shape
# print(coordinates.shape)

stack_of_zeros = np.zeros([row,1])
Table = np.column_stack((coordinates,stack_of_zeros))
Table = np.column_stack((Table,stack_of_zeros))
Table = np.column_stack((Table,stack_of_zeros))
Table = np.column_stack((Table,stack_of_zeros))
np.savetxt("/home/user/Projects/Mobile_robotics/Table.txt", Table, fmt='%.2f',delimiter=',')
# ###################################################################################################################################################
myvar = None

# ###################################################################################################################################################

def get_position(msg): 
    global myvar
    position_q = msg.pose.pose.position
    myvar = np.asarray([position_q.x, position_q.y])


def remove_from_table():
    # remove from table the point already full of energy
    Table = np.loadtxt('/home/user/Projects/Mobile_robotics/Table.txt', dtype=float, delimiter =',')
    print('shape',np.shape(Table))
    l = len(Table)
    i=0
    while (i<l):
        if Table[i][3]>0.1:                                                         # delete the row corresponding to a value of energy grater than 10mJ
            Table = np.delete(Table, i, 0)
            l = len(Table)
        i+=1
    Table = Table[np.argsort(Table[:, 4])]                                          #order table for distance
    print(len(Table))
    np.savetxt("/home/user/Projects/Mobile_robotics/Table.txt", Table, fmt='%.2f',delimiter=',')

def update_energy_table():
    global myvar                                                                    # my position at current time
    # add energy to neighbor
    Table = np.loadtxt('/home/user/Projects/Mobile_robotics/Table.txt', dtype=float, delimiter =',')

    rospy.Subscriber('/odom', Odometry, get_position)

    rospy.sleep(0.1)
    for i in range(0, len(Table)):
        a = np.array((Table[i][0],Table[i][1]))                                     # Convert into an array the coordinate of the table
        dst_x = np.linalg.norm(a[0]-myvar[0])                                       # Compute the distance x axis 
        dst_y = np.linalg.norm(a[1]-myvar[1])                                       # Compute the distance y axis
        dst = np.linalg.norm(a-myvar)                                               # Compute the distance 
        Table[i][4] = dst                                                           
        Table[i][5] = dst_x
        Table[i][6] = dst_y
        if (Table[i][5] > 0.5 and Table[i][6] > 0.5 and Table[i][4] <1):            # Note that 0.5 correspond to 0.1 meters in the assignment 
            Table[i][3] += (0.0001/((Table[i][6]/5)**2+(Table[i][5]/5)**2))*10      # approximation of the integral, *10 is to speed up the simulation
            print('Table:',Table[i])
  
    np.savetxt("/home/user/Projects/Mobile_robotics/Table.txt", Table, fmt='%.2f',delimiter=',')


# #########################################################################################################

def reach_goal(destination, client):
    coord = destination
    coord = coord[:2]                                                               # From the Table takes only the first 2 column corresponding to x and y coordinate
   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

   # Set the destination coordinates in the "map" coordinate frame as the goal 
    goal.target_pose.pose.position.x = float(coord[0])
    goal.target_pose.pose.position.y = float(coord[1])
   # goal.target_pose.pose.position.z = 0.0

   # No rotation of the mobile base frame w.r.t. map frame
    goal.target_pose.pose.orientation.w = 1.0
   # Sends the goal to the action server.
    client.send_goal(goal)
    stampa = 0
    while (stampa<3):                                                            # http://docs.ros.org/en/kinetic/api/actionlib_msgs/html/msg/GoalStatus.html
        update_energy_table()
        stampa = client.get_state()
 
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result() 
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")  

    return coord[0], coord[1]   


def movebase_client():

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()
    
   # Open the file containing the set of goals
    txt_file = np.loadtxt('/home/user/Projects/Mobile_robotics/Table.txt', dtype=float, delimiter =',')

    # txt_file = open('/home/user/Projects/Mobile_robotics/Table.txt', 'r')
    size_file = len(txt_file)
    # Read the goal and reach it
    #  The first destination is the further away from the robot position
    destination= 10 
    while(size_file>0):
        remove_from_table()
        print('destination',txt_file[destination])
        txt_file = txt_file[np.argsort(txt_file[:, 4])]
        xx, yy = reach_goal(txt_file[destination], client)
        rospy.loginfo("Point ("+str(xx)+','+str(yy)+") reached")
        txt_file = np.loadtxt('/home/user/Projects/Mobile_robotics/Table.txt', dtype=float, delimiter =',')
        size_file = len(txt_file)
        if size_file < destination:
            destination = -1
        remove_from_table()


    

    print('Final goal reached!')

   # Close the file containing the set of goals
    # txt_file.close()
  
# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

