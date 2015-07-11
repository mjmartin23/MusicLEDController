# Matt Martin
# Lights music box with alsaaudio and raspberry pi
# June 2015

import alsaaudio
import numpy as np
import struct
import time
import RPi.GPIO as GPIO
import os
import subprocess
from dotstar import Adafruit_DotStar
 
# constants
CHANNELS    = 1
INFORMAT    = alsaaudio.PCM_FORMAT_FLOAT_LE
RATE        = 44100
FRAMESIZE   = 512

# Set up LED strip
numpixels = 30
datapin = 17
clockpin = 27
#strip = Adafruit_DotStar(numpixels,datapin,clockpin)
#strip = Adafruit_DotStar(numpixels)
stripBright = 128

colors = [(255,0,0),(255,16,0),(255,62,0),(255,110,0),(255,164,0),(255,220,0),(255,255,0),
	(204,255,0),(134,255,0),(0,255,6),(0,255,68),(0,255,162),(0,246,255),(0,180,255),(0,0,255)]

# Oops, initialized colors list backwards, oh well.
# I want red to correspond to low frequency, and blue to high frequency
# So I'll just flip the list
colors = colors[::-1]+colors 

print "THROUGH DECLARATIONS"
    

def smoothAvg(vals):
	# Creates an exponentially weighted average for each actual brightness.
	# Serves to smooth out brightness changes upon refreshes in the LED strip
	
	avg = 0.0
	divisor = 0.0
	for i in range(len(vals)):
		factor = float(1.0/((float(i)+1.0)**2.0))
		divisor += factor
		avg += vals[i]*factor
	return avg/divisor
	


def controlLights(strip,values,brtold):
	signals = float(len(values))

	# Take 15 chunks of frequencies and average their magnitudes
	# The chunks are not evenly weighted because most of the noise
	# that human ears care about is going to be a fairly low (relative)
	# frequency which corresponds to the middle of the 'values' list.
	#
	# LEDs 1, 4-11, and 14 are commented out because I ended up only
	# ended up using the other frequencies (thought it provided for the
	# best visual representation of the music. Lots of trial and error.
	'''
	# LED 1/30:
	avg1 = sum(values[int(signals/16):int(signals/9)])/float(len(values[int(signals/16):int(signals/9)])) # 8 to 14
	#avg1 = sum(values[32:56])/float(len(values[32:56]))
	brt1 = avg1/4.0
	if brt1 > 1.0:
		brt1 = 1.000
	'''
	# LED 2/29:
	avg2 = sum(values[int(signals/9):int(signals/6.3)])/float(len(values[int(signals/9):int(signals/6.3)])) # 14 to 20
	#avg2 = sum(values[56:80])/float(len(values[56:80]))
	brt2 = avg2/4.0
	if brt2 > 1.0:
		brt2 = 1.000

	# LED 3/28:
	avg3 = sum(values[int(signals/6.3):int(signals/5)])/float(len(values[int(signals/6.3):int(signals/5)])) # 20 to 25
	#avg3 = sum(values[80:100])/float(len(values[80:100]))
	brt3 = avg3/4.0
	if brt3 > 1.0:
		brt3 = 1.000

	'''
	# LED 4/27:
	avg4 = sum(values[int(signals/5):int(signals/4.2)])/float(len(values[int(signals/5):int(signals/4.2)])) # 25 to 30
	#avg4 = sum(values[100:120])/float(len(values[100:120]))
	brt4 = avg4/4.0
	if brt4 > 1.0:
		brt4 = 1.000

	# LED 5/26:
	avg5 = sum(values[int(signals/4.2):int(signals/3.5)])/float(len(values[int(signals/4.2):int(signals/3.5)])) # 30 to 36
	#avg5 = sum(values[120:144])/float(len(values[120:144]))
	brt5 = avg5/6.0
	if brt5 > 1.0:
		brt5 = 1.000

	# LED 6/25:
	avg6 = sum(values[int(signals/3.5):int(signals/3.1)])/float(len(values[int(signals/3.5):int(signals/3.1)])) # 36 to 41
	#avg6 = sum(values[144:164])/float(len(values[144:164]))
	brt6 = avg6/10.0
	if brt6 > 1.0:
		brt6 = 1.000

	# LED 7/24:
	avg7 = sum(values[int(signals/3.1):int(signals/2.76)])/float(len(values[int(signals/3.1):int(signals/2.76)])) # 41 to 46
	#avg7 = sum(values[164:184])/float(len(values[164:184]))
	brt7 = avg7/14.0
	if brt7 > 1.0:
		brt7 = 1.000

	# LED 8/23:
	avg8 = sum(values[int(signals/2.76):int(signals/2.54)])/float(len(values[int(signals/2.76):int(signals/2.54)])) # 46 to 50
	#avg8 = sum(values[184:200])/float(len(values[184:200]))
	brt8 = avg8/16.0
	if brt8 > 1.0:
		brt8 = 1.000

	# LED 9/22:
	avg9 = sum(values[int(signals/2.54):int(signals/2.35)])/float(len(values[int(signals/2.54):int(signals/2.35)])) # 50 to 54
	#avg9 = sum(values[200:216])/float(len(values[200:216]))
	brt9 = avg9/20.0
	if brt9 > 1.0:
		brt9 = 1.000

	# LED 10/21:
	avg10 = sum(values[int(signals/2.35):int(signals/2.23)])/float(len(values[int(signals/2.35):int(signals/2.23)])) # 54 to 57
	#avg10 = sum(values[216:228])/float(len(values[216:228]))
	brt10 = avg10/20.0
	if brt10 > 1.0:
		brt10 = 1.000

	# LED 11/20:
	avg11 = sum(values[int(signals/2.23):int(signals/2.153)])/float(len(values[int(signals/2.23):int(signals/2.153)])) # 57 to 59
	#avg11 = sum(values[228:236])/float(len(values[228:236]))
	brt11 = avg11/30.0
	if brt11 > 1.0:
		brt11 = 1.000
	'''
	# LED 12/19:
	avg12 = sum(values[int(signals/2.153):int(signals/2.082)])/float(len(values[int(signals/2.153):int(signals/2.082)])) # 59 to 61
	#avg12 = sum(values[236:244])/float(len(values[236:244]))
	brt12 = avg12/35.0
	if brt12 > 1.0:
		brt12 = 1.000

	# LED 13/18:
	avg13 = sum(values[int(signals/2.082):int(signals/2.048)])/float(len(values[int(signals/2.082):int(signals/2.048)])) # 61 to 62
	#avg13 = sum(values[244:248])/float(len(values[244:248]))
	brt13 = avg13/50.0
	if brt13 > 1.0:
		brt13 = 1.000

	'''
	# LED 14/17:
	avg14 = sum(values[int(signals/2.048):int(signals/2.016)])/float(len(values[int(signals/2.048):int(signals/2.016)])) # 62 to 63
	#avg14 = sum(values[62:63])/float(len(values[62:63]))
	brt14 = avg14/40.0
	if brt14 > 1.0:
		brt14 = 1.000
	'''
	# LED 15/16:
	avg15 = sum(values[int(signals/2.016):int(signals/1.984)])/float(len(values[int(signals/2.016):int(signals/1.984)])) # 63 to 64
	#avg15 = sum(values[63:64])/float(len(values[63:64]))
	brt15 = avg15/110.0
	if brt15 > 1.0:
		brt15 = 1.000

	brtmid = smoothAvg([sum([brt3,brt2])/2.0]+[x[0] for x in brtold])
	brtleft = smoothAvg([sum([brt13,brt12])/2.0]+[x[1] for x in brtold])
	brtright = smoothAvg([brt15]+[x[2] for x in brtold])
	
	
	# Lights will have a mirror effect, high frequencies on the outside, and lowest in the middle
	for i in range(30):
		if i in range(5):
			r,g,b = int(colors[i][0]*brtleft),int(colors[i][1]*brtleft),int(colors[i][2]*brtleft)
		elif i in range(5,9):
			r,g,b = int(colors[i][0]*brtmid),int(colors[i][1]*brtmid),int(colors[i][2]*brtmid)
		elif i in range(9,15):
			r,g,b = int(colors[i][0]*brtright),int(colors[i][1]*brtright),int(colors[i][2]*brtright)
		elif i in range(15,21):
			r,g,b = int(colors[i][0]*brtright),int(colors[i][1]*brtright),int(colors[i][2]*brtright)
		elif i in range(21,25):
			r,g,b = int(colors[i][0]*brtmid),int(colors[i][1]*brtmid),int(colors[i][2]*brtmid)		
		elif i in range(25,30):
			r,g,b = int(colors[i][0]*brtleft),int(colors[i][1]*brtleft),int(colors[i][2]*brtleft)

		strip.setPixelColor(i,min(r,255),min(g,255),min(b,255))
	

	strip.show()
	return [sum([brt3,brt2])/2.0,sum([brt13,brt12])/2.0,brt15]
	


def getMagnitudes(recorder):

	(length,data) = recorder.read()

	if length < 0:
		# For some reason, every couple reads is blank,
		# so I'll throw out these by returning here.
		# Only losing ~1ms
		return
	
	# Unpack data
	unpacked = struct.unpack('f'*length, data)

	y = np.array(unpacked)
	y_L = y[::2]
	y_R = y[1::2]

	Y_L = np.fft.fft(y_L, FRAMESIZE)
	Y_R = np.fft.fft(y_R, FRAMESIZE)
	

	# Sewing FFT of two channels together
	# Y is essentiall the magnitude of frequencies found in the sample
	Y = abs(np.hstack((Y_L[-FRAMESIZE/2:-1], Y_R[:FRAMESIZE/2])))
	
	return Y


def shutdown(strip):
	for i in range(stripBright):
		strip.setBrightness(stripBright-i-1)
		strip.show()
		time.sleep(.01)
	GPIO.cleanup()
	os.system("sudo shutdown -h now")


def main():
	
	# set up audio input...	
	recorder = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
	recorder.setchannels(CHANNELS)
	recorder.setrate(RATE)
	recorder.setformat(INFORMAT)
	recorder.setperiodsize(FRAMESIZE)
	
	# Set up off button	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23,GPIO.IN,pull_up_down = GPIO.PUD_UP)
	
	# Initialize colors of each LED...
	strip = Adafruit_DotStar(numpixels)
	strip.begin()
	for i in range(15):
		time.sleep(float(1.0/float(i+1)))
		strip.setBrightness(int(stripBright*(i+1)/15))
		strip.setPixelColor(i,colors[i][0],colors[i][1],colors[i][2])
		strip.setPixelColor(29-i,colors[29-i][0],colors[29-i][1],colors[29-i][2])
		strip.show()
	time.sleep(1)

	# MAIN LOOP:
	i=0
	bigtime = 0.0
	valsold = []
	print "IN MAIN LOOP"
	try:
		while True:
			
			# Check for off button press
			on = GPIO.input(23)
			if on == False:
				shutdown(strip)
			
			# Read music and get magnitudes for FRAMESIZE length 
			Y = getMagnitudes(recorder)
			if Y != None:
				# Update LED strip based on magnitudes
				vals = controlLights(strip,Y,valsold)
				# Update valsold list which is used by my smoothAvg function
				# to make a running average of brightnesses rather than actual brightnesses
				valsold.insert(0,vals)
				if len(valsold) > 20:
					valsold.pop()
				if i % 1000 == 0:
					print "TIME:",time.time()-bigtime
					print "ITERATION: ",i
					bigtime = time.time()
				i+=1
	except KeyboardInterrupt:
		pass

if __name__ == '__main__':
	main()
