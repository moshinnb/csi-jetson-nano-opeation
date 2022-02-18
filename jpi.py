#created by MOUSHIN BEPARI
from platform import release
from unittest import runner
import cv2
import numpy as np
import time
import re
# 1920x1080, 30 fps
SENSOR_MODE_1080=2
# 1280x720, 60 fps
SENSOR_MODE_720=3

class pipelineError(Exception):
    def __init__(self,msg):
        self.msg=msg
    def __str__(self):
        return self.msg
class CSI_Camera:
    def __init__(self):
        self.video_capture=None
        self.grabbed=False
        self.frame=None 
        self.running=False      
    @property
    def gstreamer_pipeline(self):
        return self._gstreamer_pipeline
        #return the camera connection object
    def create_gstreamer_pipeline(self,sensor_id,sensor_mode=3,framerate=30,flip_method=0):
        #creates gstreamer pipline by one essential argument sensor-id and all are optionl arguments
        if not isinstance(flip_method,int):
            k=re.split(" |>",str(type(flip_method)))[1]
            raise pipelineError("pipelineError: invalid d-type {} -accepts only 'int' d-type  ".format(k))
        if (flip_method)<0 or  (flip_method)>=8:
            raise pipelineError("pipelineError: {} -select valid flip mode between(0-7)".format(flip_method))
            exit(0)
        if not isinstance(sensor_mode,int):
            k=re.split(" |>",str(type(sensor_mode)))[1]
            raise pipelineError("pipelineError: invalid d-type {} -accepts only 'int' d-type  ".format(k))
        elif (sensor_mode>=2 and sensor_mode<=5):
        
            self._gstreamer_pipeline = (
                "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
                "video/x-raw(memory:NVMM), "
                "format=(string)NV12, framerate=%d/1! "
                "nvvidconv flip-method=%d ! "
                "video/x-raw, format=(string)BGRx ! "
                "videoconvert ! "
                "video/x-raw, format=(string)BGR ! appsink"
                % (
                    sensor_id,
                    sensor_mode,
                    framerate,
                    flip_method,   
                ))
        else:
            raise pipelineError("pipelineError: {} -select sensor mode in between 2-5 only ".format(sensor_mode))
            exit(0)
    def open_C(self,gstreamer_pipeline_string):
        #it opens the camera  by making connection  to gstreamer pipeline
        # if not connected it will return back
        if self.video_capture==None:
            self.video_capture=cv2.VideoCapture(gstreamer_pipeline_string,cv2.CAP_GSTREAMER)
            self.grabbed, self.frame = self.video_capture.read()
            if not  self.grabbed:
                self.video_capture=None
                return 
            else:
                self.running=True
    def release(self):
        if self.video_capture!=None: 
            self.video_capture.release()
            self.video_capture=None
            self.grabbed=False
            self.frame=None
            print("camera is closed")
            return True
        else :
            raise AttributeError

    def C_is_connected(self):
        try:
            self.grabbed, self.frame = self.video_capture.read()
        except AttributeError:
            return False   
        return self.grabbed

    def display(self,b,f_w=500,f_h=500):
        #display shows capture image untill camera is connected as well as ESC pressed 
        try:
            while self.grabbed:
                self.grabbed,self.frame=self.video_capture.read()
                f=cv2.resize(self.frame,(f_w,f_h))
                cv2.imshow("press ESC to exit",f)
                keyCode = cv2.waitKey(30) & 0xFF
                # Stop the program on the ESC key
                if keyCode == 27:
                    break
            cv2.destroyAllWindows()
        except cv2.error:
            print("------------camera {} is dissconnected, please check the connection --------------".format(b))
            return 
        except AttributeError:
            print("---------camera is disconnected---------------")
    def get_frame(self):# return frame      
        try:
            self.grabbed,self.frame=self.video_capture.read()
            return self.frame
        except cv2.error as e:
            print("-----------camera is dissconnected------------------")
            release()
        except AttributeError:
            print("---------------camera is  not started/dissconnected---------------")
            release()
            return None
        
       
#for two cameras two objects are their
c1=CSI_Camera()
c2=CSI_Camera()
def getC(i):
    if not isinstance(i,int):
        k=re.split(" |>",str(type(i)))[1]
        raise pipelineError("pipelineError: invalid d-type {} -accepts only 'int' d-type  ".format(k))
        
    if i!=0 and i!=1:
        raise pipelineError("pipelineError: {} is invalid sensor_id -pass 0 or 1 as argument ".format(i))
       
    elif i==0:
        return c1
    elif i==1:
        return c2
	
		
def start(sensor_id=0,sensor_mode=3,framerate=30,flip_method=6):
    #takes 4 arguments
    #sensor-id is the camera port 0 or 1
    #flip_method ranges from 0-7 -accept that it throughs error
    #sensoe_mode ranges from 2-5
    if getC(sensor_id).grabbed :
        print("-----------------camera is already running------------")
        return True
    elif  getC(sensor_id).video_capture ==None:
        getC(sensor_id).create_gstreamer_pipeline(sensor_id,sensor_mode,framerate,flip_method)
        getC(sensor_id).open_C(getC(sensor_id).gstreamer_pipeline)
    return getC(sensor_id).grabbed

def isConnected(a):
    #takes 0 or 1  as positional arguments and returns boolean value
    return getC(a).C_is_connected()

def isAvailable(a):
    #takes 0/1 as positional arguments which returns boolen value depending on availiblity of camera
    if not getC(a).grabbed:
        start(a)
        if not getC(a).C_is_connected():
            print("-------------------------- : camera {} is not connected /check the connection--------------------------".format(a))
            return None
        getC(a).release()
        print("------: camera {} is ready to use-----------".format(a))
        return True
    else:
        print("-----: camera  {} is in use :-----------".format(a))
        return False
	#check based on sensor-id

def Info():
    print("\n\n---------------------------: Camera Info :---------------------------")
    n1= 1 if isConnected(0)==True else 0
    n2=1 if isConnected(1) ==True else 0
    if n1:
        s=getC(0).gstreamer_pipeline
        str=re.split('=| |/',s)
        s_id,s_md,f_r,f_l=[i for i in str if i.isnumeric()]
        i_h,i_w,i_d=getC(0).get_frame().shape
        
        print("     Camera position =",s_id)
        print("     Camera mode     =",s_md)
        print("     Frame Rate      =",f_r)
        print("     Flip method     =",f_l)
        print("     Capturing Width={0}   Height={1}\n".format(i_w,i_h))
        
    else:
        print("--------------------camera 0 is not connected--------------------------\n\n")
    print("--------------       #######       --------------\n")
    if n2:
        s=getC(1).gstreamer_pipeline
        str=re.split('=| |/',s)
        s_id,s_md,f_r,f_l=[i for i in str if i.isnumeric()]
        i_h,i_w,i_d=getC(1).get_frame().shape
        print("     Camera position =",s_id)
        print("     Camera mode     =",s_md)
        print("     Frame Rate      =",f_r)
        print("     Flip method     =",f_l)
        print("     Capturing Width={0}   Height={1}\n".format(i_w,i_h))
    else:    
        print("--------------------Camera 1 is not connected --------------------\n\n")
    print("--------------       #######      --------------\n")
    print("     Total Number of camera connected = {}\n".format(n1+n2))
    print("---------------------------:  Thank you :---------------------------\n\n")
    #return no

def closeCamera(a):
    #getC(a).release()
    try :
        return getC(a).release()
    except AttributeError:
        print("camera {} is not started yet ".format(a))
        return False
     
    #based on sensor id distroy the object
    #if its not exist return None

def getFrame(a):
    f= getC(a).get_frame()
    return f
	# return frame or None
def display(a,w=500,h=500):
	getC(a).display(a,w,h)      



   
    
    
    
    
