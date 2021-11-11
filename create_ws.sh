#!/bin/bash
# ####################################################################
# Make sure that the file in the script folder are executable file
# ####################################################################
rosclean purge -y # remove old log files
clear
cd
rm -rf turtle_ws
sleep 1 
echo "removed"
echo ""
mkdir -m 777 -p turtle_ws/src    #here you can change the name to the folder
cd turtle_ws/src
git clone -b melodic-devel https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b melodic-devel https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b melodic-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
git clone -b melodic-devel https://github.com/hrnr/m-explore.git
git clone https://github.com/awesomebytes/occupancy_grid_python.git


# ricorda di cambiare "turtlebot3_gazebo" in "turtlebot3_big_house"
cp -R ~/turtlebot3_big_house ~/turtle_ws/src/turtlebot3_simulations
sleep 2
cd
cd turtle_ws/src
catkin_create_pkg simple_navigation_goals rospy std_msgs geometry_msgs actionlib move_base_msgs nav_msgs std_srvs tf math
cp -R ~/scripts ~/turtle_ws/src/simple_navigation_goals
cd
cd turtle_ws
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=burger
#roslaunch turtlebot3_big_house turtlebot3_big_house.launch gui:=true



