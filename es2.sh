#!/bin/bash
# ####################################################################
# Make sure that the file in the script folder are executable file
# ####################################################################
./create_map_lite.sh
gnome-terminal -e 'sh -c "roslaunch explore_lite explore.launch"'
sleep 60
# Save the map
while : ; do
	echo "Would you like to save the map? This will overwrite the old map [y/n]"
	read answer
	if [ $answer = y ]
	then
	    echo "Saving..."
	    rosrun map_server map_saver -f /home/user/Projects/Mobile_robotics/maps/map
	    sleep 2
	    echo "Map saved"
	    break
	elif [ $answer = n ]
	then
	    echo "The old map is kept"
	    break
	else
	    echo "Wrong input"
	fi
    done
