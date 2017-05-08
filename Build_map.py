from tkinter import *

def drawBox(canvas, x, y, walld,w1,w2,w3,w4):
    wallr = walld/2
    #left wall
    if w1 == 1:
        canvas.create_line(x-wallr, y-wallr, x-wallr, y+wallr, fill="black", width=2)
    #top wall
    if w2 == 1:
        canvas.create_line(x-wallr, y-wallr, x+wallr, y-wallr, fill="black", width=2)
    #right wall
    if w3 == 1:
        canvas.create_line(x+wallr, y-wallr, x+wallr, y+wallr, fill="black", width=2)
    #bottom wall
    if w4 == 1:
        canvas.create_line(x-wallr, y+wallr, x+wallr, y+wallr, fill="black", width=2)

def draw(canvas, width, height, wall_dict, coz_x, coz_y):
    # because in tkinter y frows downward
    coz_y = -coz_y
    centerx = width/2
    centery = height/2
    circler = 14
    circled = circler * 2
    walld = circled
    canvas.create_oval(centerx-circler+circled*(coz_x), centery-circler+circled*(coz_y), centerx+circler+circled*(coz_x), centery+circler+circled*(coz_y), fill="red")
    wall_list = list(wall_dict.keys())
    for i in wall_list:
        wallx, wally = i
        #because in tkinter y grows downward
        wally = -wally
        [w1,w2,w3,w4] = wall_dict[i]
        drawBox(canvas, centerx+walld*(wallx),centery+walld*(wally), walld, w1, w2, w3, w4)
        

def runDrawing(root, canvas, width, height, wall_dict, coz_x, coz_y):
    canvas.delete("all")
    draw(canvas, width, height, wall_dict, coz_x, coz_y)
    root.update()
    print("bye!")