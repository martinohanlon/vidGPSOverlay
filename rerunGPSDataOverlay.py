#test code to re-run GPS data from data.csv and re-create the images

from PIL import Image, ImageFont, ImageDraw
from RaspividController import *
from GPSController import *
import time
import datetime

DATAFRAME_WIDTH = 500
DATAFRAME_HEIGHT = 300
MAP_WIDTH = 300
MAP_HEIGHT = 300
MAX_SCALE = 1
FONT_PATH = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
VIDEOTIME = 300000

def drawPoint(imagedraw,x,y,width,colour):
    imagedraw.ellipse((x-(width/2),y-(width/2),x+(width/2),y+(width/2)), colour)

class DataDrawer():
    def __init__(self, imagesFolder):
        #setup variables
        self.imagesFolder = imagesFolder
        self.imageSize = (300,300)
        self.minX = 99999999999
        self.maxX = -99999999999
        self.minY = 99999999999
        self.maxY = -99999999999
        self.lastFrameNo = 0
        self.lastLat = 0
        self.lastLon = 0
        self.xyPositions = []
        self.mapScale = 1
        self.padX = 0
        self.padY = 0
        #load font
        self.font = ImageFont.truetype(FONT_PATH, 14)
        #create first frame
        self.newDataFrame(1, 0, 0 ,0)
        
        
    def newDataFrame(self, frameNo, speed, lat, lon):
        #check to make sure the frame has moved on since last time
        if frameNo > self.lastFrameNo:
            
            #create sumbolic links between last frame and this frame
            for missingFrameNo in range(self.lastFrameNo+1, frameNo): 
                os.symlink(self.imagesFolder + "/" + "{0:06d}".format(self.lastFrameNo) + ".jpg",
                           self.imagesFolder + "/" + "{0:06d}".format(missingFrameNo) + ".jpg")

            #create new image
            frame = Image.new("RGBA", (DATAFRAME_WIDTH, DATAFRAME_HEIGHT))
            frameDraw = ImageDraw.Draw(frame)

            #data
            frameDraw.text((315,10),"    Speed " + str(round(speed,2)),font=self.font)
            frameDraw.text((315,50)," Latitude " + str(lat),font=self.font)
            frameDraw.text((315,90),"Longitude " + str(lon),font=self.font)
            
            #map
            #only create map if we have a GPS fix
            if lat != 0 and lon != 0:
                #only add a new set of coords if the lat and lon have changed
                if self.lastLat != lat or self.lastLon != lon:
                    #get x & y coords
                    x,y = GpsUtils.latLongToXY(lat, lon)

                    #add x,y to list
                    self.xyPositions.append([x,y])
                
                    #update mins and maxs
                    if x < self.minX: self.minX = x
                    if x > self.maxX: self.maxX = x
                    if y < self.minY: self.minY = y
                    if y > self.maxY: self.maxY = y

                    #persist lat and lon
                    self.lastLat = lat
                    self.lastLon = lon
                
                    #calculate scale
                    diffX = self.maxX - self.minX
                    #print "diffX " + str(diffX)
                    diffY = self.maxY - self.minY
                    #print "diffY " + str(diffY)
                    if diffX > diffY: 
                        if diffX != 0: self.mapScale = MAP_WIDTH / float(diffX)
                        else: self.mapScale = 1
                    else: 
                        if diffY != 0: self.mapScale = MAP_HEIGHT / float(diffY)
                        else: self.mapScale = 1
                
                    #print "mapScale " + str(self.mapScale)

                    #set max scale
                    if self.mapScale > MAX_SCALE: self.mapScale = MAX_SCALE 
                
                    #re-calculate padding
                    self.padX = int((MAP_WIDTH - (diffX * self.mapScale)) / 2)
                    self.padY = int((MAP_HEIGHT - (diffY * self.mapScale)) / 2)

                #draw lines
                #print len(self.xyPositions)
                for position in range(1, len(self.xyPositions)):
                    #print self.xyPositions[position-1]
                    #print self.xyPositions[position]
                    #draw line between previous position and this one
                    x1 = self.padX + abs((self.xyPositions[position-1][0] * self.mapScale) - (self.minX * self.mapScale))
                    y1 = self.padY + abs((self.xyPositions[position-1][1] * self.mapScale) - (self.maxY * self.mapScale))
                    x2 = self.padX + abs((self.xyPositions[position][0] * self.mapScale) - (self.minX * self.mapScale))
                    y2 = self.padY + abs((self.xyPositions[position][1] * self.mapScale) - (self.maxY * self.mapScale))
                    #x1 = self.padX + int((self.xyPositions[position-1][0] - self.minX) * self.mapScale)
                    #y1 = self.padY + int((self.xyPositions[position-1][1] - self.minY) * self.mapScale)
                    #x2 = self.padX + int((self.xyPositions[position][0] - self.minX) * self.mapScale)
                    #y2 = self.padY + int((self.xyPositions[position][1] - self.minY) * self.mapScale)
                    #print "coords - " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2)
                    frameDraw.line((x1, y1, x2, y2), fill="white", width=3)

                #draw start and end point
                if len(self.xyPositions) > 1:
                    # start
                    drawPoint(frameDraw, self.padX + abs((self.xyPositions[0][0] * self.mapScale) - (self.minX * self.mapScale)), self.padY + abs((self.xyPositions[0][1] * self.mapScale) - (self.maxY * self.mapScale)), 10, "red")
                    # end
                    drawPoint(frameDraw, self.padX + abs((self.xyPositions[len(self.xyPositions)-1][0] * self.mapScale) - (self.minX * self.mapScale)), self.padY + abs((self.xyPositions[len(self.xyPositions)-1][1] * self.mapScale) - (self.maxY * self.mapScale)), 10, "green")
            #save image
            frame.save(self.imagesFolder + "/" + "{0:06d}".format(frameNo) + ".jpg", "JPEG")
            #time.sleep(3)
            #update last frame
            self.lastFrameNo = frameNo
            
if __name__ == "__main__":

    #open data file
    datafile = open("/home/pi/dev/cbb/vidGPSOverlay/data/201310177415/data.csv", "r")

    #create data drawer class
    datadrawer = DataDrawer("/home/pi/dev/cbb/vidGPSOverlay/datatest")

    count=0

    #for each line 
    for line in datafile:
        resultstring = line
        dataitems = line.split(",")
        #create frame
        datadrawer.newDataFrame(int(dataitems[0]), float(dataitems[1]), float(dataitems[2]), float(dataitems[3]))
        count += 1
        if count==500: break

    datafile.close()
