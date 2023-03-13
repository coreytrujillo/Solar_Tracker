# Import libraries
from labjack import ljm # LabJack functions
from datetime import datetime # Date and time
import numpy as np # Numbers and math
import time # For sleep function, pef_counter
import os # For removing files
import sys # Scripting functions
import pandas as pd # For data analysis
import ephem as ep # For predicting Sun's position

# CSV separator
sep = ','

# Connect with LabJack and get handle and information
def find_LJ():
	# Look for LabJack
	lookforLJ = True
	print('Looking for LabJack...')
	while lookforLJ:
		# Try to find LabJack
		try:
			handle = ljm.openS('ANY', 'ANY', 'ANY')  # Get handle (or ID) for T7 device, Any connection, Any identifier
			info = ljm.getHandleInfo(handle) # LabJack Info
			print('Connected to LabJack')
			return(handle, info)
			ljm.closeAll
			lookforLJ = False
			
		# If LabJack isn't found, it's likely not connected. This exception allows the user to connect it, then continue the code
		except:
			print('Not finding a LabJack Connection... \n')
			while True:
				LJ_response = input('Would you like to try again? (y/n) \n')
				if LJ_response == 'y':
					break
				elif LJ_response == 'n':
					sys.exit()
					lookforLJ = False
				else:
					print('Invalid response. Please enter y for yes or n for no\n')

# Initiate log file and data collection file
def init_files(fd_path, fl_path, info, header):
	# fd_path = data file path
	# fl_path = log file path
	# info = LabJack Information
	# header = first line of data collection file
	
	# Initiate logical variables
	needtowrite = True # Need to write?
	needtooverwrite = True # Need to overwrite?	
	
	while needtowrite == True:
		# Try to initate log file and data file
		try:
			# Start log file
			salutation = 'Experiment start at: ' + datetime.now().strftime('%Y-%b-%d %H:%M:%S') + '\n'
			fl = open(fl_path, 'x')
			fl.write(salutation)
			fl.write('Opened a Labjack with device type: %i,\n Connection Type: %i,\n Serial number: %i,\n IP address: %s,\n Port: %i,\n Max bytes per MB: %i\n' %(info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))
			fl.close()
			
			# Start data file
			fd = open(fd_path, 'x')
			fd.write(header + '\n')
			fd.close()
			break
		
		# This exception adresses any issues with initiating a file
		# This would usually be triggered when a file by the same name already exists
		# It gives the user the option to exit the program, delete the existing file, or append it
		except Exception as e:
			print('File initiation failed:', e)
			while needtooverwrite == True:
				a_response = input('Enter a to append, dd to delete and overwrite, or ee to exit\n')
				
				# If user chooses to append the file
				if a_response == 'a':
					salutation_i = 'Experiment contunued at: ' +  datetime.now().strftime('%Y-%b-%d %H:%M:%S') + '\n'
					fl = open(fl_path, 'a')
					fl.write(salutation_i)
					fl.close()
					needtowrite = False
					break
				
				# If user chooses to exit the program
				elif a_response == 'ee':
					print('Exiting Program')
					sys.exit()
					
				# If user chooses to delete the file
				elif a_response == 'dd':
					while True:
						# Confirm Delete
						del_response = input('Are you sure you want to delete and overwrite? (y/n)\n')
						if del_response == 'y':
							os.remove(fl_path)
							os.remove(fd_path)
							needtooverwrite== False
							break
						elif del_response == 'n':
							print('Nothing deleted. Exiting Program. \n')
							sys.exit()
						# If unexpected input is received
						else:
							print('Invalid response. Please enter y for yes or n for no\n')
					break
				
				# If unexpected input is received.
				else:
					print('Invalid response. Please enter y for yes or n for no')

# Append to data file
# This is used when collecting data
def append_data_file(fpath, outstr):
	# fpath = path to file that's being appended
	# outstr = string to append to file 

	f = open(fpath, 'a') # Open file
	f.write(outstr) # Append outstring to file
	f.close() # Close file

# Read Thermocouples from LabJack
def read_LJ_TC(handle, TC_num, TC_AIN_start, TC_AIN_vec, CJCON, CJCAIN):
	# handle = LabJack T7 ID, should be acquired from find_LJ() function
	# TC_num = number of thermocouples
	# TC_AIN_start = first AIN TC's are plugged into ???????
	# TC_AIN_vec = list of TC AINS. Set to 0 for only 1 TC ???????? 
	# CJCON = Cold junciton compensation sensor on/off
	# CJCAIN = AIN cold junction sensor is plugged into.
	
	# Initiate variables
	ain_n = [] # Initiate vector for AIN's connected to TC's
	ain_idx = [] # Initiate vector for TC type
	ain_cnfgA = [] # Initiate vector for Temperature scale
	ain_cnfgB = [] # CJC AIN configuration
	ain_cnfgD = [] # CJC slope
	ain_cnfgE = [] # CJC offset
	ain_rd =[] # Initiate vector of variable to read temps
	
	
	# Create variables for thermocuple settings and measurement
	for i in range(0, TC_num):
		
		# If there's only one TC
		if TC_AIN_vec == 0:
			ain_n.append('AIN' + str(i + TC_AIN_start)) # Create name for AIN as input argument for ljm.eWriteNames
		
		# If there's more than on TC
		else:
			ain_n.append('AIN' + str(TC_AIN_vec[i])) # Create vector of AIN names for ljm.eWriteNames

		ain_idx.append(ain_n[i] + '_EF_INDEX') # Input tag for ljm.eWriteNames: thermocouple type
		ain_cnfgA.append(ain_n[i] + '_EF_CONFIG_A') # Input for ljm.eWriteNames: Temperature scale configuration: 0 for K, 1 for C, 2 for F
		ain_rd.append(ain_n[i] + '_EF_READ_A') # Input for ljm.eWriteNames: Read thermocouple variable
		
		# If using Cold Junction Sensor, prepare configuration setting variables ???? Move down lower to consolidate CJC functions??????
		if CJCON == 1:
			ain_cnfgB.append(ain_n[i] + '_EF_CONFIG_B') # CJC AIN configuration
			ain_cnfgD.append(ain_n[i] + '_EF_CONFIG_D') # CJC slope
			ain_cnfgE.append(ain_n[i] + '_EF_CONFIG_E') # CJC offset
	
	# Indentify TC settings for LabJack
	v_idx = 22*np.ones((TC_num,1),float) # Input for ljm.eWriteNames: 22 = Type K thermocouple
	cnfgA = np.ones((TC_num,1),float) # Input for ljm.eWriteNames: Set thermocouple to read in Celcius
	
	# Comminicate settings to LabJack
	ljm.eWriteNames(handle, TC_num, ain_idx, v_idx) # Identify which AINs are being used as Type K Thermocouples
	ljm.eWriteNames(handle, TC_num, ain_cnfgA, cnfgA) # Configure LabJack for temperature scale
	
	# Setup Cold Juction Compensation Sensor, if being used
	if CJCON == 1:
		# Set configuration values for LM34
		# See https://labjack.com/support/datasheets/t-series/ain/extended-features/thermocouple
		cnfgB = CJCAIN*np.ones((TC_num,1),float) # AIN which LM34 is plugged into
		cnfgD = 55.56*np.ones((TC_num,1),float) # CJC Slope for LM34
		cnfgE = 255.37*np.ones((TC_num,1),float) # CJC offset for LM34. This value should always be 
		
		# Write values to LabJack ????????????
		ljm.eWriteNames(handle, TC_num, ain_cnfgB, cnfgB)
		ljm.eWriteNames(handle, TC_num, ain_cnfgD, cnfgD)
		ljm.eWriteNames(handle, TC_num, ain_cnfgE, cnfgE)
	
	# Read temperature values from LabJack
	Temps = ljm.eReadNames(handle, TC_num, ain_rd)
	TCVs = ljm.eReadNames(handle, TC_num, ain_n)
	
	# Output Temperatures
	return Temps, TCVs

# Read temperature values from cold junction temperature sensor LM34
# See https://labjack.com/support/datasheets/t-series/ain/extended-features/thermocouple
def read_LJ_CJC(handle, AIN):
	# Set up CJC Temperature Sensor
	CJCT = ljm.eReadName(handle, 'AIN' + str(AIN) + '_EF_READ_C') # Read temperature from LM34
	CJCV = ljm.eReadName(handle, 'AIN' + str(AIN) + '_EF_READ_B') # Read calculated voltage for LM34
	
	return CJCT, CJCV

# Read Pyrheliometer Voltage from LabJack
def read_LJ_Pyr(handle, AIN):
	# handle = LabJack handle
	# AIN = AIN the Pyrheliometer is plugged into
	s = 7.83e-6 # Radiometer sensitivity [V/W/m2]
	Pyr_O = ljm.eReadName(handle, AIN) # Pyrheliometer output in Volts
	Pyr_E = Pyr_O/s # Calculated Solar irradiance [W/m2]
	
	# Output values
	return Pyr_O, Pyr_E

# Run a Lua Script (for compass and accelerometer readings) ????????? Delete?????????
def run_lua(handle, lua_s_name):
	# handle = LabJack handle
	# lua_s_name = name of lua script to run
	
	# Read Lua script
	with open(lua_s_name, 'r') as myfile:
		lua_script = myfile.read()
	script_length = len(lua_script)

	# Clear any running scripts from labjack
	ljm.eWriteName(handle, 'LUA_RUN', 0) # Stop running lua scripts on LJ
	time.sleep(1) # Wait for labjack to clear all firmware/variables
	ljm.eWriteName(handle, 'LUA_RUN', 0) # Stop running lua scripts again

	# Write the size and the Lua Script to the device
	ljm.eWriteName(handle, 'LUA_SOURCE_SIZE', script_length)
	ljm.eWriteNameByteArray(handle, 'LUA_SOURCE_WRITE', script_length, bytearray(lua_script, encoding='utf8'))

	# Start the script with debug output enabled
	ljm.eWriteName(handle, 'LUA_DEBUG_ENABLE', 0)
	ljm.eWriteName(handle, 'LUA_DEBUG_ENABLE_DEFAULT', 0)
	ljm.eWriteName(handle, 'LUA_RUN', 1)

# Normalize magnetometer readings to outupt between -1 and 1 ??????????? delete ???????????
def normalize_mag(lo, hi, inp):
	# lo = lowest possible magnetometer output
	# hi = highest possible magnetometer output
	m = 2/(hi - lo) # slope
	b = 1-m*hi # intercept
	outp = m*inp + b # y = mx + b
	
	# If an unexpected value is received, output that value to the log file
	if outp > 1 or outp < -1:
		print('Unexpected Value in Nomalization:', inp)
		fl = open(fl_path, 'a')
		fl.write('Mag value out of range! Received: ' + str(inp) + 'Should have received' + str(lo) + 'or' + str(hi) + '\n')
		fl.close
	return outp


# Read Compass and Acceleromter ??????????? Delete ????????????????
def read_LJ_CA(handle):
	# time.sleep(0.1) # Pause between readings 
	mX0 = ljm.eReadName(handle, 'USER_RAM0_F32') # dirty mag x
	mZ0 = ljm.eReadName(handle, 'USER_RAM1_F32') # dirty mag z
	mY0 = ljm.eReadName(handle, 'USER_RAM2_F32') # dirty mag y
	aX = ljm.eReadName(handle, 'USER_RAM3_F32') # Accelerometer X
	aY = ljm.eReadName(handle, 'USER_RAM4_F32') # Accel Y
	aZ = ljm.eReadName(handle, 'USER_RAM5_F32') # Accel Z
	
	
	# Normalize magnetic values
	# Values calibrated based on experience
	# mX = (-371, 520, mX0)
	# mY = (-543, 431, mY0)
	# mZ = (-671, 317, mZ0)
	# mX = normalize_mag(-346, 563, mX0)
	# mY = normalize_mag(-525, 378, mY0)
	# mZ = normalize_mag(-671, 309, mZ0)
	
	mX = mX0
	mY = mY0
	mZ = mZ0
	
	return mX, mY, mZ, aX, aY, aZ

# Average Compass and accelerometer values to reduce noise ?????????? Delete ????????????????
def ave_CA(handle):
	# Number of data points to average
	loop = 1	
	
	# Initiate running sums
	summX = 0
	summY = 0
	summZ = 0
	sumaX = 0
	sumaY = 0
	sumaZ = 0
	
	# Sum values 
	for i in range (0,loop):
		time.sleep(0.1)
		[mX, mY, mZ, aX, aY, aZ] = read_LJ_CA(handle)
		summX += mX
		summY += mY
		summZ += mZ
		sumaX += aX
		sumaY += aY
		sumaZ += aZ

	
	# Average values
	avemX = summX/loop
	avemY = summY/loop
	avemZ = summZ/loop
	aveaX = sumaX/loop
	aveaY = sumaY/loop
	aveaZ = sumaZ/loop

	return avemX, avemY, avemZ, aveaX, aveaY, aveaZ


# Calculate elevation angle ???????????? Delete????????????????
def el_ang(up, face):
	# up = up vector
	# face = vector that defines plane of the face of the collectors
	
	# Calculate elevation angle
	p1 = np.dot(up,face)*face # Vector projection on plane vector
	p2 = up - p1 # Vector projection on plane
	el = np.arccos(np.dot(p2,up)/(np.linalg.norm(p2)*np.linalg.norm(up)))*180/np.pi # Elevation angle
	
	return el

# Calculate azimuthal Angle ???????????? Delete????????????????
def az_ang(up, top, north):
	# up = vector pointing directly up
	# top = vector pointing from bottom top of face of solar collectors (y)
	# north = north vector
	
	# Calculate projection of angles in necessary planes
	p1 = np.dot(north, up)*up # projection of north vector on up vector
	p2 = north - p1 # North projection in level plane
	p3 = np.dot(top, up)*up # projection of vector pointing to top of collectors on up vector
	p4 = top - p3 # Direction of back of solar collector in level plane
	
	# Determine clockwise or counterclockwise angle
	p5 = np.cross(p2,p4) # Cross product between north and back projections in level plane
	p6 = np.dot(p5,up) # Comparison between p5 and up
	
	
	# Calculate Azimuth angle
	az = np.arccos(np.dot(p4,p2)/(np.linalg.norm(p4)*np.linalg.norm(p2)))*180/np.pi
	# az = np.dot(north,top)
	# print('AZ', az)
	
	# Correct to make clockwise from north
	if p6 < 0:
		az = 360 - az
	return az

# Look up true az and el angles along with calculated ones ???????????? Delete????????????????
def solar_angs(handle):
	[mX, mY, mZ, aX, aY, aZ] = read_LJ_CA(handle)
	
	# Azimuth and elevation Readings
	up = np.array([-aX,-aY,-aZ]) # Accelerometer readings
	face = np.array([0,0,-1]) # Opposite direction of quartz rods
	top = np.array([0,-1,0]) # Opposite direction pointing at top of collectors
	north = np.array([mX,mY,mZ]) # Switch these around!!!!!!!!!!!!
	el = el_ang(up, face) # Elevation angle
	azim = az_ang(up, top, north) # Azimuth angle
	
	# Averaged readings
	[avemX, avemY, avemZ, aveaX, aveaY, aveaZ] = ave_CA(handle)
	avenorth = np.array([avemX, avemY, avemZ])
	aveup = np.array([-aveaX, -aveaY, -aveaZ])
	aveel = el_ang(aveup, face)
	aveaz = az_ang(aveup, top, avenorth)
	faaa = np.array([0,0,1])
	
	# True Az/ El
	# PyEphem constants for calculating Sun's angles
	lab = ep.Observer() # Observing from lab
	lablat = 39.781763 # lab latitude
	lablon = -104.910462 # lab longitude
	lab.lat = str(lablat) # input lat to pyephem
	lab.lon = str(lablon) # input lon to pyephem
	lab.elevation = 1610 # lab elevation
	Ang = ep.Sun(lab)
	az_True = float(Ang.az) * 180/ np.pi # True azimuth in degress
	el_True = float(Ang.alt) *  180/ np.pi # True elevation in degrees
	
	if 1 == 1:
		print('El:', el)
		print('El Ave:', aveel)
		print('ElT:', el_True)
		print('Az:', azim)
		print('Az Ave:', aveaz)
		print('AzT:', az_True)
	
	return el, azim, aveel, aveaz, az_True, el_True 

# Read Light Tower voltages from LabJack
def read_LJ_LT(handle, AIN_D, AIN_NS, AIN_EW):
	# handle = LabJack handle
	# AIN_D = AIN for direct light sensor
	# AIN_NS = AIN for north/south light sensor
	# AIN_EW = AIN for east/west light sensor
	
	# Collect values from LabJack
	LT_direct = ljm.eReadName(handle, AIN_D) # Input from top sensor
	LT_NS = ljm.eReadName(handle, AIN_NS) # North/South Voltage reading
	LT_EW = ljm.eReadName(handle, AIN_EW) # East/West votage reading
	
	return LT_direct, LT_NS, LT_EW

#  Check that power meter is writing to file: the power meter requires its own software called PowerMax PC and cannot be read directly with Python. Therefore, the output of the power meter data to a separate file then read it from there. The power meter must be outputting data before it can be read, so this function checks that the power meter is outputting data.
def check_PM(PM_fpath):
	# PM_fpath = file path for power meter data
	
	lookPM = True # look for power meter?
	
	while lookPM:
		
		try:
			# Read Power Meter file
			# ???????????? Rewrite to check if numlines is growing??????????????
			PMf = open(PM_fpath, 'r') # Open file
			numlines = len(PMf.readlines()) # Get the number of lines
			PMf.close()  # close file
			
			# Check to ensure file contains more than just the header
			if numlines >3: 
				print('Reading Power Meter data!')
				print(numlines)
				lookPM = False

			# If the Power meter is not collecting data, this conditional gives the user time to start it	
			else: 
				print('\n')
				while True:
					PM_response = input('Power Meter file is very short and may not be collecting data!!\n Would you like to try again? (y/n)\n ')
					if PM_response == 'y':
						break
					elif PM_response == 'n':
						ExitProgram = input('Would you like to exit the program?\n')
						if ExitProgram == 'y':
							sys.exit()
							lookPM = False
						elif ExitProgram == 'n':
							print('Program not exiting - power data may not be collected \n')
							lookPM = False
							break
						else:
							print('Invalid response. Please enter y for yes or n for no\n')
					else:
						print('Invalid response. Please enter y for yes or n for no\n')
		
		# This exception handles an error reading the PM file. I'm not sure if this will ever be used
		except Exception as e:
			print('Power Meter Error:', e)
			while True:
				PM_response = input('Would you like to try again? (y/n) \n')
				if PM_response == 'y':
					break
				elif PM_response == 'n':
					print('Exiting program')
					lookPM = False
					sys.exit()
				else:
					print('Invalid response. Please enter y for yes or n for no\n')

# Read Power Meter data from its own output file
def read_PM(PM_fpath):
	PM_data = pd.read_csv(PM_fpath, header = 2, index_col = 'Timestamp') # Read power file
	power = PM_data['0293A13R:Watts'][-1] # Retrieve latest power measurement
	return power # Return measurement

# This function uses global toggles to create a header for all variables that are being used
def build_header(CJCON, TCON, TC_num, PyrON, ComAccelON, LTON, PMON):
	
	header = 'Time'
	
	# Add TCs to header if using
	if TCON == 1:
		for i in range(0, TC_num):
			header = header + sep + 'Temp' + str(i+1)
		for i in range(0, TC_num):
			header = header + sep + 'TCV' + str(i+1)
			
	# Add Cold Junction Sensor to header if using
	if CJCON == 1:
		header = header + sep + 'CJCT' + sep + 'CJCV'

	# Add pyrheliometer to header if using
	if PyrON == 1:
		header = header + ',PyrO,PyrE'

	# Add Compass and Accelerometer variables to header if using
	if ComAccelON == 1:
		header = header + ',Mag X,Mag Y,Mag Z,Accel X,Accel Y,Accel Z,Elevation,Azimuth,El Ave,Az Ave,El True,Az True'

	# Add Light Tower readings to header if using
	if LTON == 1:
		header = header + ',LT direct,LT NS,LT EW'

	# Add power meter to the header if using
	if PMON == 1:
		header = header + ',Power'

	header = header # Not sure if this is necessary ????????????????

	return header

# This function reads all requested instruments outputs their values to an output string
# It depends on global variables
def collect_data(handle, CJCON, CJCAIN, TCON, TC_num, TC_AIN_start, TC_AIN_vec, PyrON, Pyr_AIN, ComAccelON, LTON, AIN_D, AIN_NS, AIN_EW, PMON, PM_fpath):
	# Initiate output string with the first column as a timestamp
	outstr =  datetime.now().strftime('%H:%M:%S.%f')
	
	# Read TCs and include in outstr
	if TCON == 1:
		[Temps, TCVs] = read_LJ_TC(handle, TC_num, TC_AIN_start, TC_AIN_vec, CJCON, CJCAIN)
		outstr = outstr + sep + sep.join(map(str, Temps)) # Temperatures
		outstr = outstr + sep + sep.join(map(str, TCVs)) # Voltage readings
	
	# Read Cread Cold Junction Sensor and output to outstr
	if CJCON == 1:
		CJCT, CJCV = read_LJ_CJC(handle, TC_AIN_start) 
		outstr = outstr + sep + str(CJCT) + sep + str(CJCV)
	
	# Read Pyrheliometer and output to outstr
	if PyrON == 1:
		[PO, PE] = read_LJ_Pyr(handle, Pyr_AIN)
		outstr = outstr + sep + str(PO) + sep + str(PE)
	
	# Read Compass and Accelerometer and output to outstr
	if ComAccelON == 1:
		[mX, mY, mZ, aX, aY, aZ] = read_LJ_CA(handle)
		[el, azim, aveel, aveaz, az_True, el_True] = solar_angs(handle)
		outstr = outstr + sep + str(mX) + sep + str(mY) + sep + str(mZ) + sep + str(aX) + sep + str(aY) + sep + str(aZ)

		
		outstr = outstr + sep + str(el) + sep + str(azim) + sep + str(aveel) + sep + str(aveaz) + sep + str(el_True)  + sep + str(az_True)
		# outstr = outstr + sep + str(el) + sep + str(el_True) + sep + str(azim) + sep + str(az_True)
		
	# Read Light Tower and output to outstr
	if LTON == 1:
		[LT_direct, LT_NS, LT_EW] = read_LJ_LT(handle, AIN_D, AIN_NS, AIN_EW)
		outstr = outstr + sep + str(LT_direct) + sep + str(LT_NS) + sep + str(LT_EW)
	
	# Read Power Meter and output to outstr
	if PMON == 1:
		Power = read_PM(PM_fpath)
		outstr = outstr + sep + str(Power)
	
	outstr = outstr + '\n' # New line at end of output string
	return outstr

########################################
# Tracker function

def Track(handle, AIN_NS, LT_moveN, LT_stopN, FION, LT_moveS, LT_stopS, FIOS, AIN_EW, LT_moveW, LT_stopW, FIOW, LT_moveE, LT_stopE, FIOE):
	
	# Try moving
	try:
		# Move North
		if ljm.eReadName(handle, AIN_NS) < LT_moveN:
			while ljm.eReadName(handle, AIN_NS) < LT_stopN:
				ljm.eWriteName(handle, FION,1)
				print('Moving North. LT NS: ', ljm.eReadName(handle, AIN_NS))
			ljm.eWriteName(handle, FION, 0)
		
		# Move South
		if ljm.eReadName(handle, AIN_NS) > LT_moveS:
			while ljm.eReadName(handle, AIN_NS) > LT_stopS:
				ljm.eWriteName(handle, FIOS,1)
				print('Moving South. LT NS: ', ljm.eReadName(handle, AIN_NS))
			ljm.eWriteName(handle, FIOS, 0)
		
		# Move West
		if ljm.eReadName(handle, AIN_EW) < LT_moveW:
			while ljm.eReadName(handle, AIN_EW) < LT_stopW:
				print('Moving West. LT EW: ', ljm.eReadName(handle, AIN_EW))
				ljm.eWriteName(handle, FIOW, 1)
			ljm.eWriteName(handle, FIOW, 0)
		
		# Move East
		if ljm.eReadName(handle, AIN_EW) > LT_moveE:
			while ljm.eReadName(handle, AIN_EW) > LT_stopE:
				print('Moving East. LT EW: ', ljm.eReadName(handle, AIN_EW))
				ljm.eWriteName(handle, FIOE, 1)
			ljm.eWriteName(handle, FIOE, 0)
	
	# If there's an issue, stop moving
	except:
		ljm.eWriteName(handle, FION, 0)
		ljm.eWriteName(handle, FIOS, 0)
		ljm.eWriteName(handle, FIOW, 0)
		ljm.eWriteName(handle, FIOE, 0)
		in1 = input('Would you like to continue? (y/n) \n')
		while True:
			if in1 == 'y':
				break
			elif in1 == 'n':
				exit()
			else:
				in1 = input('Invalid input. Please enter y or n. \n')

################# End of Library ###################