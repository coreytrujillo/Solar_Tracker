import ephem as ep
import time
from math import pi

lab = ep.Observer()
lablat = 39.781763
lablon = -104.910462
lab.lat = str(lablat)
lab.lon = str(lablon)
lab.elevation = 1610

# Optimal light tower values (V)
LTNS_opt = 310
LTEW_opt = 90

# Light Tower variances and boundaries
LTNS_var_N = 40
LTNS_var_S = LTNS_var_N
LTEW_var_E = 10
LTEW_var_W = LTEW_var_E
LTNS_backstop = 5
LTEW_backstop = 2

# Light Tower move and stop values
move_N = LTNS_opt - LTNS_var_S
move_S = LTNS_opt + LTNS_var_N
move_E = LTEW_opt + LTEW_var_W
move_W = LTEW_opt - LTEW_var_E
stop_N = move_S - LTNS_backstop
stop_S = move_N + LTNS_backstop
stop_E = move_W + LTEW_backstop
stop_W = move_E - LTEW_backstop

# FIO Relay Controls
FIO_N = 2
FIO_S = 3
FIO_E = 4
FIO_S = 5

# Azimuth and Elevation Angle variances
az_var_lo = 10
az_var_hi = 10
el_var_lo = 5
el_var_hi = 5

# Az and El move and stop values


# while True:
if 1==1:
	# True azimuth and elevation angles
	Ang = ep.Sun(lab)
	az_True = float(Ang.az) * 180/ pi
	el_True = float(Ang.alt) *  180/ pi
	print('az, el')
	print(az_True, el_True)
	
	# Upper and lower boundaries
	az_lo = az_True - az_var_lo
	az_hi = az_True + az_var_hi
	el_lo = el_True - el_var_lo
	el_hi = el_True + el_var_hi
	print('az_lo, az_hi, el_lo, el_hi')
	print(az_lo, az_hi, el_lo, el_hi)
	print('LTNS_lo, LTNS_hi, LTEW_lo, LTEW_hi')
	print(LTNS_lo, LTNS_hi, LTEW_lo, LTEW_hi)
	
	# Measured azimuth and elevation angles
	az_meas = 263 # !!!!!!!!!!!! Include measurement here
	el_meas = 35 # !!!!!!!!!!!!!!!!!! Include measurement here
	
	# Read light tower
	LTNS = 300 # !!!!!!!!!!!! Include measurement here
	LTEW = 90 # !!!!!!!!!!!! Include measurement here
	
	# Motion E/W
	if az_meas > az_lo and az_meas < az_hi: # If az is within expected range
		if LTEW < LTEW_lo: # Adjust west based on light tower reading
			print('Move West')
			move(handle, AIN_LT_EW, stop_W, FIO_W)
		elif LTEW > LTEW_hi: # Adjust east based on light tower reading
			move(handle, AIN_LT_EW, stop_E, FIO_E)
			print('Move East')
	elif az_meas < az_lo: # if az is lower than expected
		print('Out of range! Move West')
	elif az_meas > az_hi: # if az is higher than expected
		print('Out of range! Move East')
	
	
	# Motion N/S
	if el_meas > el_lo and el_meas < el_hi: # if el is within expectations
		if LTNS < LTNS_lo:
			move(handle, AIN_LT_NS, stop_N, FIO_N)
			print('Move North')
		elif LTNS > LTNS_hi:
			move(handle, AIN_LT_NS, stop_S, FIO_S)
			print('Move South')
	elif el_meas < el_lo:
		print('Out of range! Move North')
	elif el_meas > el_hi:
		print('Out of range! Move South')
	
	# time.sleep(5)


def move(handle, LT_AIN, stop, FIO):
	while ljm.eReadName(handle, LT_AIN) < stop:
		ljm.eReadName(handle, FIO)