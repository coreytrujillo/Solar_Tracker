# Import libraries
from labjack import ljm # LabJack
from datetime import datetime # Date and time
import numpy as np # Numbers and math
import time # For sleep function, pef_counter
import os # For removing files
import sys # Scripting functions
import ctypes
import importlib
import pandas as pd # For data analysis
import ephem as ep # For predicting Sun's position
# import Header
# from Header import * # Global variables

# CSV separator
sep = ','

# Connect with LabJack
def find_LJ():
	# Look for LabJack
	lookforLJ = True  
	while lookforLJ:
		# Try to find LabJack
		try:
			handle = ljm.openS('T7', 'ANY', 'ANY')  # T7 device, Any connection, Any identifier
			info = ljm.getHandleInfo(handle) # LabJack Info
			print('Connected to LabJack')
			return(handle, info)
			ljm.closeAll
			lookforLJ = False
			
		# If LabJack isn't found
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
		
		# If file can't initiate
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
def append_data_file(fpath, outstr):
	f = open(fpath, 'a') # Open file
	f.write(outstr) # Append outstring to file
	f.close() # Close file

# Read Thermocouples from LabJack
def read_LJ_TC(handle, TC_num, TC_AIN_start):
	# Initiate variables
	ain_n = [] # Initiate vector for AIN's connected to TC's
	ain_idx = [] # Initiate vector for TC type
	ain_cnfg = [] # Initiate vector for Temperature scale
	ain_rd =[] # Initiate vector of variable to read temps
	
	# Create variables for thermocuple settings and measurement
	for i in range(TC_AIN_start,TC_AIN_start+TC_num):
		ain_n.append('AIN' + str(i)) # AIN numbers on Labjack
		ain_idx.append(ain_n[i] + '_EF_INDEX') # Thermocouple type: 22 for K
		ain_cnfg.append(ain_n[i] + '_EF_CONFIG_A') # Temperature scale configuration: 0 for K, 1 for C, 2 for F
		ain_rd.append(ain_n[i] + '_EF_READ_A') # Reader variable
	
	# Indentify TC settings for LabJack
	v_idx = 22*np.ones((TC_num,1),float) # Identify type K thermocouple
	v_cnfg = np.ones((TC_num,1),float) # Set thermocouple to read in Celcius
	
	# Comminicate settings to LabJack
	ljm.eWriteNames(handle, TC_num, ain_idx, v_idx) # Tell LabJack which AINs are Type K Thermocouples
	ljm.eWriteNames(handle, TC_num, ain_cnfg, v_cnfg) # Tell LabJack temperature scale
	
	# Read temperature values from LabJack
	Temps = ljm.eReadNames(handle, TC_num, ain_rd)
	
	# Output Temperatures
	return Temps

# Read Pyrheliometer Voltage from LabJack
def read_LJ_Pyr(handle, AIN):
	# handle = LabJack handle
	# AIN is Pyrheliometer AIN
	
	s = 7.85e-6 # Radiometer sensitivity [V/W/m2]
	Pyr_O = ljm.eReadName(handle, AIN) # Pyrheliometer output in Volts
	Pyr_E = Pyr_O/s # Calculated Solar irradiance [W/m2]
	
	# Output values
	return Pyr_O, Pyr_E

# Run a Lua Script (for compass and accelerometer readings)
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

# Normalize magnetometer readings to outupt between -1 and 1
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


# Read Compass and Acceleromter
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

# Average Compass and accelerometer values to reduce noise
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


# Calculate elevation angle
def el_ang(up, face):
	# up = up vector
	# face = vector that defines plane of the face of the collectors
	
	# Calculate elevation angle
	p1 = np.dot(up,face)*face # Vector projection on plane vector
	p2 = up - p1 # Vector projection on plane
	el = np.arccos(np.dot(p2,up)/(np.linalg.norm(p2)*np.linalg.norm(up)))*180/np.pi # Elevation angle
	
	return el

# Calculate azimuthal Angle
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
	
	if 1 == 1:
		print('Direct: ', LT_direct)
		print('NS: ', LT_NS)
		print('EW: ', LT_EW)
	
	return LT_direct, LT_NS, LT_EW

# Check that power meter is writing to file
def check_PM(PM_fpath):
	# PM_fpath = file path for power meter data
	
	lookPM = True # look for power meter?
	
	while lookPM:
		
		try:
			# Look at file
			PMf = open(PM_fpath, 'r') # Open file
			numlines = len(PMf.readlines()) # Get the number of lines
			PMf.close()  # close file
			
			if numlines >3: 
				print('Reading Power Meter data!')
				print(numlines)
				lookPM = False
				
			else: # If the file is not collecting data
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
		
		# If there is an error reading the PM file
		except Exception as e:
			print('Power Meter Error:', e)
			while True:
				PM_response = input('Would you like to try again? (y/n) \n')
				if PM_response == 'y':
					break
				elif PM_response == 'n':
					sys.exit()
					print('Exiting program')
					lookPM = False
				else:
					print('Invalid response. Please enter y for yes or n for no\n')

# Read Power Meter data from file
def read_PM(PM_fpath):
	PM_data = pd.read_csv(PM_fpath, header = 2, index_col = 'Timestamp') # read power file
	power = PM_data['0293A13R:Watts'][-1] # Retrieve latest power measurement
	return power

# Build header for data file
# This function depends on global variables
def build_header(TCON, TC_num, PyrON, ComAccelON, LTON, PMON):
	
	header = 'Time'
	if TCON == 1:
		for i in range(0,TC_num):
			header = header + sep + 'TC' + str(i+1)

	if PyrON == 1:
		header = header + ',PyrO,PyrE'

	if ComAccelON == 1:
		# header = header + ',Mag X,Mag Y,Mag Z,Accel X,Accel Y,Accel Z,Elevation,El True,Azimuth,Az True'
		header = header + ',Mag X,Mag Y,Mag Z,Accel X,Accel Y,Accel Z,Elevation,Azimuth,El Ave,Az Ave,El True,Az True'

	if LTON == 1:
		header = header + ',LT direct,LT NS,LT EW'

	if PMON == 1:
		header = header + ',Power'

	header = header
	return header

# This function reads all requested instruments outputs their values to an output string
# It depends on global variables
def collect_data(handle, TCON, TC_num, TC_AIN_start, PyrON, Pyr_AIN, ComAccelON, LTON, AIN_D, AIN_NS, AIN_EW, PMON, PM_fpath):
	# Initiate output string
	outstr =  datetime.now().strftime('%H:%M:%S.%f')
	
	# Read TCs
	if TCON == 1:
		Temps = read_LJ_TC(handle, TC_num, TC_AIN_start)
		outstr = outstr + sep + sep.join(map(str, Temps))
	
	# Read Pyrheliometer
	if PyrON == 1:
		[PO, PE] = read_LJ_Pyr(handle, Pyr_AIN)
		outstr = outstr + sep + str(PO) + sep + str(PE)
	
	# Read Compass and Accelerometer
	if ComAccelON == 1:
		[mX, mY, mZ, aX, aY, aZ] = read_LJ_CA(handle)
		[el, azim, aveel, aveaz, az_True, el_True] = solar_angs(handle)
		outstr = outstr + sep + str(mX) + sep + str(mY) + sep + str(mZ) + sep + str(aX) + sep + str(aY) + sep + str(aZ)

		
		outstr = outstr + sep + str(el) + sep + str(azim) + sep + str(aveel) + sep + str(aveaz) + sep + str(el_True)  + sep + str(az_True)
		# outstr = outstr + sep + str(el) + sep + str(el_True) + sep + str(azim) + sep + str(az_True)
		
	# Read Light Tower
	if LTON == 1:
		[LT_direct, LT_NS, LT_EW] = read_LJ_LT(handle, AIN_D, AIN_NS, AIN_EW)
		outstr = outstr + sep + str(LT_direct) + sep + str(LT_NS) + sep + str(LT_EW)
	
	# Read Power Meter
	if PMON == 1:
		Power = read_PM(PM_fpath)
		outstr = outstr + sep + str(Power)
	
	outstr = outstr + '\n' # New line at end of output string
	return outstr

########################################
# Tracker function

# def Track(handle):
def Track(handle, AIN_NS, LT_moveN, LT_stopN, FION, LT_moveS, LT_stopS, FIOS, AIN_EW, LT_moveW, LT_stopW, FIOW, LT_moveE, LT_stopE, FIOE):
	# Move North
	try:
		if ljm.eReadName(handle, AIN_NS) < LT_moveN:
			while ljm.eReadName(handle, AIN_NS) < LT_stopN:
				ljm.eWriteName(handle, FION,1)
				print('Move North. LT NS: ', ljm.eReadName(handle, AIN_NS))
			ljm.eWriteName(handle, FION, 0)
		
		# Move South
		if ljm.eReadName(handle, AIN_NS) > LT_moveS:
			while ljm.eReadName(handle, AIN_NS) > LT_stopS:
				ljm.eWriteName(handle, FIOS,1)
				print('Move South. LT NS: ', ljm.eReadName(handle, AIN_NS))
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