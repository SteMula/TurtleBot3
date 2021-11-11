#!/bin/bash
# ####################################################################
# Make sure that the file in the script folder are executable file
# ####################################################################
clear
cd
cd turtle_ws
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=burger
# Run roscore if it is not running
if pgrep -x roscore >/dev/null
then
    echo "roscore is running"
else
    echo "Starting roscore"
    gnome-terminal -e roscore 
    echo "roscore started"
    sleep 4
    read -n 1 -s -r -p "Press any key to continue"
fi


# Open the simulation of the TutleBot3 burger in Gazebo in the house environment if it is not running
if pgrep -x gzserver >/dev/null
then
    echo "Gazebo is running"
    read -n 1 -s -r -p "Press any key to continue"
else
    while : ; do
	echo "Would you like to change the layout of the map or change the robot spawn point?[y/n]"
	read answer
	if [ $answer = y ]
	then
	    echo "Enter the desired x coordinate (default: -3.0)"
	    read xx
	    echo "Enter the desired y coordinate (default: 1.0)"
	    read yy
	    echo "Starting Gazebo"
	    gnome-terminal -e "sh -c 'roslaunch turtlebot3_big_house turtlebot3_big_house.launch gui:=true x_pos:=$xx y_pos:=$yy'"
	    echo "Gazebo started"
	    sleep 14
	    read -n 1 -s -r -p "Make the desired changes then press any key to continue"
	    echo " "
	    break
	elif [ $answer = n ]
	then
	    echo "Starting Gazebo"
	    gnome-terminal -e 'sh -c "roslaunch turtlebot3_big_house turtlebot3_big_house.launch gui:=true"'
	    echo "Gazebo started"
	    sleep 14
	    read -n 1 -s -r -p "Press any key to continue"
	    echo " "
	    break
	else
	    echo "Wrong input"
	fi
    done
fi




