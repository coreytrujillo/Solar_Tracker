#############################################
# Variables to Change
#############################################

from datetime import datetime

# File Input
# floc = './test/'
floc = '../../Experiments/210527_LT_Calibration/' # Working Directory
frootname = 'LT_Calibration' # File name root (do NOT include date code)

# Sensor on/of (1 = yes, 0 = no)
LJON = 0 # LabJack
TCON = 0 # Thermocouples
PyrON = 0 # Pyrheliometer
ComAccelON = 0 # Compass and Accelerometer
LTON = 1 # Light Tower
PMON = 0 # Power Meter
TrackON = 0 # Tracker

################################################################
# TC Input
TC_num = 4 # Number of Thermocouples
TC_AIN_start = 0 # AIN start for thermocouples

# Pyrheliometer Input
Pyr_AIN = 'AIN12' # Pyr AIN

# Light Tower
AIN_D = 'AIN9' # Direct LT AIN
AIN_NS = 'AIN10' # NS LT AIN
AIN_EW = 'AIN11' # EW LT AIN

# Power meter
PM_floc = floc
# PM_fname =  datetime.now().strftime('%y%m%d') + '_Power_Data.csv'
PM_fname =  datetime.now().strftime('%y%m%d') + '_Power_Data.csv'

###################################
# Live Plot Variables 
###################################



## Don't Change anything below this line!
##############################################################################
# File paths
# fd_path = floc + datetime.now().strftime('%y%m%d') + '_' + frootname + '_data.csv' # Data file path
fd_path = floc + '210527_' + frootname + '_data.csv'

fl_path = floc + datetime.now().strftime('%y%m%d') + '_' + frootname + '.log' # Log file path

PM_fpath = PM_floc + PM_fname # Power meter file path

# CSV separator
sep = ','