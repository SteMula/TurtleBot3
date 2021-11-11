#!/bin/bash
clear
# ####################################################################
# Make sure that the file in the script folder are executable file 
# ####################################################################
rosclean purge -y
cd
cp -R ~/scripts ~/turtle_ws/src/simple_navigation_goals
cd turtle_ws
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=burger

##################################################################################################
# Run roscore if it is not running
if pgrep -x roscore >/dev/null
then
    echo "roscore is running"
else
    echo "Starting roscore"
    gnome-terminal -e roscore 
    echo "roscore started"
    sleep 4
fi
##################################################################################################
# Start GAZEBO
gnome-terminal -e 'sh -c "roslaunch turtlebot3_big_house turtlebot3_big_house.launch gui:=false"'
sleep 4
echo "GAZEBO launched"
sleep 4
##################################################################################################
# Initialize pose of the robot for the init_pose
echo "Initializing the init_pose"
gnome-terminal -e 'sh -c "rosrun simple_navigation_goals init_pose.py"'
sleep 4
echo "POSE INIT launched"
sleep 4

##################################################################################################
# Initialize pose of the robot for the amcl
echo "Initializing the amcl"
gnome-terminal -e 'sh -c "rosrun simple_navigation_goals amcl_init.py"'
sleep 4
echo "AMCL INIT launched"
sleep 4

##################################################################################################
# Start the navigation with the map
echo "Starting the navigation"
gnome-terminal -e 'sh -c "roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=/home/user/Projects/Mobile_robotics/maps/map.yaml "'
sleep 4
echo "NAV launched"
sleep 4


##################################################################################################
# Start moving around
rosrun simple_navigation_goals simple_navigation_goals.py



