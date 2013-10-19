from gps import *
import time
import threading
import math

class GpsUtils():

    MPS_TO_MPH = 2.2369362920544

    @staticmethod
    def latLongToXY(lat, lon):
    
        rMajor = 6378137 # Equatorial Radius, WGS84
        shift = math.pi * rMajor
        x = lon * shift / 180
        y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
        y = y * shift / 180

        return x,y

class GpsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.running = False
     
    def run(self):
        self.running = True 
        while self.running:
            # grab EACH set of gpsd info to clear the buffer
            self.gpsd.next()

    def stopController(self):
        self.running = False
    
    @property
    def fix(self):
        return self.gpsd.fix

    @property
    def utc(self):
        return self.gpsd.utc

    @property
    def satellites(self):
        return self.gpsd.satellites
 
if __name__ == '__main__':
    gpsc = GpsController() # create the thread
    try:
        gpsc.start() # start it up
        while True:
            
            print "latitude ", gpsc.fix.latitude
            print "longitude ", gpsc.fix.longitude
            #print "time utc ", gpsc.utc, " + ", gpsc.gpsd.fix.time
            print "altitude (m)", gpsc.fix.altitude
            #print "eps ", gpsc.gpsd.fix.eps
            #print "epx ", gpsc.gpsd.fix.epx
            #print "epv ", gpsc.gpsd.fix.epv
            #print "ept ", gpsc.gpsd.fix.ept
            print "speed (m/s) ", gpsc.fix.speed
            #print "climb ", gpsc.gpsd.fix.climb
            print "track ", gpsc.gpsd.fix.track
            #print "mode ", gpsc.gpsd.fix.mode
            #print "sats ", gpsc.satellites
            print "climb ", gpsc.fix.climb
            #print "heading ", gpsc.fix.direction
            x,y = GpsUtils.latLongToXY(gpsc.fix.latitude, gpsc.fix.longitude)
            print "x", x
            print "y", y
            time.sleep(0.5)

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        print "Stopping gps controller"
        gpsc.stopController()
        #wait for the tread to finish
        gpsc.join()
        
    print "Done"
