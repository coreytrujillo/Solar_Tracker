#########################
# File Input
#########################

# floc = './test/'
# frootname = 'test'
floc = '../../Experiments/210622_Power_Benchmark/' # Working Directory
frootname = 'Power_Benchmark' # File name root (do NOT include date code)

#########################
# On / Off Variables
#########################

# Mechanism on/of (1 = on, 0 = off)
LJON = 1 # LabJack
TrackON = 1 # Tracker

# Sensor on/of (1 = on, 0 = off)
TCON = 0 # Thermocouples
PyrON = 1 # Pyrheliometer
ComAccelON = 0 # Compass and Accelerometer
LTON = 1 # Light Tower
PMON = 1 # Power Meter

# Debuggers
LT_debug = 1

#####################################
# Sensor AIN assignments
###################################
# TC Input
TC_num = 8 # Number of Thermocouples
TC_AIN_start = 0 # AIN start for thermocouples

# Pyrheliometer Input
Pyr_AIN = 'AIN12' # Pyr AIN

# Light Tower
AIN_D = 'AIN9' # Direct LT AIN
AIN_NS = 'AIN10' # NS LT AIN
AIN_EW = 'AIN11' # EW LT AIN

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
LTEW_var_E = 1
LTEW_var_W = 2.5
LTNS_backstop = 0.05
LTEW_backstop = 0.4

# NSEW Relay Controls
FIOS = 'FIO2' # South
FION = 'FIO3' # North
FIOW = 'FIO4' # West
FIOE = 'FIO5' # East

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
if 1==1: #LT_debug == 1:
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

# Power meter

PM_floc = floc
PM_fname = datetime.now().strftime('%y%m%d') + '_Power_Data.csv'
PM_fpath = PM_floc + PM_fname # Power meter file path