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
import video

class App(object):
	def __init__(self, video_src):
		self.cam = video.create_capture(video_src)
		ret, self.frame = self.cam.read()
		cv2.namedWindow('juggle-music')
		cv2.setMouseCallback('juggle-music', self.onmouse)

		self.selection = None
		self.tracking_state = 0

	def onmouse(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.tracking_state = 0
			self.selection = self.hsv[y, x]
			print(self.selection)

	def run(self):
		while True:
			ret, self.frame = self.cam.read()
			vis = self.frame.copy()
			
			# smooth it
			self.frame = cv2.blur(self.frame,(3,3))

			# convert to hsv and find range of colors
			self.hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)
			
			# a dictionary of our tracked objects with their hue range
			objects = dict()
			objects["orange"] = (np.array((5, 80, 80)), np.array((15, 255, 255)))
			objects["yellow"] = (np.array((18, 80, 80)), np.array((25, 255, 255)))
			objects["red"] = (np.array((172, 80, 80)), np.array((182, 255, 255)))
			
			# draw a blue dot in the center of each object
			# it will be this point which is tracked for sample triggering
			for color, bounds in objects.iteritems():
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
