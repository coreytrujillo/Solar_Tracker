#########################
# File Input
#########################

# floc = './test/'
# frootname = 'test'
floc = '../../../Box_Concept/Box_Experiments/221018_HiRez_Quartz/' # Working Directory
frootname = 'HiRez_Quartz' # File name root (do NOT include date code)

#########################
# On / Off Variables
#########################

# Mechanism on/of (1 = on, 0 = off)
LJON = 1 # LabJack
TrackON = 0 # Tracker

# Sensor on/of (1 = on, 0 = off)
TCON = 1 # Thermocouples
CJCON = 1 # Cold Junction Sensor

PyrON = 1 # Pyrheliometer
LTON = 1 # Light Tower

PMON = 0 # Power Meter
ComAccelON = 0 # Compass and Accelerometer

#####################################
# Sensor AIN assignments
###################################
# AIN numbers on expansion boards for thermocouples
X2 = [0, 1, 2, 3, 120, 121, 122, 123, 124, 125, 126, 127]
X3 = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61]
X4 = [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85]
X5 = [96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109]

# Which Board is plugged into which port
B1 = X2
B2 = X3
B3 = X4
B4 = X5

# TC Input
# TC_AIN_vec = B1[5:12] + B2 + B3 + B4
TC_AIN_vec = B1[5:12] + B2 + B3[0:6]

TC_num = len(TC_AIN_vec) # Number of Thermocouples
TC_AIN_start = TC_AIN_vec[0] # AIN start for thermocouples

# Cold junction AIN
CJCAIN = B1[0]

# Light Tower AINs
AIN_D = 'AIN' + str(B1[1])# Direct LT AIN (Brown Wire)
AIN_NS = 'AIN' + str(B1[2]) # NS LT AIN (White Wire)
AIN_EW = 'AIN' + str(B1[3]) #'AIN99' # EW LT AIN (Green Wire)

# Pyrheliometer Input AINs
Pyr_AIN = 'AIN' + str(B1[4]) # Pyr AIN

###################################
# Tracker Variables
###################################
# Optimal light tower values (mV)
LTNS_opt =  6.5
LTEW_opt = 5

# Cycle Time (sec)
cycletime = 30

# Light Tower variances and boundaries
LTNS_var_N = 0.5#0.40
LTNS_var_S = LTNS_var_N
LTEW_var_E = 0.2
LTEW_var_W = 2
LTNS_backstop = 0.05
LTEW_backstop = 0.1

# NSEW Relay Controls
FIOS = 'FIO0' # South
FION = 'FIO1' # North
FIOW = 'FIO2' # West
FIOE = 'FIO3' # East

# Light Tower move and stop values
LT_moveN = LTNS_opt - LTNS_var_S
LT_moveS = LTNS_opt + LTNS_var_N
LT_moveE = LTEW_opt + LTEW_var_W
LT_moveW = LTEW_opt - LTEW_var_E
LT_stopN = LT_moveS - LTNS_backstop
LT_stopS = LT_moveN + LTNS_backstop
LT_stopE = LT_moveW + LTEW_backstop
LT_stopW = LT_moveE - LTEW_backstop

# Print NSEW values
if False: #LT_debug == 1:
	print('Move East', LT_moveE)
	print('Stop East', LT_stopE)
	print('Move West', LT_moveW)
	print('Stop West', LT_stopW)
	print('Move North', LT_moveN)
	print('Stop North', LT_stopN)
	print('Move South', LT_moveS)
	print('Stop South', LT_stopS)
	print('---------------------')


## Don't Change anything below this line!
##############################################################################
# File paths
###########################
from datetime import datetime
fd_path = floc + datetime.now().strftime('%y%m%d') + '_' + frootname + '_data.csv' # Data file path
fl_path = floc + datetime.now().strftime('%y%m%d') + '_' + frootname + '.log' # Log file path

# fd_path = floc + '220315' + '_' + frootname + '_data.csv' # Data file path


# Power meter

PM_floc = floc
PM_fname = datetime.now().strftime('%y%m%d') + '_Power_Data.csv'
PM_fpath = PM_floc + PM_fname # Power meter file path