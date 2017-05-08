from cozmo_fsm import *
from Build_map import *

class Build_walls(StateNode):
    def start(self, event=None):
        #assume self.parent.lines is a tuple of binary (a,b,c)
        #assume self.parent.cozmo_x is a tuple of coordinates (x,y)
        #assume self.parent.cozmo_head 0, 1, 2, 3 left front right bottom
        #assume value of each key [left,top.right,bottom]

        if self.running: return
        #heading left
        super().start(event)

        if (self.parent.curWall ==[0,0,0]):
            self.post_completion()

        print("Building Walls")
        print("Cozmo_X: ", self.parent.cozmo_x)
        print("Cozmo_Y: ", self.parent.cozmo_y)
        print("Heading: ", self.parent.cozmo_head)
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
        
        runDrawing(self.parent.root, self.parent.canvas, self.parent.canvas_width, \
            self.parent.canvas_height,self.parent.walls, self.parent.cozmo_x, self.parent.cozmo_y)
        self.post_completion()


#use left front right moving policy
class DecideMove(StateNode):
    def start(self, event=None):
        #heading left
        if self.running: return
        super().start(event)

        right_angle = 93
        distance_forward = 120
        back_angle = 193

        print("Deciding Move")
        print("dictionary:", self.parent.walls)
        if self.parent.cozmo_head == 0:
            #forward
            if self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][0] == 0:
                print("Forward0")
                self.parent.distance = distance_forward
                if self.parent.walls[self.parent.cozmo_x-1,self.parent.cozmo_y][0] == 1:
                    self.parent.distance = self.parent.distanceForward
                self.parent.cozmo_x -= 1
                self.post_success()

            #turn left
            elif self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][3] == 0:
                print("Left0")
                self.parent.angle = right_angle
                self.parent.cozmo_head = 3
                self.post_failure()

            #turn right
            elif self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][1] == 0:
                print("Right0")
                self.parent.angle = -right_angle
                self.parent.cozmo_head = 1
                self.post_failure()

            #turn around
            else:
                print("Turn Around0")
                self.parent.angle = back_angle
                self.parent.cozmo_head = 2
                self.post_failure()

        elif self.parent.cozmo_head == 1:
            if self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][1] == 0:
                print("Forward1")
                self.parent.distance = distance_forward
                if self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y+1][1] == 1:
                    self.parent.distance = self.parent.distanceForward
                self.parent.cozmo_y += 1
                self.post_success()
                
            elif self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][0] == 0:
                print("Left1")
                self.parent.angle = right_angle
                self.parent.cozmo_head = 0
                self.post_failure()

            elif self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][2] == 0:
                print("Right1")
                self.parent.angle = -right_angle
                self.parent.cozmo_head = 2
                self.post_failure()

            else:
                print("Turn Around1")
                self.parent.angle = back_angle
                self.parent.cozmo_head = 3
                self.post_failure()

        elif self.parent.cozmo_head == 2:
            if self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][2] == 0:
                print("Forward2")
                self.parent.distance = distance_forward
                if self.parent.walls[self.parent.cozmo_x+1,self.parent.cozmo_y][2] == 1:
                    self.parent.distance = self.parent.distanceForward
                self.parent.cozmo_x += 1
                self.post_success()
                
            elif self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][1] == 0:
                print("Left2")
                self.parent.angle = right_angle
                self.parent.cozmo_head = 1
                self.post_failure()

            elif self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][3] == 0:
                print("Right2")
                self.parent.angle = -right_angle
                self.parent.cozmo_head = 3
                self.post_failure()

            else:
                print("Turn Around2")
                self.parent.angle = back_angle
                self.parent.cozmo_head = 0
                self.post_failure()

        elif self.parent.cozmo_head == 3:
            if self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][3] == 0:
                print("Forward3")
                self.parent.distance = distance_forward
                if self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y-1][3] == 1:
                    self.parent.distance = self.parent.distanceForward
                self.parent.cozmo_y -= 1
                self.post_success()
                
            elif self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][2] == 0:
                print("Left3")
                self.parent.angle = right_angle
                self.parent.cozmo_head = 2
                self.post_failure()

            elif self.parent.walls[self.parent.cozmo_x,self.parent.cozmo_y][0] == 0:
                print("Right3")
                self.parent.angle = -right_angle
                self.parent.cozmo_head = 0
                self.post_failure()

            else:
                print("Turn Around3")
                self.parent.angle = back_angle
                self.parent.cozmo_head = 1
                self.post_failure()



class ForwardCustom(Forward):
    def start(self, event = None):
        if self.running: return
        print("Driving Forward")
        self.distance= distance_mm(self.parent.distance)
        super().start()


class TurnCustom(Turn):
    def start(self, event = None):
        if self.running: return
        print("Turning")
        self.angle = degrees(self.parent.angle)
        super().start()