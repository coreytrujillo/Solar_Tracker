#############################################
# Variables to Change
#############################################

from datetime import datetime

# File Input
# floc = './test/'
floc = '../../Experiments/210525_AutoTracker_Calibration/' # Working Directory
frootname = 'AutoTracker_calib' # File name root (do NOT include date code)

# Sensor on/of (1 = yes, 0 = no)
TCON = 0 # Thermocouples
PyrON = 1 # Pyrheliometer
ComAccelON = 1 # Compass and Accelerometer
LTON = 1 # Light Tower
PMON = 1 # Power Meter
TrackON = 1 # Tracker

################################################################
# TC Input
TC_num = 4 # Number of Thermocouples
TC_AIN_start = 0 # AIN start for thermocouples

# Pyrheliometer Input
Pyr_AIN = 'AIN12' # Pyr AIN

# Light Tower
AIN_D = 'AIN9' # Direct LT AIN
AIN_NS = 'AIN11' # NS LT AIN
AIN_EW = 'AIN10' # EW LT AIN

# Power meter
PM_floc = floc
# PM_fname =  datetime.now().strftime('%y%m%d') + '_Power_Data.csv'
PM_fname =  datetime.now().strftime('%y%m%d') + '_Power_Data.csv'

###################################
# Tracker motion variables
###################################



## Don't Change anything below this line!
##############################################################################
# File paths
fd_path = floc + datetime.now().strftime('%y%m%d') + '_' + frootname + '_data.csv' # Data file path
fl_path = floc + datetime.now().strftime('%y%m%d') + '_' + frootname + '.log' # Log file path
PM_fpath = PM_floc + PM_fname # Power meter file path

# CSV separator
sep = ','