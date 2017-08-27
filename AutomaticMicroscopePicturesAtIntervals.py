# Author: Quentin Delepine
# Purpose: Takes pictures on the microscope at regular user set time intervals
# Also records times of each image for records

# imports
import autopy	# controls mouse and keyboard
import time 	# controls wait time
import shutil	# can delete files
import datetime # controls date

# functions
def alert(msg,title): # Displays an alert message to control the program
    return autopy.alert.alert(msg,title,"Yes","Cancel")

def set_mouse(x,y): # Helper function
	autopy.mouse.move(x,y)

def click(): # left click in place
	autopy.mouse.click(autopy.mouse.LEFT_BUTTON)

def left_click(x,y): # move to location, then left click
	set_mouse(x,y)
	click()

def get_pos(): # used to determine coordinates. Returns mouse position
	return autopy.mouse.get_pos()

def get_time(): # returns time and date formatted for a note
	time = datetime.datetime.now()
	return time.strftime('%I:%M %p, %b %d, %Y')

def get_date(): # returns date for log file name
	time = datetime.datetime.now()
	return time.strftime('%b %d, %Y')

def get_month(): # returns month for img file names
	time = datetime.datetime.now()
	return time.month

def get_day(): # returns day for img file names
	time = datetime.datetime.now()
	return time.day

def get_nextTime(t): # calculates next img time
	time = datetime.datetime.now()
	if t < subset:
		next = time + datetime.timedelta(minutes=interval1)
	else:
		next = time + datetime.timedelta(minutes=interval2)
	return next.strftime('%I:%M %p')

def light(setting): # single function toggles microsoft light on and off
	if setting == 'on':
		left_click(xon,yon)
	elif setting == 'off':
		left_click(xoff,yoff)

def save(name): # Closes and saves the file
	# The save part takes 8s (as zvi, 10s as jpg).
	# This wait is the amount of time it needs to take the picture (ie more for mosaics)
	time.sleep(52) # This needs to be adjusted with the wait below to ensure regular pictures.

	left_click(xclose,yclose) # Click [x] button
	time.sleep(1)
	autopy.key.toggle(autopy.key.K_RETURN, True) # yes, save before closing
	time.sleep(1)
	autopy.key.type_string(name, 0) # types file name
	time.sleep(1)
	autopy.key.toggle('	',True) # tab
	time.sleep(1)
	# This section determines the file save type.
	# Scrolling all the way down is for jpg. Nothing should be zvi by default
	# autopy.key.toggle(autopy.key.K_DOWN,True)
	# time.sleep(.5)
	# autopy.key.toggle(autopy.key.K_DOWN,True)
	# time.sleep(.5)
	# autopy.key.toggle(autopy.key.K_DOWN,True)
	# time.sleep(.5)
	# autopy.key.toggle(autopy.key.K_DOWN,True)
	# time.sleep(.5)
	# --------
	autopy.key.toggle(autopy.key.K_RETURN,True)
	time.sleep(1)
	autopy.key.toggle('	',True) # tab
	time.sleep(1)
	autopy.key.toggle(autopy.key.K_RETURN,True) # enter (save)
	time.sleep(1)
	autopy.key.toggle(autopy.key.K_RETURN,True) # enter (overwrite existing file, just in case)
	time.sleep(1)
	# shutil.rmtree(date + "/" + name + ".jpg_Files") # for mosaic, delete individual file folder

def start_Time(): # Delays the start time until designated
	start = datetime.datetime(Syear,Smonth,Sday,Shour,Smins)
	now   = datetime.datetime.now().replace(microsecond=0)
	delay = start - now
	print 'Starting at ' + start.strftime('%I:%M %p, %b %d, %Y') + ". In " + str(delay.seconds) +" seconds."
	time.sleep(delay.seconds)

# This section gives an alert before starting the program. 'enter' will start the program
# Cancel will allow you to determine button coordinates. Follow instructions.
if alert("Start Program?","Automated Microscope Pictures") == False:
	alert("Move your mouse to the start button location. Press enter.","Automated Microscope Pictures")
	print "Start Button"
	print get_pos() # Returns start button coordinates [x,y]
	alert("Move your mouse to the light on button location. Press enter.","Automated Microscope Pictures")
	print "On Button"
	print get_pos() # Returns light on button coordinates [x,y]
	alert("Move your mouse to the light on button location. Press enter.","Automated Microscope Pictures")
	print "Off Button"
	print get_pos() # Returns light off button coordinates [x,y]
	alert("Move your mouse to the close button location. Press enter.","Automated Microscope Pictures")
	print "Close Button"
	print get_pos() # Returns close button coordinates [x,y]
	print "Enter these coordinates into the program"
	exit() 			# ends the program

# You can determine these coordinates by running the program and
# at the first alert prompt, press cancel. Follow the prompt instructions.
# Terminal will print the resulting coordinates
# Put the terminal coordinates as the first number.
# Leave the second number as is; it is an offset and shouldn't need adjusting.
xstart = 217   # start button x-coordinate
ystart = 1027  # start button y-coordinate
xclose = 1904  # close [x] button x-coordinate
yclose = 150   # close [x] button y-coordinate
xon    = 1012  # microscope light on button x-coordinate
yon    = 73    # microscope light on button y-coordinate
xoff   = 1048  # microscope light off button x-coordinate
yoff   = 71    # microscope light off button y-coordinate

# This section is needed if you want the program to start at a certain time.
# Ie: start program at 7:30 pm, August 30, 2016
# This is also useful if the program stopped in the middle and needs to be restarted at the proper time
# To turn on/off this functionality, you need to uncomment/comment the start_Time() function call below. (right above the loop)
Syear  = 2016 	# Start Year
Smonth = 8 		# Start Month
Sday   = 30 	# Start Day
Shour  = 19		# Start Hour (use 24 hour time)
Smins  = 30 	# Start Minute

month  = get_month() 	# Used to date pictures
day    = get_day() 	 	# Used to date pictures

t = 0 # starting time (normally zero unless starts in middle of test)
numSamples = 35 # the total number of pictures (dictates length of program)

# Take a sample every _interval1_ minutes for the first _subset_ minutes
# Then take a sample every _interval2_ minutes after
# This can be expanded to have more intervals/subsets
interval1  =  5 # in minutes
interval2  = 30 # in minutes
subset     = 60 # multiple of -interval1- #in minutes

sampleName = "Perfusion " + get_date()		# This is the name of the log file. Date as mth d, y
fileName   =  sampleName  + ".txt" 			# Creates the log file name
date  = str(month) + "-" + str(day) + "-16"	# Formats the date for naming files

notes = open(fileName, "w") 								# opens a new txt log file
notes.write ('10% PEG 10% GelMA | ' + date + ' |'+"\n" ) 	# This is the first line of the log file; like a header

print 'Taking ' + str(numSamples) + ' pictures total. ' 					# info printed to terminal
print 'Estimated duration: ' + str( (numSamples-13)/2 + 1 ) + ' hours. '	# Time calculation different for different intervals.
print 'Ctrl+C to end program early. '										# info printed to terminal

# start_Time() # uncomment this line to start the program at a certain time.

# Below is actual loop that is iterated
for i in range(1,numSamples+1):
	left_click(xstart, ystart)		# This takes the picture.
	note = "Picture " + str(i) + ": " + str(t) + " minutes " + get_time() + ". Next pic at: " + get_nextTime(t) # records time of pics
	print note 						# note printed to terminal
	notes.write(note + "\n")		# Saves note to the log file
	save ( "Perfusion-" + date + "-t-" + str(t) ) # Calls save function. Input is name of file

	if t < subset:
		t += interval1
		light( "off" ) # Turns microscope light off
		time.sleep( interval1 * 60 - 60 - 15 ) # This is the actual wait part. -15 for light to warm up, -Z to compensate for save time
		light( "on"  ) # Turns microscope light on
		time.sleep( 15 ) # pause after microscope on for it to warm up
	else:
		t += interval2
		light( "off" ) # Turns microscope light off
		time.sleep( interval2 * 60 - 60 - 15 ) # This is the actual wait part. -15 for light to warm up, -Z to compensate for save time
		light( "on"  ) # Turns microscope light on
		time.sleep( 15 ) # pause after microscope on for it to warm up

print "Note file is called: " + fileName # info printed to terminal

light( off )  # Turns microscope light off

notes.close() # Closes file

print Done
