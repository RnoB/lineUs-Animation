#import the necessary modules
import freenect
import cv2
import numpy as np
import time
try:
    from blinkt import set_pixel, set_brightness, show, clear
except:
    pass
import random
try:
    from blinked import blinked
except:
    pass

def round(x, base=1):
    return base * np.round(x/base)




class kinect:    



    def kinectFrame(self,width,height):
        kinectWidth = width
        kinectHeight = height




    def depthToDistance(self,frame):
        depthMeter = 0.1236 * np.tan(frame / 2842.5 + 1.1863)
        return depthMeter


    def get_depth(self):
        print('get depth')
        array = freenect.sync_get_depth()[0]
        print('got depth')
        array=np.float32(array)
        return array


    def getFrames(self,nFrames=30,delay=.5,maxDepth = 945):
        frames = []
        
        for k in range(0,nFrames):
            #blinked.switchColor('r',[3])
            depth = get_depth()
            #blinked.switchColor('g',[3])
            depth[depth>maxDepth]=np.nan
            if np.isnan(depth).all() or len(depth[~np.isnan(depth)])<20000:
                print('all nan')
            else:
            
            
                depthMin = np.min(depth[~np.isnan(depth)])
                depthMax = np.max(depth[~np.isnan(depth)])
            
                frames.append(1-(depth-depthMin)/(depthMax-depthMin))
            time.sleep(delay)
        return frames


    def derivateFrames(self,blur=True,level=10,sobel=False,ksize=-1):
        dX = []
        dY = []
        angle = []
        angleZ = []

        for frame in self.frames:
            if sobel:
                dY.append(cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=ksize))
                dX.append(cv2.Sobel(frame,cv2.CV_64F,0,1,ksize=ksize))
            else:
                dX.append(np.roll(frame, 1, axis=0)-np.roll(frame, -1, axis=0))
                dY.append(np.roll(frame, 1, axis=1)-np.roll(frame, -1, axis=1))
            if blur:
                dX[-1] = self.frameSmoother(dX[-1],level)
                dY[-1] = self.frameSmoother(dY[-1],level)


            angle.append(np.arctan2(dY[-1],dX[-1]))

            norm = np.sqrt(dX[-1]**2+dY[-1]**2)
            dZ = .05
            angleZ.append(np.arctan2(norm,dZ))
        return dX,dY,angle,angleZ




    def scaler(self,x,y,scale=100,offsetX = 5,offsetY = 5,invert=False):
        if invert:
            x2 = np.int(kinectHeight*(x-offsetX)/scale)
            y2 = np.int(kinectHeight*(y-offsetY)/scale)
        else:
            x2 = scale*x/kinectHeight+offsetX
            y2 = scale*y/kinectHeight+offsetY

        return x2,y2

    def frameSmoother(self,frame,level = 10):
    
        temp = np.copy(frame)
        temp[np.isnan(frame)]=0
        temp = cv2.blur(temp,(level,level))
        temp[np.isnan(frame)]=np.nan
        return temp


    def backAcq(self,dev, data, timestamp):
        try:
            blinked.switchColor('r',[3])
        except:
            pass
        self.background.append(np.float32(data))
        try:
            blinked.switchColor('g',[3])
        except:
            pass
        

    def backGroundSubstractor(self,nFrames = 100):
        self.nFrames = nFrames

        self.fgbg = cv2.createBackgroundSubtractorMOG2() 
        freenect.start_depth(self.dev)
        freenect.set_depth_callback(self.dev,self.backAcq)
        self.background = []
        previousProgress = -1
        while len(self.background)<nFrames:
            
            freenect.process_events(self.ctx)
            time.sleep(.01)
            progress = len(self.background)/nFrames
            if progress>previousProgress:
                try:
                    blinked.progressColor(progress,'c','o',pix = [2])
                except:
                    pass
                previousProgress = progress
        for frame in self.background:
            fgmask = self.fgbg.apply(frame,learningRate=0.01)
        self.background = []



    def backgroundSubstract(self,blur=False,level=10,maxValue=2046):
        depth = []
        
        for frame in self.frames:
            fgmask=self.fgbg.apply(frame,learningRate=0)
            kernel = np.ones((5,5),np.uint8)
        
            erosion = cv2.erode(fgmask,kernel,iterations = 3)
            dilate = cv2.dilate(erosion,kernel,iterations = 3)
            frame[frame>maxValue]=np.nan
            frame[dilate==0]=np.nan
            frame[dilate<.7]=np.nan
            if np.isnan(frame).all() or len(frame[~np.isnan(frame)])<self.nMin:
                print('all nan')
            else:
                depthMin = np.min(frame[~np.isnan(frame)])
                depthMax = np.max(frame[~np.isnan(frame)])
            
                depth.append(1-(frame-depthMin)/(depthMax-depthMin))
                if blur:
                    depth[-1] = self.frameSmoother(depth[-1],level)

                

        self.frames = depth
        



    def depthAcq(self,dev, data, timestamp):
        try:
            blinked.switchColor('r',[3])
        except:
            pass
        
        depth = np.float32(data)
        depth[depth>self.maxDepth]=np.nan
        if np.isnan(depth).all() or len(depth[~np.isnan(depth)])<self.nMin:
            print('all nan')
        else:
        
        
            #depthMin = np.min(depth[~np.isnan(depth)])
            #depthMax = np.max(depth[~np.isnan(depth)])
        
            #self.frames.append(1-(depth-depthMin)/(depthMax-depthMin))
            self.frames.append(depth)
        try:
            blinked.switchColor('g',[3])
        except:
            pass
        


    def getDepthFrames(self,delay=.01,nFrames=10,maxDepth=2049):
        self.nFrames = nFrames
        self.delay = delay
        self.maxDepth = maxDepth
        freenect.start_depth(self.dev)
        freenect.set_depth_callback(self.dev,self.depthAcq)
        self.frames = []
        previousProgress = -1
        while len(self.frames)<nFrames:
            progress = len(self.frames)/nFrames
            if progress>previousProgress:
                try:
                    blinked.progressColor(progress,'c','o',pix = [2])
                except:
                    pass
                previousProgress = progress
            
            
            freenect.process_events(self.ctx)
            time.sleep(delay)

    def start(self,degs=10):
        self.ctx = freenect.init()
        if not self.ctx:
            freenect.error_open_device()
        self.dev = freenect.open_device(self.ctx, 0)
        if not self.dev:
            freenect.error_open_device()
        freenect.set_tilt_degs(self.dev,-degs)
        freenect.set_tilt_degs(self.dev,degs)
        self.intialised == True
        print('kinect Started')

    def stop(self):
        freenect.close_device(self.dev)
        freenect.shutdown(self.ctx)
        print('kinect Stopped')

    def __init__(self,output = False,nFrames = 10,delay = .5):
        self.kinectWidth = 640
        self.kinectHeight = 480
        self.intialised = False
        self.record = False

        self.ctx = []
        self.dev = []
        self.frames = []
        self.blur = []
        self.nFrames = nFrames
        self.delay = delay
        self.background = []
        self.fgbg = []
        self.fgmask = []
        self.nMin = 2000
        self.maxDepth = 2049

        self.depthM = []





