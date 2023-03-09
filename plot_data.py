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
from math import pi

fig1 = plt.figure()

CJCTV = 0 # Plot CJC Voltage?
TCV = 0 # Plot TC voltage?
AINON = 0 # AIN test

def animate(i, fpath, CJCON, CJCTV, TCON, TCV, TC_num, PyrOn, ComAccelON, LTON, PMON):
	
	fig1.clear()
	plt.subplots_adjust(top=0.94, bottom=0.041, left=0.078, right=0.959, hspace=0.7, wspace=0.4)
	
	PlotEff = 0
	if (PMON == 1) & (PyrOn == 1):
		PlotEff = 1
	
	
	if AINON == 1:
		TCON =0
	WinCount = CJCON + CJCTV + TCON*TC_num + 1 + TCON + TCV*TC_num + PyrOn + ComAccelON + LTON + 2*PMON + PlotEff + AINON*TC_num
	
	if WinCount < 1:
		print('Error! Nothing to Plot????')
	elif WinCount == 1:
		spx = 1
		spy = spx
	elif WinCount == 2:
		spx = 1
		spy = 2
	elif WinCount < 5:
		spx = 2
		spy = 2
	elif WinCount < 7:
		spx = 2
		spy = 3
	elif WinCount < 10:
		spx = 3
		spy = 3
	elif WinCount < 13:
		spx = 4
		spy = 3
	elif WinCount < 17:
		spx = 4
		spy = 4
	elif WinCount < 21:
		spx = 5
		spy = 4
	elif WinCount < 26:
		spx = 5
		spy = 5
	elif WinCount < 31:
		spx = 6
		spy = 5
	elif WinCount < 37:
		spx = 6
		spy = 6
	elif WinCount < 43:
		spx = 7
		spy = 6
	elif WinCount < 50:
		spx = 7
		spy = 7
	elif WinCount < 57:
		spx = 8
		spy = 7
	elif WinCount < 65:
		spx = 8
		spy = 8
	elif WinCount < 100:
		spx = 10
		spy = 10
	else:
		print('We need ', WinCount, 'windows')
		print('please write a new scenario for WinCount')
		exit()
		
	# Set plotting parameters
	rez = 1250 # Data resolution
	# spx = 2 # Number of subplots in x direction
	# spy = 3 # Number of subplots in y direction
	spx = 7
	spy = 5
	spn = 1 # Subplot number
	
	
	# Collect data
	data = pd.read_csv(fpath, header = 0, index_col='Time', parse_dates=True)	
	x = data.index.strftime('%H:%M:%S') # X-axis data formatted for time
	data = data.replace(-9999, 0)
	
	
	# For small files
	if len(data.index) < rez:
		rez = len(data.index)
	
	
	if AINON == 1:
		for j in range(0, TC_num):
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			T_data_name = 'AIN' + str(TC_AIN_vec[j])
			plt.plot(x[-rez:-1], data[T_data_name][-rez:-1])
			plt.scatter(x[-1], data[T_data_name][-1], c='r')
			ti = T_data_name + f': {data[T_data_name][-1]:.1f}' + 'V'
			plt.title(ti)
			plt.ylabel('Voltage (V)')
			plt.xticks([x[-rez], x[-1]])
			spn +=1
	
	if TCON == 1:
		for j in range(0, TC_num):
			Temp_Plot_Clrs = ['r', 'y', 'g', 'r', 'b', 'r', 'm', ]
			# if j == 0:
				# pc = Temp_Plot_Clrs[2]
			# elif j == 1:
				# pc = Temp_Plot_Clrs[1]
			# elif j ==2:
				# pc = Temp_Plot_Clrs[0]
			# else:
				# pc = Temp_Plot_Clrs[j%7]
			pc = Temp_Plot_Clrs[j%7]
			T_data_name = 'Temp' + str(j+1)
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			plt.plot(x[-rez:-1], data[T_data_name][-rez:-1], c=pc)
			# plt.scatter(x[-1], data[T_data_name][-1], c='r')
			ti ='Temp' + str(j+1) + f':{data[T_data_name][-1]:.1f}' + '$^\circ$C'
			plt.title(ti)
			plt.ylabel('Temp ($^\circ$C)')
			plt.xticks([x[-rez], x[-1]])
			spn +=1
		plt.suptitle('Data from ' + str(x[-rez]) + ' to ' + str(x[-1]))
		
		# All TCs 
		if TC_num > 1:
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			for k in range(0, TC_num):
				T_data_name = 'Temp' + str(k+1)
				plt.plot(x[-rez:-1], data[T_data_name][-rez:-1])
				# plt.plot(x, data[T_data_name])
				# dT = (data[T_data_name][-1] - data[T_data_name][-2])/(x[-1] - x[-2])
				if 0 == 1:
					dtt =(data.index[-1] - data.index[-rez])
					dtt = dtt.total_seconds()
					dTdt = (data[T_data_name][-1] - data[T_data_name][-rez])/dtt
					 
					print(T_data_name, f'{data[T_data_name][-1]:.1f}', '\u00B0C \t dT/dt', f'{dTdt*60:.1f}\u00B0C/min')
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
		
		# Thermocouple differential
		if 1 == 0:
			xxx = data.index
			# xxx = np.diff(xxx)
			xxx = xxx.to_series().diff()
			for i in range(0,len(xxx)):
				yyy = xxx[i].total_seconds()
			
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			plt.plot(x[0:-1],np.diff(data['TC2'])/yyy)
			plt.title('TC2 Differential')
			spn += 1
		
	if TCV == 1:
		for j in range(0, TC_num):
			T_data_name = 'TCV' + str(j+1)
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			plt.plot(x[-rez:-1], data[T_data_name][-rez:-1])
			plt.title('AIN' + str(TC_AIN_vec[j]))
			plt.ylabel('AIN Voltage')
			plt.xticks([x[-rez], x[-1]])
			plt.suptitle('AIN Voltages')
			spn +=1
	
	# Thermocouples
	if CJCON == 1:
		fig1.add_subplot(spy,spx,spn)
		plt.cla()
		cjcnow = data['CJCT'][-1]
		plt.plot(x[-rez:-1],data['CJCT'][-rez:-1], 'm')
		ti ='CJ Temp: ' + f'{cjcnow:.1f}' + '$^\circ$C'
		plt.title(ti)
		plt.ylabel('Temp [$^\circ$C]')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
		if (CJCTV == 1) & (TCV == 1):
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			plt.plot(x[-rez:-1],data['CJCV'][-rez:-1])
			plt.title('Cold Junction Voltage')
			plt.ylabel('Voltage')
			plt.xticks([x[-rez], x[-1]])
			spn +=1
	
	
	# Pyrheliometer
	if PyrON == 1:
		fig1.add_subplot(spy,spx,spn)
		plt.cla()
		plt.plot(x[-rez:-1],data['PyrE'][-rez:-1], 'r')
		pyrnow = data['PyrE'][-1]
		ti ='Pyrheliometer: ' + f'{pyrnow:.0f}' + ' W/m$^2$'
		plt.title(ti)
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
		if PMON == 1:
			df1 = data.nlargest(1000, ['Power']) # 100 largest values
			f2 = data['Power']> 50
			df2 = data.loc[f2]
			fig1.add_subplot(spy,spx,spn)
			plt.cla()
			plt.scatter(df1['LT EW'], df1['LT NS'], c = df1['Power'])
			# plt.scatter(df2['LT EW'], df2['LT NS'], c = df2['Power'])
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
		plt.title('Power: ' + '%0.1f' % data['Power'][-1] +' W')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
		
	if (PyrOn == 1) & (PMON == 1):
		Ac = pi*0.6**2/4
		fig1.add_subplot(spy,spx,spn)
		plt.cla()
		PowIn = data['Power'][-rez:-1]/(data['PyrE'][-rez:-1]*Ac)*100
		plt.plot(x[-rez:-1],PowIn)
		EffNow = data['Power'][-1]/(data['PyrE'][-1]*Ac)*100
		# ti = 'Power Efficiency: ' + str(EffNow)
		ti = f'Power Efficiency: {EffNow:.2f}'
		plt.title(ti)
		plt.ylabel('Efficiency [%]')
		plt.xticks([x[-rez], x[-1]])
		spn +=1
		
# Animate!
ani = FuncAnimation(plt.gcf(), animate, fargs = [fd_path, CJCON, CJCTV, TCON, TCV, TC_num, PyrON, ComAccelON, LTON, PMON], interval=100)

plt.show()