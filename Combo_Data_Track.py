# Import Libraries
import Track_Data_Funcs
from Track_Data_Funcs import *
import Header
from Header import *

##################################
# Setup
##################################
# LJ Setup
if LJON == 1: # If using LabJack. It's rare that this won't be the case
	[handle, info] = find_LJ() # Connect to LabJack and collect information on it

# ??? Remove?
# Compass/Accelerometer Setup. It's rare that this would be on 
# if ComAccelON == 1:
# 	# Set up voltage output
# 	CA_name = 'DAC0' # Set DAC0 to voltage for chip
# 	CA_voltage = 3.3  # 3.3 Volts
# 	ljm.eWriteName(handle, CA_name, CA_voltage) # Send info to LabJack
# 	lua_s_name = 'CA_reader.lua' # Lua Compass/Accel reader
# 	run_lua(handle, lua_s_name) # Send lua script to run on LabJack continuously

# Check Power Meter On. It should be on before this script is started
if PMON == 1:
	check_PM(PM_fpath)

# Adjust Pyrheliometer AIN sensitivity
if PyrON == 1:
	Pyr_range_name = Pyr_AIN + '_RANGE'
	Pyr_AIN_range = 0.01
	ljm.eWriteName(handle, Pyr_range_name, Pyr_AIN_range)

# Initiate log and data files
header = build_header(CJCON, TCON, TC_num, PyrON, ComAccelON, LTON, PMON) # Create Header
if LJON == 1:
	init_files(fd_path, fl_path, info, header) # Initiate files (if necessary)
else:
	init_files(fd_path, fl_path, [0, 0, 0, 0, 0, 0], header) # Initiate files (if necessary)

# Handle Ctrl C. This is mostly copied and pasted from LabJack's website
if not sys.platform.startswith("win32"):
    raise ValueError("Unsupported platform: " + sys.platform)
kernel32 = ctypes.CDLL("Kernel32.dll")

def ctrlc_handler(dwCtrlType):
	print("Python ctrlc_handler called with dwCtrlType " + str(dwCtrlType))
	
	ljm.eWriteName(handle, FIOW, 0)
	ljm.eWriteName(handle, FIOE, 0)
	ljm.eWriteName(handle, FION, 0)
	ljm.eWriteName(handle, FIOS, 0)
	ljm.closeAll()

ctrlc_callback_type = ctypes.WINFUNCTYPE(None, ctypes.c_int)
cc_h = ctrlc_callback_type(ctrlc_handler)
success = kernel32.SetConsoleCtrlHandler(cc_h, True)
if not success:
	ValueError("SetConsoleCtrlHandler failed")

##################################
# Run
##################################

# Find the sun at first
if TrackON == 1:
	Track(handle, AIN_NS, LT_moveN, LT_stopN, FION, LT_moveS, LT_stopS, FIOS, AIN_EW, LT_moveW, LT_stopW, FIOW, LT_moveE, LT_stopE, FIOE)

# Read clock time to compare later
ctime0 = time.perf_counter()

# Tracking and Data Collection loop
while True:

	# Import header each loop to allow for updated parameters each loop
	importlib.reload(Header) 
	from Header import *
	
	# This if statement is just for if only the Power Meter is being used
	# ????? Move Higher?
	if LJON == 0:
		handle = 0
	
	# Collect data and add to file 
	outstr = collect_data(handle, CJCON, CJCAIN, TCON, TC_num, TC_AIN_start, TC_AIN_vec, PyrON, Pyr_AIN, ComAccelON, LTON, AIN_D, AIN_NS, AIN_EW, PMON, PM_fpath) # Collect data
	append_data_file(fd_path, outstr) # Add data to data file
	
	# Print output to screen
	if PrintOut == 1:
		print(header)
		print(outstr)
	
	# Prepare for next loop
	ctime1 = time.perf_counter() # Check clock time again 
	dctime = ctime1 - ctime0 #  Compare clock time measurements 
	
	# If dctime is too low, you need to pause  briefly so that different components don't get in each other's way
	if dctime < 0.1:
		time.sleep(0.1)
	
	# Tracking Loop
	if TrackON == 1:
				
		# If cycle time is sufficient, track
		if dctime > cycletime:
			Track(handle, AIN_NS, LT_moveN, LT_stopN, FION, LT_moveS, LT_stopS, FIOS, AIN_EW, LT_moveW, LT_stopW, FIOW, LT_moveE, LT_stopE, FIOE) # Track function 

			ctime0 = time.perf_counter() # Check clock time for next loop

		# if dctime is too low do not track
		# ??? Not sure if this is necessary	
		elif LJON==1:
			ljm.eWriteName(handle, FIOW, 0)
			ljm.eWriteName(handle, FIOE, 0)
			ljm.eWriteName(handle, FION, 0)
			ljm.eWriteName(handle, FIOS, 0)