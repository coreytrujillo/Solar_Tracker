# Libraries
import Track_Data_Funcs
from Track_Data_Funcs import *
import Header
from Header import *

##################################
## Setup
##################################
# LJ Setup
# if LJON == 1:
	# [handle, info] = find_LJ() # Connect to LabJack and collect information on it
if LJON == 1:
	[handle, info] = find_LJ() # Connect to LabJack and collect information on it

# Compass/Accelerometer Setup
if ComAccelON == 1:
	# Set up voltage output
	CA_name = 'DAC0' # Set DAC0 to voltage for chip
	CA_voltage = 3.3  # 3.3 Volts
	ljm.eWriteName(handle, CA_name, CA_voltage) # Send info to LabJack
	lua_s_name = 'CA_reader.lua' # Lua Compass/Accel reader
	run_lua(handle, lua_s_name) # Send lua script to run on LabJack continuously

# Check Power Meter On
if PMON == 1:
	check_PM(PM_fpath)

# Initiate log and data files
header = build_header(TCON, TC_num, PyrON, ComAccelON, LTON, PMON) # Create Header\
if LJON == 1:
	init_files(fd_path, fl_path, info, header) # Initiate files (if necessary)
else:
	init_files(fd_path, fl_path, [0, 0, 0, 0, 0, 0], header) # Initiate files (if necessary)

# Handle Ctrl C
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
## Run
##################################
iter = 1
ctime0 = time.perf_counter()

# Find the sun
if TrackON == 1:
	Track(handle, AIN_NS, LT_moveN, LT_stopN, FION, LT_moveS, LT_stopS, FIOS, AIN_EW, LT_moveW, LT_stopW, FIOW, LT_moveE, LT_stopE, FIOE)
while True:
	importlib.reload(Header)
	from Header import *
	
	if TrackON == 0:
		handle = 0
	outstr = collect_data(handle, TCON, TC_num, TC_AIN_start, PyrON, Pyr_AIN, ComAccelON, LTON, AIN_D, AIN_NS, AIN_EW, PMON, PM_fpath) # Collect data
	append_data_file(fd_path, outstr) # Add data to data file
	
	# Print output to screen
	print('Iteration:', iter)
	print(header)
	print(outstr)
	
	# Prepare for next loop
	iter = iter + 1
	time.sleep(0.1)
	
	# If cycle time is up, track
	if TrackON == 1:
		ctime1 = time.perf_counter() # Check cycle end time 
		dct = ctime1 - ctime0
		print('Cycle Time: %0.1f seconds ' %dct)
		
		# If cycle time is up, track
		if dct > cycletime:
			Track(handle, AIN_NS, LT_moveN, LT_stopN, FION, LT_moveS, LT_stopS, FIOS, AIN_EW, LT_moveW, LT_stopW, FIOW, LT_moveE, LT_stopE, FIOE)
			ctime0 = time.perf_counter()
				
		elif LJON==1:
			ljm.eWriteName(handle, FIOW, 0)
			ljm.eWriteName(handle, FIOE, 0)
			ljm.eWriteName(handle, FION, 0)
			ljm.eWriteName(handle, FIOS, 0)