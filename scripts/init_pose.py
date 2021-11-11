#!/usr/bin/env python3
import rospy
import tf
import tf2_msgs.msg
import geometry_msgs.msg


base_tf = geometry_msgs.msg.Transform()
message_read = False

def readTF(msg):
	global base_tf
	global message_read
	for pose_tf in msg.transforms:
		if pose_tf.child_frame_id == "base_footprint":
			base_tf = pose_tf.transform
	message_read = True
	return 

if __name__ == '__main__':
	rospy.init_node('my_init_node', anonymous=True)
	sub_tf = rospy.Subscriber("tf", tf2_msgs.msg.TFMessage, readTF)
	pub_init = rospy.Publisher("/initialpose", geometry_msgs.msg.PoseWithCovarianceStamped, queue_size = 10)
	
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		if message_read:
			base_pose = geometry_msgs.msg.PoseWithCovarianceStamped()
			base_pose.header.stamp = rospy.get_rostime()
			base_pose.header.frame_id = "map"
			base_pose.pose.pose.position.x = base_tf.translation.x
			base_pose.pose.pose.position.y = base_tf.translation.y
			base_pose.pose.pose.position.z = base_tf.translation.z
			base_pose.pose.pose.orientation = base_tf.rotation
		
			pub_init.publish(base_pose)
		rate.sleep()
