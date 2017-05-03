from cozmo_fsm import *
from cozmo.util import Pose
import asyncio, time

#needs a global list to hold all the walls
wall_list[];

async def build_walls():
	#assume self.parent.lines is a tuple of binary (a,b,c)
	d_to_next_box = 4.75
	d_to_front = 2.375
	d_to_left = 2.375
	d_to_right = 2.375

	#wall at left
	if self.parent.lines[0] == 1:
		#build wall at x = cozmo_x + d_to_next_box + d_to_front y = cozmo_y
		
	#wall at front
	if self.parent.lines[1] == 1:
		#build wall at x = cozmo_x + d_to_next_box  y = cozmo_y - d_to_left

	#wall at right
	if self.parent.lines[2] == 1:
		#build wall at x = cozmo_x + d_to_next_box  y = cozmo_y + d_to_right

class DecideMove(StateNode):
	def start(self):
		if (1,0,1):
			self.post_success()
		if (1,1,0):
			angle = -90
			self.post_failure()
		if (0,1,1):
			angle = 90
			self.post_failure()
		if (1,1,1):
			angle = 180
			self.post_failure()

class ForwardCustom(DriveForward):
	#IMPLEMENT

class TurnCustom(DriveTurn):
	#IMPLEMENT
