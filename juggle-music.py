#!/usr/bin/env python

'''
Juggle Music
================

Trigger playback of samples by juggling.

On launch the user will be prompted to select the red, blue and green balls.
These will then be positionally tracked and trigger the samples assigned to 
regions of "juggle space".

Controls:
-----
	ESC key  		- exit
	left mouse button	- report color of pixel under cursor
'''

import numpy as np
import cv2
from mingus.midi import fluidsynth

fluidsynth.init('/usr/share/sounds/sf2/FluidR3_GM.sf2',"alsa")

class App(object):
	def __init__(self, video_src):
		self.cam = cv2.VideoCapture(video_src)
		ret, self.frame = self.cam.read()
		cv2.namedWindow('juggle-music')
		cv2.setMouseCallback('juggle-music', self.onmouse)

		# set up font for writing text
		self.font = cv2.FONT_HERSHEY_SIMPLEX

		# a dictionary of our tracked objects with their hue range
		self.objects = dict()
		self.tracking = False

	def onmouse(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.selection = self.hsv[y, x]
			low = self.selection[0] - 5
			high = self.selection[0] + 5
			self.objects[self.this_obj] = (np.array((low, 80, 80)), np.array((high, 255, 255)))
			self.tracking = True

	def run(self):
		while True:
			# read from the webcam
			ret, self.frame = self.cam.read()
			width = np.size(self.frame, 1)
			
			if len(self.objects) < 3:
				cv2.rectangle(self.frame, (0,0), (width,50), (0,0,0), -1)
				if not "orange" in self.objects:
					cv2.putText(self.frame,"Click on the orange object", (100,30), self.font, 1, (0,115,255), 2)
					self.this_obj = "orange"
				elif not "yellow" in self.objects:
					cv2.putText(self.frame,"Click on the yellow object", (100,30), self.font, 1, (0,240,255), 2)
					self.this_obj = "yellow"
				elif not "red" in self.objects:
					cv2.putText(self.frame,"Click on the red object", (100,30), self.font, 1, (0,0,255), 2)
					self.this_obj = "red"
				
			# smooth it
			self.frame = cv2.blur(self.frame,(3,3))

			# convert to hsv and find range of colors
			self.hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)
			
			if self.tracking:
				# draw a blue dot in the center of each object
				# it will be this point which is tracked for sample triggering
				for obj, bounds in self.objects.iteritems():
					try:
						col_range = cv2.inRange(self.hsv,bounds[0],bounds[1])

						# find contours in the threshold images
						contours,hierarchy = cv2.findContours(col_range,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

						# finding contour with maximum area and store it as best_cnt
						max_area = 0
						for cnt in contours:
							area = cv2.contourArea(cnt)
							if area > max_area:
								max_area = area
								best_cnt = cnt

						# finding centroids of best_cnt and draw a circle there
						M = cv2.moments(best_cnt)
						cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
						cv2.circle(self.frame,(cx,cy),5,255,-1)
						
						if cx < 150 and cy < 150:
							print("triggered by %s" % obj)
							fluidsynth.play_Note(64,0,100)
					except:
						print("no color range for %s yet" % obj)

			# Show it, if key pressed is 'Esc', exit the loop
			cv2.imshow('juggle-music',self.frame)

			ch = 0xFF & cv2.waitKey(5)
			if ch == 27:
				break
				
		cv2.destroyAllWindows()


if __name__ == '__main__':
	import sys
	try: video_src = sys.argv[1]
	except: video_src = 0
	print __doc__
	App(video_src).run()
