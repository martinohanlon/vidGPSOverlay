import os
import subprocess
import threading
import time
import sysv_ipc

RASPIVIDCMD = ["/home/pi/dev/cbb/vidGPSOverlay/raspivid"]
TIMETOWAITFORABORT = 0.5
SHAREDMEMORYID = 20130821
SEMAPHOREID = 20130822

class RaspiVidController(threading.Thread):
    def __init__(self, filePath, timeout, preview, otherOptions=None):
        threading.Thread.__init__(self)
        
        #setup the raspivid cmd
        self.raspividcmd = RASPIVIDCMD

        #add file path, timeout and preview to options
        self.raspividcmd.append("-o")
        self.raspividcmd.append(filePath)
        self.raspividcmd.append("-t")
        self.raspividcmd.append(str(timeout))
        if preview == False: self.raspividcmd.append("-n")

        #if there are other options, add them
        if otherOptions != None:
            self.raspividcmd = self.raspividcmd + otherOptions

        #set state to not running
        self.running = False

        #setup shared memory and semaphore variable
        self.memory = None
        self.semaphore = None
        
    def run(self):
        #run raspivid
        raspivid = subprocess.Popen(self.raspividcmd)
        
        #loop until its set to stopped or it stops
        self.running = True
        while(self.running and raspivid.poll() is None):
            time.sleep(TIMETOWAITFORABORT)
        self.running = False
        
        #kill raspivid if still running
        if raspivid.poll() == True: raspivid.kill()

    def stopController(self):
        self.running = False

    def getFrameCount(self):
        frameCount = "-1"
        if self.running == True:
            if self.memory == None:
                # Open shared memory object
                self.memory = sysv_ipc.SharedMemory(20130821)
                
            if self.semaphore == None:
                # Open semaphore 
                self.semaphore = sysv_ipc.Semaphore(20130822)

            # Acquire the semaphore
            self.semaphore.acquire(2)

            # Read frame count from shared memory
            frameCount = self.memory.read()

            # Release the semaphore
            self.semaphore.release()

            # Find the 'end' of the string and strip
            i = frameCount.find('\0')
            if i != -1:
                frameCount = frameCount[:i]
                
        return frameCount

if __name__ == '__main__':

    #create raspivid controller
    vidcontrol = RaspiVidController("/home/pi/dev/raspivid/test.h264", 5000, False, ["-fps", "25"])

    try:
        print("Starting raspivid controller")
        #start up raspivid controller
        vidcontrol.start()
        #wait for it to finish
        while(vidcontrol.isAlive() == True):
            print("Current frame - " + str(vidcontrol.getFrameCount()))
            time.sleep(0.5)

    #Ctrl C
    except KeyboardInterrupt:
        print "Cancelled"
    
    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    #if it finishes or Ctrl C, shut it down
    finally: 
        print "Stopping raspivid controller"
        #stop the controller
        vidcontrol.stopController()
        #wait for the tread to finish if it hasn't already
        vidcontrol.join()
        
    print "Done"
