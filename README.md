# TurtleBot3
Before start to run the project:

- Do steps from 1.1.1 to 1.1.4 of the page https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/ 
- If SLAM or gmapping cause issues, try to manually install it with: sudo apt install ros-melodic-slam-gmapping (Be sure to use the correct distribution I have used Melodic with Ubuntu 18.04 LTS in case just adjust the files for your distro)
- install the explore_lite package for the navigation. instructions here: https://github.com/hrnr/m-explore

Once you have downloaded the zip folder, you should extract the file in your "Home". 

You have to change the execution permission for the files ".sh" (go to the Home folder, open terminal and type: "chmod +x *.sh". 

There is also a folder called scripts (I have used Python3 but you can remove the 3 from the first row to use it with Python 2.x) you should repeat the same procedure done for the bash files with the python code.

I suggest to execute first the create_ws.sh. 

Important: In some part of the code I used an absolut path /home/user/... , please remember to replace "user" with your correct admin name.



