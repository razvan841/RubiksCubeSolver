# How to use

Run pip install -r requirements.txt for all the required libraries
Create a .env file and set up the following variables:

- PORT = any value that is not reserved (65432 for example)
- IP_ADDRESS = for testing use localhost (127.0.0.1); for actual deployment, use '0.0.0.0' (scans the whole network)
- MODEL_ID = 65432
- You also need an api_key for the edge impulse api ('ei_fd5aace96f94d5edb2becbb095f2957bd60b5682be090b2d25fc67e99066d4dd')

If you want to use only the virtual version of the project, run the cube_gui.py file
The full system is used by running the main.py file. Make sure the camera index matches the desired one. In order to use the camera
on the box, you will need to install a driver: <https://support.logi.com/hc/nl/articles/360024692954--Downloads-HD-Webcam-C270>

In order to set up a server, you need both the Raspberry Pi and the ESP to be on the same network. Eduroam will not work, we recommend setting up a personal hotspot on the phone or laptop.
In the main.py, there is a variable that sets which solver to use. For the python solver, make this variable be "optimal", otherwise keep it as "uppaal"
In the solver.py file, some paths will need to be setup correctly in order for the UPPAAL solver to work.
First, make sure you have UPPAAL installed and the path to it doesn't include space characters, otherwise the path will be wrong.
There are 6 paths required:

- verifyta_path: path to the \\bin-Windows\\verifyta.exe file in the UPPAAL installation
- solve_path: path to the folder that contains the part-solve file, which is important for the final solution
- model_file: path to the xml spec for UPPAAL
- query_path: path to the query_files directory. make sure this path ends with \\
- solution_file: path to output file
- final_state_file: path to final state file

In case the system is stopped midway through the solve, make sure to reset the xml file for the state of the cube. The initial state should be as following:

int flags[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

int front_face[9] = {-1,-1,-1,-1,-1,-1,-1,-1,-1};
int back_face[9] = {-1,-1,-1,-1,-1,-1,-1,-1,-1};
int right_face[9] = {-1,-1,-1,-1,-1,-1,-1,-1,-1};
int left_face[9] = {-1,-1,-1,-1,-1,-1,-1,-1,-1};
int up_face[9] = {-1,-1,-1,-1,-1,-1,-1,-1,-1};
int down_face[9] = {-1,-1,-1,-1,-1,-1,-1,-1,-1};

These can be found on lines 40-50 in testcube.xml

The Edge Impulse and YOLO models were trained using a Speed Cube, the type of Rubik's Cube use in official competitions. Other types of cubes will most likely not be classified correctly. Before introducing the cube in the robot, make sure you remove the middle patches on all the faces that connect to motors. Additionally, the magnets inside need to be removed so that the motors have enough torque to turn the sides properly.
