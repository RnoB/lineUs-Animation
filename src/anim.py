import kinecter.kinecter as kinecter
import drawer.drawer as drawer
import time
import traceback
import numpy as np
import random

def round(x, base=1):
    return base * np.round(x/base)


def drawing(kFrames,frames,angle,angleZ,draw,
            nLines = 400,scale = 70,A0=0,
            resolution=.1,speed = .4,distanceLine=.8 ,distanceFigure = 5.0,
            noise = 0,offsetX = 0,offsetY=0,figurePosition = []):
    kFrames = np.int(kFrames)

    imagePosition = []
    repetitionPosition = []

    
    z = frames[kFrames]
    A = angle[kFrames]+A0
    AZ = angleZ[kFrames]

    

    
    xL = []
    yL = []

    xu,yu = scaler(1,1,scale=scale,offsetX=0,offsetY=0)

    #if speed<distanceLine:
        #speed = distanceLine
    for k in range(0,nLines):

        size = 0
        trial =0
        while(size == 0):
            linePosition = []
            trial+=1 
            xLines = []
            yLines = []

            size = 0
            xChecking = True
            while xChecking:
                kx = random.randint(0, 639)
                ky = random.randint(0, 479)
                x,y = scaler(kx,ky,scale=scale,offsetX=offsetX,offsetY=offsetY)

                x = round(x+(.5-random.random())*xu,resolution/2.0)
                y = round(y+(.5-random.random())*yu,resolution/2.0)
                x1 = round(x,distanceLine)
                y1 = round(y,distanceLine)
                x2 = round(x,distanceFigure)
                y2 = round(y,distanceFigure)
                zTest = z[ky,kx]
                Atest = A[ky,kx]
                if (x2,y2) not in figurePosition and (x1,y1) not in imagePosition:
                    xChecking = False
            running = True
            if np.isnan(zTest) or np.isnan(Atest):
                running=False
            while running:
                xLines.append(y)
                yLines.append(x)
                linePosition.append((round(x,resolution),round(y,resolution)))
                speedZ = speed#*np.cos(AZ[ky,kx])**.2
                angleD = A[ky,kx]+noise*(.5-random.random())
                dxS = x+speedZ*np.cos(angleD)
                dyS = y+speedZ*np.sin(angleD)
                dx = round(dxS,resolution)
                dy = round(dyS,resolution)
                dx1 = round(dx,distanceLine)
                dy1 = round(dy,distanceLine)
                dx2 = round(dx,distanceFigure)
                dy2 = round(dy,distanceFigure)
                dxk,dyk = scaler(dx,dy,scale=scale,offsetX=offsetX,offsetY=offsetY,invert=True)

                if (dxk > -1) and (dxk < 640) \
                and (dyk > -1) and (dyk < 480) \
                and size < 2000 \
                and (dx,dy) not in linePosition\
                and (dx1,dy1) not in imagePosition \
                and (dx2,dy2) not in figurePosition \
                and AZ[ky,kx]-A0<1.5 \
                and dx < 1125 and dy < 2000 \
                and dx > 0 and dy > 0:
                    
                    x=dxS
                    y=dyS
                    
                    kx=dxk
                    ky=dyk
                    zTest = z[ky,kx]
                    Atest = A[ky,kx]
                    AZtest = AZ[ky,kx]
                    size +=speedZ
                    if np.isnan(zTest) or np.isnan(Atest)or np.isnan(AZtest):
                        running=False
                else:
                    running = False
            if trial>100 and size==0:
                size = -1
        if size>0:
            #print("X : "+str(np.min(xLines))+" Y : "+str(np.min(yLines)))
            
            draw.lines(xLines,yLines)
            for position in linePosition:
                imagePosition.append((round(position[0],distanceLine),round(position[1],distanceLine)))
                repetitionPosition.append((round(position[0],distanceFigure),round(position[1],distanceFigure)))

    for position in repetitionPosition:
        if position not in figurePosition:
            figurePosition.append(position)
            if len(figurePosition)>10000000:
                del figurePosition[0]
    return figurePosition

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
    time.sleep(10)
    kinect.start()
    kinect.getDepthFrames(nFrames = nFrames,delay=.01,maxDepth=2049)
    kinect.stop()
    kinect.backgroundSubstract(blur=True,level=10)
    dX,dY,angle,angleZ = kinect.derivateFrames()

    draw = drawer.Drawer()

    scale = 1125
    try:
        for kFrames in range(0,nFrames):






            drawing(kFrames,kinect.frames,angle,angleZ,draw,nLines = 100,scale = scale,A0=0,\
                    distanceLine = 4  ,speed = 4)
            time.sleep(30)

    except Exception as e: 
        print(traceback.format_exc())
        draw.toPosition(0,0,0)
    draw.closeDrawer()  





if __name__ == "__main__":
    main()

