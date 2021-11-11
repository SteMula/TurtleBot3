#!/usr/bin/env python3
# license removed for brevity

import rospy

# Brings in the SimpleActionClient
import actionlib

# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def reach_goal(destination, client):
    coord = destination.split(',')

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
    txt_file = open('/home/user/Projects/Mobile_robotics/navigation_goals.txt', 'r')

   # Read the goal and reach it
    for destination in txt_file:
        xx, yy = reach_goal(destination, client)
        rospy.loginfo("Point ("+str(xx)+','+str(yy)+") reached")

    print('Final goal reached!')

   # Close the file containing the set of goals
    txt_file.close()
  
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

