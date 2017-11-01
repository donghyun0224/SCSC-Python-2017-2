#!/usr/bin/env python3
from docwriter import *
from math import sin,pi

def printFuncTable(dwrt,func,start,stop,step=1):
    pos=start
    ptlst=list()
    while pos<stop:
            ptlst.append(pos)
            pos+=step
    val={i:func(i) for i in ptlst}
    dwrt.write(val,"x","f(x)")
    
smpwr=DocWriter("simple.txt")
prtwr=TxtWriter("pretty.txt")
htmwr=HTMLWriter("tbl.html")
smpwr.open()
prtwr.open()
htmwr.open()
printFuncTable(smpwr,sin,-pi,pi,0.2)
printFuncTable(prtwr,sin,-pi,pi,0.2)
printFuncTable(htmwr,sin,-pi,pi,0.2)
smpwr.close()
prtwr.close()
htmwr.close()
