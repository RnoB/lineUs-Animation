
import time
import math
import numpy as np
import random
import sys
import os
import traceback
from lineus import LineUs





offset = [650,-1000]
sizeMax = [1775-650,1000+1000]





def noiser(xMax):
    return xMax*random.random()



class Drawer:

    penPosition = True
    output = False
    penCode = [1000,0]
    X = []





    def toPosition(self,x0,y0,penPosition):

        if x0 < sizeMax[0] and y0<sizeMax[1] and x0>=0 and y0>=0:
            self.drawer.g01(x0+offset[0],y0+offset[1],self.penCode[penPosition])




    def closeDrawer(self):
        self.drawer.disconnect()



    def line(self,x0,y0,length=1,angle=0):
        
        xf = x0+length*math.cos(angle)
        yf = y0+length*math.sin(angle)
        self.toPosition(x0,y0,1)
        self.toPosition(x0,y0,0)
        self.toPosition(xf,yf,0)
        self.toPosition(xf,yf,1)
        

    def lines(self,x,y):
        x0 = x[0]
        y0 = y[0]
        self.toPosition(x0,y0,1)
        self.toPosition(x0,y0,0)

        k0=0
        try:
            for k in range(0,len(x)):
                k0 = k
                x0 = x[k0]
                y0 = y[k0]
                self.toPosition(x0,y0,0)
            self.toPosition(x0,y0,1)
        except:
            print('--- CRASH !!!! ---')
            print("length : "+str(len(x)))
            print("  k0   : "+str(k0))
            self.toPosition(x[0],y[0],1)


    def __init__(self,output = False,dx = 0,dy=0,de = 40):
        self.drawer = LineUs()
        self.drawer.connect()
