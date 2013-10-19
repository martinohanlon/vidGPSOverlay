#script to run the whole vid gps capture
/home/pi/dev/cbb/vidGPSOverlay/startGPSService.sh
sudo python /home/pi/dev/cbb/vidGPSOverlay/waitforbutton.py
python /home/pi/dev/cbb/vidGPSOverlay/vidGPSOverlay.py
/home/pi/dev/cbb/vidGPSOverlay/stopGPSService.sh
sudo python /home/pi/dev/cbb/vidGPSOverlay/waitforbutton.py
sudo shutdown -h now
