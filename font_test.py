# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 13:39:10 2018

@author: Yettee
"""

import numpy as np
#from math import *
import matplotlib.pyplot as plt

from FF6Font import *



#read from offset of smallfont some number of bytes larger than font size (20000 bytes is enough)

with open('D:\\ff.gba','rb') as f:
	f.seek(0x161FF4) # #16320C 
	#f.seek(0x4E870C) # #16320C
	#f.seek(0x162CD0) # #16320C	
	readb=f.read(20000)
	rawfont=bytearray(readb)

#make 4 -colors palette
pal=[(0,0,255),(255,255,255),(0,0,0),(128,128,128)]

#load byte array with font in parser
font=FF6Font(rawfont)

#obtain font symbols with given palette
fontsymbols=font.getsymbols(palette=pal)

print 'Font height = {nRows} rows; number of symols = {nSymbols}'.format(**font.getfontprops())  #print properties of font
print "Number of pointers = ",len(font.getptrpage())
print "Readed symbols = ",len(res) #must be equal to number of pointers and nSymbols

rows=font.getfontprops()['nRows']

#loading alphabet
alphabet=font.getalphabet()

#making empty pict with nRows height
alphabet_pict=[]
for i in range(rows):
	alphabet_pict.append([])




for symbol in alphabet:
	if res[symbol]["columns"]>0	:
		for i in range(rows):
			alphabet_pict[i]+=res[symbol]["symbol"][i]

#convert to np array
pict=np.array(alphabet_pict,np.uint8)

#show pict with matplotlib pyplot
plt.figure()

plt.imshow(pict,aspect="equal",interpolation="none")

plt.show()
			

	