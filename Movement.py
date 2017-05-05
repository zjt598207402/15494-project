from cozmo_fsm import *
from cozmo.util import Pose
import asyncio, time

#needs a global list to hold all the walls
self.parent.walls = {}

class Build_walls(StateNode):
	def start(self):
		#assume self.parent.lines is a tuple of binary (a,b,c)
	    #assume self.parent.cozmo_x is a tuple of coordinates (x,y)
	    #assume self.parent.cozmo_head 0, 1, 2, 3 left front right bottom
	    #assume value of each key [left,top.right,bottom]


	    #heading left
	    if (self.parent.cozmo_head == 0):
	    	if (self.parent.cozmo_x-1,self.parent.cozmo_y) not in self.parent.walls:
	    		self.parent.walls[(self.parent.cozmo_x-1,self.parent.cozmo_y)]=[0,0,0,0]

			#wall at left
			if self.parent.curWall[0] == 1:
				self.parent.walls[(self.parent.cozmo_x-1, self.parent.cozmo_y)][3] = 1

			#wall at top
			if self.parent.curWall[1] == 1:
				self.parent.walls[(self.parent.cozmo_x-1, self.parent.cozmo_y)][0] = 1

			#wall at right
			if self.parent.curWall[2] == 1:
				self.parent.walls[(self.parent.cozmo_x-1, self.parent.cozmo_y)][1] = 1


		#heading top
		if self.parent.cozmo_head == 1:
			if (self.parent.cozmo_x,self.parent.cozmo_y+1) not in self.parent.walls:
	    		self.parent.walls[(self.parent.cozmo_x,self.parent.cozmo_y+1)]=[0,0,0,0]

			#wall at left
			if self.parent.curWall[0] == 1:
				self.parent.walls[(self.parent.cozmo_x, self.parent.cozmo_y+1)][0] = 1

			#wall at top
			if self.parent.curWall[1] == 1:
				self.parent.walls[(self.parent.cozmo_x, self.parent.cozmo_y+1)][1] = 1

			#wall at right
			if self.parent.curWall[2] == 1:
				self.parent.walls[(self.parent.cozmo_x, self.parent.cozmo_y+1)][2] = 1

		#heading right
		if self.parent.cozmo_head == 2:
			if (self.parent.cozmo_x+1,self.parent.cozmo_y) not in self.parent.walls:
	    		self.parent.walls[(self.parent.cozmo_x+1,self.parent.cozmo_y)]=[0,0,0,0]

			#wall at left
			if self.parent.curWall[0] == 1:
				self.parent.walls[(self.parent.cozmo_x+1, self.parent.cozmo_y)][1] = 1

			#wall at top
			if self.parent.curWall[1] == 1:
				self.parent.walls[(self.parent.cozmo_x+1, self.parent.cozmo_y)][2] = 1

			#wall at right
			if self.parent.curWall[2] == 1:
				self.parent.walls[(self.parent.cozmo_x+1, self.parent.cozmo_y)][3] = 1

		#heading bottom
		if self.parent.cozmo_head == 3:
			if (self.parent.cozmo_x,self.parent.cozmo_y-1) not in self.parent.walls:
	    		self.parent.walls[(self.parent.cozmo_x,self.parent.cozmo_y-1)]=[0,0,0,0]

			#wall at left
			if self.parent.curWall[0] == 1:
				self.parent.walls[(self.parent.cozmo_x, self.parent.cozmo_y-1)][2] = 1

			#wall at top
			if self.parent.curWall[1] == 1:
				self.parent.walls[(self.parent.cozmo_x, self.parent.cozmo_y-1)][3] = 1

			#wall at right
			if self.parent.curWall[2] == 1:
				self.parent.walls[(self.parent.cozmo_x, self.parent.cozmo_y-1)][0] = 1

#use left front right moving policy
class DecideMove(StateNode):
	def start(self):
		#heading left
		if self.parent.cozmo_head == 0:
			if self.parent.walls[self.cozmo_x,self.cozmo_y][3] == 0:
				self.parent.angle = 90
				self.post_failure()

			else if self.parent.walls[self.cozmo.x,self.cozmo_y][0] == 0:
				self.parent.distance = 120
				self.post_success()

			else if self.parent.walls[self.cozmo.x,self.cozmo_y][1] == 0:
				self.parent.angle = -90
				self.post_failure()

			else
				self.parent.angle = 180
				self.post_failure()

		if self.parent.cozmo_head == 1:
			if self.parent.walls[self.cozmo_x,self.cozmo_y][0] == 0:
				self.parent.angle = 90
				self.post_failure()
				
			else if self.parent.walls[self.cozmo.x,self.cozmo_y][1] == 0:
				self.parent.distance = 120
				self.post_success()

			else if self.parent.walls[self.cozmo.x,self.cozmo_y][2] == 0:
				self.parent.angle = -90
				self.post_failure()

			else
				self.parent.angle = 180
				self.post_failure()

		if self.parent.cozmo_head == 2:
			if self.parent.walls[self.cozmo_x,self.cozmo_y][1] == 0:
				self.parent.angle = 90
				self.post_failure()
				
			else if self.parent.walls[self.cozmo.x,self.cozmo_y][2] == 0:
				self.parent.distance = 120
				self.post_success()

			else if self.parent.walls[self.cozmo.x,self.cozmo_y][3] == 0:
				self.parent.angle = -90
				self.post_failure()

			else
				self.parent.angle = 180
				self.post_failure()

		if self.parent.cozmo_head == 3:
			if self.parent.walls[self.cozmo_x,self.cozmo_y][2] == 0:
				self.parent.angle = 90
				self.post_failure()
				
			else if self.parent.walls[self.cozmo.x,self.cozmo_y][3] == 0:
				self.parent.distance = 120
				self.post_success()

			else if self.parent.walls[self.cozmo.x,self.cozmo_y][0] == 0:
				self.parent.angle = -90
				self.post_failure()

			else
				self.parent.angle = 180
				self.post_failure()



class ForwardCustom(Forward):
	def start(self, event = None):
        if self.running: return
        self.distance= distance_mm(self.parent.distance)
        super().start()


class TurnCustom(Turn):
	def start(self, event = None):
        if self.running: return
        self.angle = degrees(self.parent.angle)
        super().start()