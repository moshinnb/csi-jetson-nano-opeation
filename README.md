# csi-jetsonnao-opeation

Jetson-nano 4gb module and CSI camera V2.1\

## test camera
test camera before running\
run following command\
    `gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! \
   'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1' ! \
   nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=540' ! \
   nvvidconv ! nvegltransform ! nveglglessink -e`\
  Note sensor id 0 or 1\
  Ctrl^C to exit
  
  ### libraries
  Python 3.6.9 \
  cv2 4.1.1\
  numpy
  re
  
  
  ### jpi.py
The jpi file contains following functions\

1.strat() takes 4 arguments\
   position of camera i.e sensor_id=0 or 1\
   sensor_mode=3( H.D),2(full H.D),4\
   framerate=30any interger u can specify\
   flip_method=6 0-7 \\
2.isConnected takes 0 or 1  as positional arguments and returns boolean value\
3.Info doesn't takes any arguments prints the information about cameras\
4.closeCamera takes 0 or 1 as positional argument and closes the camera \
5.getFrame() takes 0 or 1 as positional argument returns frame \
6.display takes 3 arguments 0 or 1,hieght,width \
7.isAvailable() takes 0/1 as positional arguments which returns boolen value depending on availiblity of camera\

