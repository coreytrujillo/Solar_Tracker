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
	
	fig1.clear()

	# Set plotting parameters
	rez = 100 # Data resolution
	spx = 1 # Number of subplots in x direction
	spy = 3 # Number of subplots in y direction
	spn = 1 # Subplot number
	
	
	# Collect data
	data = pd.read_csv(fpath, header = 0, index_col='Time', parse_dates=True)	
	x = data.index.strftime('%H:%M:%S') # X-axis data formatted for time
	
	
	# For small files
	if len(data.index) < rez:
		rez = len(data.index)
	
	# Thermocouples
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
		
		# All TCs 
		if 1 == 1:
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			for k in range(0, TC_num):
				T_data_name = 'TC' + str(k+1)
				plt.plot(x[-rez:-1], data[T_data_name][-rez:-1])
				# dT = (data[T_data_name][-1] - data[T_data_name][-2])/(x[-1] - x[-2])
				dt =(data.index[-1] - data.index[-100])
				dt = dt.total_seconds()
				dTdt = (data[T_data_name][-1] - data[T_data_name][-100])/dt
				
				print(T_data_name, data[T_data_name][-1], '\t dT/dt', dTdt)
			print('--------------------------')
			plt.title('All Thermocouples')
			plt.ylabel('Temp ($^\circ$C)')
			plt.xticks([x[-rez], x[-1]])
			
			# plt.legend(np.array2string(np.arange(TC_num), separator = ','))
			# plt.legend(map(str, TC_num))))
			ss = ''
			aaa = ss.join(map(str, np.arange(TC_num)+1))
			plt.legend(aaa, loc=2)
			spn += 1
	
	# Pyrheliometer
	if PyrON == 1:
		fig1.add_subplot(spy,spx,spn)
		plt.cla()
		plt.plot(x[-rez:-1],-data['PyrE'][-rez:-1])
		plt.title('Pyrheliometer Reading')
		plt.ylabel('Power (W/m$^2$)')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
	
	# Compass/Accelerometer
	if ComAccelON == 1:
		
		# Raw mag and accel data
		if 1 == 1:
			
			# Magnetometer
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
			plt.legend(['X','Y','Z'])
			plt.ylabel('Magnetic Reading')
			plt.title('Magnetometer Reading')
			plt.xticks([x[-rez], x[-1]])
			spn +=1
			
			# Accelerometer
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
		
		# Azimuth
		fig1.add_subplot(spy, spx, spn)
		plt.cla()
		plt.plot(x[-rez:-1],data['Azimuth'][-rez:-1])
		plt.plot(x[-rez:-1],data['Az Ave'][-rez:-1])
		plt.plot(x[-rez:-1],data['Az True'][-rez:-1])
		plt.legend(['Azim','az ave','Az T'])
		plt.ylabel('Azimuth Angle')
		plt.title('Azimuth')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
		
		# Elevation 
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
	
	# Light tower
	if LTON == 1:
	
		# Plot Direct, NS, EW Voltages
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
		
		# Heat Map!!!!!!!!! To debug optimal values, plot voltages on a power heat map. 
		if (LT_debug == 1) & (PMON == 1):
			df1 = data.nlargest(1000, ['Power']) # 100 largest values
			f2 = data['Power']> 50
			df2 = data.loc[f2]
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			# plt.scatter(df1['LT EW'], df1['LT NS'], c = df1['Power'])
			plt.scatter(df2['LT EW'], df2['LT NS'], c = df2['Power'])
			# plt.scatter(data['LT EW'][-rez:-1], data['LT NS'][-rez:-1], c = data['Power'][-rez:-1])
			# plt.scatter(data['LT EW'], data['LT NS'], c = data['Power'])
			cb = plt.colorbar()
			
			plt.scatter(data['LT EW'][-1], data['LT NS'][-1], color = 'r')
			plt.xlabel('LT EW')
			plt.ylabel('LT NS')
			plt.title('Light Tower Power Heat Map')
			spn +=1
	
	# Power Meter
	if PMON == 1:
		fig1.add_subplot(spy,spx,spn)
		plt.cla()
		plt.plot(x[-rez:-1],data['Power'][-rez:-1])
		plt.ylabel('Power Meter')
		plt.title('Power [W]')
		plt.xticks([x[-rez], x[-1]])
		spn +=1

# Animate!
ani = FuncAnimation(plt.gcf(), animate, fargs = [fd_path, TCON, TC_num, PyrON, ComAccelON, LTON, PMON], interval=100)
plt.show()