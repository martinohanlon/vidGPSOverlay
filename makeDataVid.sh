mencoder "mf://*.jpg" -mf fps=25 -o test.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=800000

#MUCH SLOWER, but seems to be better quality and creates an mp4 rather than avi
#ffmpeg -r 25 -b 1800 -i %06d.jpg testdata.mp4

