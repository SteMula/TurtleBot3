#!/usr/bin/env python3

from occupancy_grid_python import OccupancyGridManager
from nav_msgs.msg import OccupancyGrid
from map_msgs.msg import OccupancyGridUpdate
import rospy
from rospkg import RosPack
import numpy as np


if __name__ == '__main__':
    rospy.init_node('test_occ_grid')
    rospy.loginfo("Initializing")

    map_pub = rospy.Subscriber('/map',
                              OccupancyGrid)
    # update_pub = rospy.Publisher('/map_updates', OccupancyGridUpdate,
    #                              queue_size=1)

    rospy.sleep(1.0)


    ogm = OccupancyGridManager('/map',
                               subscribe_to_updates=False)
    

    L2 = []
    print(ogm.height)
    for  y in np.arange(-10, 9.2,0.5):   # row
        for x in np.arange(-10, 9.2,0.5):  # column
            cost = ogm.get_cost_from_world_x_y(x, y)
            print(x,y,cost)
            L2.append([x,y,cost])
    print(len(L2))

    np.savetxt("/home/user/Projects/Mobile_robotics/get_cost_from_world_x_y.txt", L2, fmt='%.2f',delimiter=',')




