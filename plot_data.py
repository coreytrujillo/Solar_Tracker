import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np
import datetime
import warnings
warnings.filterwarnings("ignore")
import importlib
import Header
from Header import *

fig1 = plt.figure()

def animate(i, fpath, TCON, TC_num, PyrOn, ComAccelON, LTON, PMON):
	# importlib.reload(Header)
	# from Header import *
	# Import data
	data = pd.read_csv(fpath, header = 0, index_col='Time', parse_dates=True)
	
	# Set plotting parameters
	rez = 1000# Data resolution
	if len(data.index) < rez:
		rez = len(data.index)
	spx = 2 # Number of subplots in x direction
	spy = 2 # Number of subplots in y direction
	spn = 1 # Subplot number

	x = data.index.strftime('%H:%M:%S') # X-axis data formatted for time
	
	if TCON == 1:
		for j in range(0, TC_num):
			T_data_name = 'TC' + str(j+1)
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			plt.plot(x[-rez:-1], data[T_data_name][-rez:-1])
			plt.title('Thermocouple ' + str(j+1))
			plt.ylabel('Temp ($^\circ$C)')
			plt.xticks([x[-rez], x[-1]])
			spn +=1
			
	if PyrON == 1:
		fig1.add_subplot(spy,spx,spn)
		plt.cla()
		plt.plot(x[-rez:-1],data['PyrE'][-rez:-1])
		plt.title('Pyrheliometer Reading')
		plt.ylabel('Power (W/m$^2$)')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
		
	if ComAccelON == 1:
		
		if 1 == 0:
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			plt.plot(x[-rez:-1],data['Mag X'][-rez:-1])
			plt.plot(x[-rez:-1],data['Mag Y'][-rez:-1])
			plt.plot(x[-rez:-1],data['Mag Z'][-rez:-1])
			mxmax = max(data['Mag X'])
			mymax = max(data['Mag Y'])
			mzmax = max(data['Mag Z'])
			mxmin = min(data['Mag X'])
			mymin = min(data['Mag Y'])
			mzmin = min(data['Mag Z'])
			# print('X: [', mxmin, mxmax, ']')
			# print('Y: [', mymin, mymax, ']')
			# print('Z: [', mzmin, mzmax, ']')
			plt.legend(['X','Y','Z'])
			plt.ylabel('Magnetic Reading')
			plt.title('Magnetometer Reading')
			plt.xticks([x[-rez], x[-1]])
			spn +=1
		
			
			fig1.add_subplot(spy, spx, spn)
			plt.cla()
			plt.plot(x[-rez:-1],data['Accel X'][-rez:-1])
			plt.plot(x[-rez:-1],data['Accel Y'][-rez:-1])
			plt.plot(x[-rez:-1],data['Accel Z'][-rez:-1])
			plt.legend(['X','Y','Z'])
			plt.ylabel('Acceleration Reading')
			plt.title('Accelerometer Reading')
			plt.xticks([x[-rez], x[-1]])
			spn +=1
		
		fig1.add_subplot(spy, spx, spn)
		plt.cla()
		
		plt.plot(x[-rez:-1],data['Azimuth'][-rez:-1])
		plt.plot(x[-rez:-1],data['Az Ave'][-rez:-1])
		# plt.plot(x[-rez:-1],data['Az True'][-rez:-1])
		plt.legend(['Azim','az ave','Az T'])
		plt.ylabel('Azimuth Angle')
		plt.title('Azimuth')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
		
		fig1.add_subplot(spy, spx, spn)
		plt.cla()
		plt.plot(x[-rez:-1],data['Elevation'][-rez:-1])
		plt.plot(x[-rez:-1],data['El Ave'][-rez:-1])
		plt.plot(x[-rez:-1],data['El True'][-rez:-1])
		plt.legend(['El', 'El ave', 'El t'])
		plt.ylabel('Elevation Angle')
		plt.title('Elevation')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
		
	if LTON == 1:
		fig1.add_subplot(spy,spx,spn)
		plt.cla()
		plt.plot(x[-rez:-1],data['LT direct'][-rez:-1])
		plt.plot(x[-rez:-1],data['LT NS'][-rez:-1])
		plt.plot(x[-rez:-1],data['LT EW'][-rez:-1])
		plt.legend(['Direct','NS','EW'])
		plt.ylabel('Light Tower')
		plt.title('Light Volgage Reading')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
		
		fig1.add_subplot(spy,spx,spn)
		plt.cla()
		# plt.plot(x[-rez:-1],data['LT direct'][-rez:-1])
		# plt.plot(x[-rez:-1],data['LT NS'][-rez:-1])
		plt.plot(x[-rez:-1],data['LT EW'][-rez:-1])
		plt.legend(['Direct','NS','EW'])
		plt.ylabel('Light Tower')
		plt.title('Light Volgage Reading')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
		
		if 1 == 1:
			df1 = data.nlargest(100, ['Power']) 
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			plt.scatter(df1['LT EW'], df1['LT NS'], c = df1['Power'])
			plt.xlabel('LT EW')
			plt.ylabel('LT NS')
			plt.title('Light Tower Power Heat Map')
			plt.colorbar()
			
			spn +=1
		
	if PMON == 1:
		fig1.add_subplot(spy,spx,spn)
		plt.cla()
		plt.plot(x[-rez:-1],data['Power'][-rez:-1])
		plt.ylabel('Power Meter')
		plt.title('Power [W]')
		plt.xticks([x[-rez], x[-1]])
		spn +=1

# fpath = './210507_test/210510_Tracker_Calibration_data.csv'
# TCON = 0
# TC_num = 4
# PyrON = 1
# ComAccelON = 0
# LTON = 1
# PMON = 0

ani = FuncAnimation(plt.gcf(), animate, fargs = [fd_path, TCON, TC_num, PyrON, ComAccelON, LTON, PMON], interval=50)
plt.show()