# Libraries
from labjack import ljm
import time
import importlib
import sys # Scripting functions
import ctypes
import Header_Standalone_Tracker
from Header_Standalone_Tracker import *
import Track_Data_Funcs
import Track_Data_Funcs as TDF

# Connect to LabJack and collect information on it
[handle, info] = TDF.find_LJ() 

###################################
# Handle Ctrl-C
#########################

if not sys.platform.startswith("win32"):
    raise ValueError("Unsupported platform: " + sys.platform)
kernel32 = ctypes.CDLL("Kernel32.dll")

def ctrlc_handler(dwCtrlType):
	print("Python ctrlc_handler called with dwCtrlType " + str(dwCtrlType))
	ljm.eWriteName(handle, FION, 0)
	ljm.eWriteName(handle, FIOS, 0)
	ljm.eWriteName(handle, FIOE, 0)
	ljm.eWriteName(handle, FIOW, 0)
	ljm.closeAll()
		
	

ctrlc_callback_type = ctypes.WINFUNCTYPE(None, ctypes.c_int)
cc_h = ctrlc_callback_type(ctrlc_handler)
success = kernel32.SetConsoleCtrlHandler(cc_h, True)
if not success:
	ValueError("SetConsoleCtrlHandler failed")

#########################################
# Run Tracker
#########################################
# Find sun
TDF.Track(handle)
ctime0 = time.perf_counter() # Set cycle start time 
while True:

	ctime1 = time.perf_counter() # Check cycle end time 
	dct = ctime1 - ctime0
	print('Cycle Time: %0.1f seconds ' %dct)
	
	# If cycle time is up, track
	if dct > cycletime:
		TDF.Track(handle)
		ctime0 = time.perf_counter() # Reset cycle start time