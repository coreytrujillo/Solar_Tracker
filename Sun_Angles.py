import ephem as ep
import matplotlib.pyplot as plt
import datetime as dt
from math import pi

# Calculate relevant angles and times for a day
def daily_sun_angles(andate, lablat, lablon, labelev, minel):
	# andate = date for analysis
	# lablat = location latitude
	# lablon = longitude of location
	# labelev = elevation of location in meters
	# minel = minimum angle for operating collectors

	lab = ep.Observer() # Observing from lab
	sun = ep.Sun() # Observing sun
	lab.date = andate.strftime('%Y/%m/%d') # Date of observation
	lab.lat = str(lablat) # Latitude of lab 
	lab.lon = str(lablon) # Longitude of lab
	lab.elevation = labelev # Lab elevation (m above sea level)
	lab.horizon = str(minel) # Minimum elevation angle for collectors
	
	SNutc = lab.next_transit(sun) # Solar noon UTC
	SNloc = ep.localtime(SNutc) # Solar noon local time
	SNel = sun.alt # Elevation angle at solar noon
	SNaz = sun.az # Azimuth angle at solar noon 
	
	# If solar noon is less than minimum collector operation angle
	if SNel >= lab.horizon:
		rUTC = lab.next_rising(sun) # Time sun rises above min collector angle UTC
		raz = sun.az*180/pi
		rloc = ep.localtime(rUTC) # Time sun rises above min collector angle MT
		sUTC = lab.next_setting(sun) # Time sun falls below min angle UTC
		sloc = ep.localtime(sUTC) # Time sun falls below min angle MT
	
	# If sun never rises above operable angle
	else:
		rUTC = 0
		rloc = rUTC
		sUTC = rUTC
		sloc = rUTC
		raz = rUTC
		
	return SNloc, SNel, rloc, raz, sloc

# Location and operation setup
lablat = 39.781763 # lab latitude
lablon = -104.910462 # lab longitude
labelev = 1610 # lab elevation (m)
minel = 27 # Minimum elevation angle for collectors to operate
d0 = dt.datetime.now() # Start date (today)
RunHours = 2 #dt.timedelta(hours=2) # Minimum number of hours for operating collectors

# Today's data
[SNloc, SNel, rloc, raz, sloc] = daily_sun_angles(d0, lablat, lablon, labelev, minel)
print('----------------------------')
print('-----------TODAY------------')
print('----------------------------')
print('Today the sun will rise above', minel, 'degrees elevation at', rloc, '\n at that time the azimuth angle will be ', raz, '\n The sun will set below', minel, 'degrees elevation at', sloc)

# Tomorrow's data
d1 = d0 + dt.timedelta(days=1)
[SNloc1, SNel1, rloc1, raz1, sloc1] = daily_sun_angles(d1, lablat, lablon, labelev, minel)
print('----------------------------')
print('----------TOMORROW----------')
print('----------------------------')
print('Today the sun will rise above', minel, 'degrees elevation at', rloc1, '\n at that time the azimuth angle will be ', raz1, '\n The sun will set below', minel, 'degrees elevation at', sloc1)


# Initiate vectors
OTV = [] # Operable time vector
dv = [] # Date vector
sr = [] # Time Sun rises above min operable elevation angle
ss = [] # Time Sun sets below min operable elevation angle
bo = [] # blackout
razv = []


for i in range(0,200):
	# Calculate angles and times for day i
	[SNloc, SNel, rloc, raz, sloc] = daily_sun_angles(d0, lablat, lablon, labelev, minel)
	
	# Operable time
	OT = sloc-rloc 
	
	# Mindight today
	MN = dt.datetime.combine(d0, dt.datetime.min.time()) 
	
	# If there is operable time
	if OT!=0:
		OT = OT.total_seconds()/3600 # Calculate Operable Time in hours
		
		# Calculate operable time start hour (Sunrise)
		sunrise = rloc - MN 
		sunrise = sunrise.total_seconds()/3600
		
		# Calculate operable time Stop hour hour (Sunset)
		sunset = sloc - MN 
		sunset = sunset.total_seconds()/3600
		
	# If no operable time
	else:
		sunrise = None
		sunset = None
		raz = None
	
	# If operable time is less than desired hours, catagorize date as blackout	
	if OT < RunHours:
		bo.append(d0)

	# Append data to vectors
	OTV.append(OT)
	dv.append(d0)
	sr.append(sunrise)
	ss.append(sunset)
	razv.append(raz)
	
	# Iterate day
	d0 = d0 + dt.timedelta(days=1)

# Print Blackout Information 
print('----------------------------')
print('---------BLACKOUT-----------')
print('----------------------------')
if not bo:
	print('No blackout dates for ', RunHours,' hours run time at', minel, ' degrees')
else:
	print('The Sun is up more than', minel, 'degrees elevation \n for less than ', RunHours, ' hours \n starting on:', bo[0], '\n and ending on:' , bo[-1])

####################################
# Plotting 
####################################
# Hours sun is above requred Elevation Angle
plt.figure()
plt.subplot(221)
titlestr = 'Number of hours Sun is above ' + str(minel) + ' degrees elevation'
plt.title(titlestr)
plt.plot(dv, OTV)

# Sunrise/sunset times
plt.subplot(122)
titlestr2 = 'Hour of day sun rises or sets above/below ' + str(minel) + ' degrees elevation'
plt.title(titlestr)
plt.title('Hour of day sun rises/sets above/below collector operation angle')
plt.plot(dv,sr)
plt.plot(dv,ss)
plt.xlabel('Date')
plt.ylabel('Hour of day')
plt.legend(['Sunrise', 'Sunset'])

# Azimuth angle at sunrise
plt.subplot(223)
plt.title('Azimuth angle when sun is high enough for operation')
plt.plot(dv,razv)


plt.show()