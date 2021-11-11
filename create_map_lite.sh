#!/bin/bash
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
fi

# Start GAZEBO
gnome-terminal -e 'sh -c "roslaunch turtlebot3_big_house turtlebot3_big_house.launch gui:=false"'
sleep 4
echo "GAZEBO launched"
sleep 4

# Start the SLAM
gnome-terminal -e 'sh -c "roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping"'
sleep 4
echo "SLAM launched"
sleep 4

# Start the MOVE BASE
gnome-terminal -e 'sh -c "roslaunch turtlebot3_navigation move_base.launch"'
sleep 4
echo "MOVE launched"
sleep 4

