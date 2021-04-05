import kinecter.kinecter as kinecter
import drawer.drawer as drawer
import time




def scaler(x,y,scale=100,offsetX = 5,offsetY = 5,invert=False):
    if invert:
        x2 = np.int(480*(x-offsetX)/scale)
        y2 = np.int(480*(y-offsetY)/scale)
    else:
        x2 = scale*x/480+offsetX
        y2 = scale*y/480+offsetY

    return x2,y2



def main():

    nFrames = 100

    kinect = kinecter.kinect()
    kinect.start()
    kinect.backGroundSubstractor(nFrames=100)
    kinect.stop()
    time.sleep(30)
    kinect.start()
    kinect.getDepthFrames(nFrames = nFrames,delay=.01,maxDepth=2049)
    kinect.stop()
    kinect.backgroundSubstract(blur=True,level=10)
    dX,dY,angle,angleZ = kinect.derivateFrames()

    draw = drawer.Drawer()

    scale = 1125
    try:
        for kFrames in range(0,nFrames):






            X2 = drawing(kFrames,kinect.frames,angle,angleZ,draw,nLines = 250,scale = scale,A0=0,\
                    offsetX = offsetX,offsetY=offsetY,figurePosition = X2,distanceLine = 4  ,speed = 4)
            

    except Exception as e: 
        print(traceback.format_exc())
        draw.toPosition(0,0)
    draw.closeDrawer()  





if __name__ == "__main__":
    main()

