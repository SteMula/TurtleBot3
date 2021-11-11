#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped

def amcl_init():
    pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=1, latch=True)
    rospy.init_node('amcl_init', anonymous=False)

    # Acquiring inputs
    # while True:
	# 	try:
	# 		xx = input("Enter the initial x coordinate of the robot ")
	# 		try:
	# 			float(xx)
	# 			break;
	# 		except ValueError:
	# 			print ("This is not a number. Please enter a valid number")
	# 	except NameError:
	# 			print ("Name not defined. Please enter a valid number")
		
    # while True:
	# try:
	#     yy = input("Enter the initial y coordinate of the robot ")
	#     try:
	#         int(yy)
	#         break;
	#     except ValueError:
	# 	try:
	# 	    float(yy)
	# 	    break;
	#         except ValueError:
	# 	    print ("This is not a number. Please enter a valid number")
	# except NameError:
	#     print ("Name not defined. Please enter a valid number")

    # Construction of the message
    pose_stamped = PoseWithCovarianceStamped()
    pose_stamped.header.frame_id = 'map'
    pose_stamped.header.stamp = rospy.Time.now()

    pose_stamped.pose.pose.position.x = float(-3.0) 
    pose_stamped.pose.pose.position.y = float(1.0) 
    pose_stamped.pose.pose.position.z = 0.0

    pose_stamped.pose.pose.orientation.x = 0.0
    pose_stamped.pose.pose.orientation.y = 0.0
    pose_stamped.pose.pose.orientation.z = 0.01
    pose_stamped.pose.pose.orientation.w = 0.99

    pose_stamped.pose.covariance = [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]

    rospy.loginfo("Publishing initial pose with covariance for amcl")
    
    pub.publish(pose_stamped)
    rospy.spin()
    
if __name__ == '__main__':
    try:
        amcl_init()
    except rospy.ROSInterruptException:
        pass

