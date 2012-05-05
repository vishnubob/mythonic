#!/usr/bin/env python
#       


from Tkinter import *
from PIL import Image, ImageTk
from collections import namedtuple
from struct import unpack
import serial


class Wall_Visualizer(object):
    PIXEL_WIDTH = 100

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tk_init()
        self.cull_list = []

    def tk_init(self):
        self.root = Tk()
        self.root.title("Wall %d x %d" % (self.width, self.height))
        self.root.resizable(0, 0)
        self.frame = Frame(self.root, bd=5, relief=SUNKEN)
        self.frame.pack()

        self.canvas = Canvas(self.frame,
                             width=self.PIXEL_WIDTH * self.width,
                             height=self.PIXEL_WIDTH * self.height,
                             bd=0, highlightthickness=0)
        self.canvas.pack()
        self.root.update()
        
    def loadImage(self, filename):
		img = Image.open(filename).resize((self.PIXEL_WIDTH-1, self.PIXEL_WIDTH-1)).convert("RGBA")
		return ImageTk.PhotoImage(img)

    def draw(self, wall):
        for item in self.cull_list:
            self.canvas.delete(item)
        self.cull_list = []
        for box in wall:
			x_0 = box.x * self.PIXEL_WIDTH
			y_0 = box.y * self.PIXEL_WIDTH
			x_1 = x_0 + self.PIXEL_WIDTH
			y_1 = y_0 + self.PIXEL_WIDTH

			color = "#%02x%02x%02x" % (box.color[0], box.color[1], box.color[2])

			rect = self.canvas.create_rectangle(x_0, y_0, x_1, y_1, fill=color)
			self.cull_list.append(rect)

			self.canvas.create_text(x_0+self.PIXEL_WIDTH-2, y_0+2, anchor=NE, text=box.id)
			self.canvas.create_image(x_0+1, y_0+1, anchor=NW, image=box.image)


        self.canvas.update()

def main():
	
	if len(sys.argv) < 2:
		print "usage: python sssim.py /dev/ttySerialPort"
		exit(0)
		
	sport = serial.Serial(sys.argv[1], 9600, timeout=1)	
	
	gui = Wall_Visualizer(6,5)
	
	Box = namedtuple('Box', 'id x y color image')
	wall = [
		Box(0, 0, 1, (255, 0, 0), gui.loadImage("placeholder.png")),
		Box(1, 0, 2, (255, 0, 0), gui.loadImage("placeholder.png")),
		Box(2, 1, 2, (0, 255, 0), gui.loadImage("placeholder.png")),
		Box(3, 1, 3, (0, 255, 0), gui.loadImage("placeholder.png")),
		Box(4, 1, 4, (0, 255, 0), gui.loadImage("placeholder.png")),
		Box(5, 2, 4, (0, 255, 0), gui.loadImage("placeholder.png")),
		Box(6, 2, 2, (100, 100, 255), gui.loadImage("placeholder.png")),
		Box(7, 2, 1, (100, 100, 255), gui.loadImage("placeholder.png")),
		Box(8, 2, 0, (100, 100, 255), gui.loadImage("placeholder.png")),
		Box(9, 3, 0, (100, 100, 255), gui.loadImage("placeholder.png")),
		Box(10, 3, 2, (100, 100, 100), gui.loadImage("placeholder.png")),
		Box(11, 3, 3, (100, 100, 100), gui.loadImage("placeholder.png")),
		Box(12, 3, 4, (100, 100, 100), gui.loadImage("placeholder.png")),
		Box(13, 4, 4, (100, 100, 100), gui.loadImage("placeholder.png")),
		Box(14, 5, 4, (100, 100, 100), gui.loadImage("placeholder.png")),
		Box(15, 4, 2, (0, 0, 255), gui.loadImage("placeholder.png")),
		Box(16, 4, 1, (0, 0, 255), gui.loadImage("placeholder.png")),
		Box(17, 4, 0, (0, 0, 255), gui.loadImage("placeholder.png")),
		Box(18, 5, 0, (0, 0, 255), gui.loadImage("placeholder.png")),
		Box(19, 5, 2, (255, 0, 255), gui.loadImage("placeholder.png")),
	]
		 
	while 1:
		gui.draw(wall)
		bytedata = sport.read(1)
		if bytedata == 'm':
			bytedata = sport.read(120)
			if len(bytedata) == 120:
				data = unpack('120c', bytedata)
				for b in range(0,19):
					wall[b].color = (data[b*6+0], data[b*6+1], data[b*6+2])
	
	return 0

if __name__ == '__main__':
	main()



