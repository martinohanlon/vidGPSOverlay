# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw

def drawPoint(imagedraw,x,y,width,colour):
    imagedraw.ellipse((x-(width/2),y-(width/2),x+(width/2),y+(width/2)), colour)
    

frame = Image.new("RGBA", (300,300))
frameDraw = ImageDraw.Draw(frame)
#load font
fontpath = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
# use a truetype font
font = ImageFont.truetype(fontpath, 15)
#draw some text
frameDraw.text((0,0),"Hello World", font=font)
#draw a line
frameDraw.line((0, 20, 150, 20), fill="white", width=3)
#draw a point
#frameDraw.ellipse((147, 17, 153, 23), "red")
drawPoint(frameDraw, 150, 20, 10, "red")

frame.save("/home/pi/dev/cbb/vidGPSOverlay/testcode/pil.gif", "GIF")
