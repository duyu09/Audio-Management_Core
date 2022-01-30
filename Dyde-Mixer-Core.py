# Copyright (c) 2020-2022 Qilu University of Technology, College of Computer Science And Technology,Duyu No.202103180009
# Dyde-Mixer-Core.py
import os
import sys
import numpy as np
from scipy.io import wavfile
from scipy import signal
import pygame
import threading

window_wid=500
window_hei=300
prog_posi = (100,150)
WHITE = (255,255,0)
proc = 0
count=0
con = 0

def upnew():
   image1 = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + r"\Image\Dyde-Mixer-Core-Background.bmp")
   image2 = pygame.transform.scale(image1,(window_wid,window_hei))
   window.blit(image2,(0,0))
   pygame.display.flip()
   global proc
   global count
   global con
   while True:
       try:
           proc = int(con*100/count)
       except:
          print("err")
       prog_text = prog_font.render("Process:%d%%" % proc, False, WHITE)
       window.blit(image2,(0,0))
       window.blit(prog_text, prog_posi)
       pygame.display.update()
       pygame.event.get()
       
def splitChannel(srcMusicFile1,srcMusicFile2,desMusicFile,Aleft1,Aright1,Aleft2,Aright2,SRate,Mode): # SRate=0 means default. # Mode=0 means plus,Mode=1 means subtraction.
   # read wav file
   sampleRate1, musicData1 = wavfile.read(srcMusicFile1)
   sampleRate2, musicData2 = wavfile.read(srcMusicFile2)
   if Aleft1 == 0:
      Aleft1 = 1
   if Aright1 == 0:
      Aright1 = 1
   if Aleft2 == 0:
      Aleft2 = 1
   if Aright2 == 0:
      Aright2 = 1
   if SRate == 0:
      SRate = sampleRate1
   left1 = []
   right1 = []
   left2 = []
   right2 = []
   mixed_data1 = []
   mixed_data2 = []
   mixed_data3 = []
   global count
   count = len(musicData1) + len(musicData2)
   pygame.display.update()
   global con
   global proc
   global WHITE
   SECOND = threading.Thread(target=upnew, daemon=True).start()

   for item1 in musicData1:
       left1.append((Aleft1*item1[0]).astype(item1[0].dtype))
       right1.append((Aright1*item1[1]).astype(item1[1].dtype))
       con = con + 1
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
   for item2 in musicData2:
       left2.append((Aleft2*item2[0]).astype(item2[0].dtype))
       right2.append((Aright2*item2[1]).astype(item2[1].dtype))
       con = con + 1
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

   if len(musicData1) > len(musicData2):
       for q1 in range(len(musicData1) - len(musicData2)):
            left2.append(0.0)
            right2.append(0.0)
   elif len(musicData2) > len(musicData1):
       for q2 in range(len(musicData2) - len(musicData1)):
            left1.append(0.0)
            right1.append(0.0)

   l1 = np.array(left1)
   l2 = np.array(left2)
   r1 = np.array(right1)
   r2 = np.array(right2)
   if Mode == 0:
       for i1 in range(len(l1)):
           dte1 = l1[i1] + l2[i1]
           mixed_data1.append(dte1.astype(l1.dtype))
       for i2 in range(len(r1)):
           dte2 = r1[i2] + r2[i2]
           mixed_data2.append(dte2.astype(l1.dtype))
   else:
       for i3 in range(len(l1)):
           dte3 = l1[i3] - l2[i3]
           mixed_data1.append(dte3.astype(l1.dtype))
       for i4 in range(len(r1)):
           dte4 = r1[i4] - r2[i4]
           mixed_data2.append(dte4.astype(l1.dtype))
           
   pygame.display.update()
   mixed_data3 = np.vstack((mixed_data1,mixed_data2)).T
   #mixed_data3 = [list(ite) for ite in zip(mixed_data1,mixed_data2)]
   wavfile.write(desMusicFile, SRate, mixed_data3)
   
# Five Arguments:Input file and output file.
if len(sys.argv)<3:
   print("Argument Error.")
   sys.exit()
a = sys.argv[1]
if len(sys.argv)==3:
   b = str(a) + '_Output.wav'
else:
   b = sys.argv[2]

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  
window = pygame.display.set_mode((window_wid,window_hei)) #,pygame.RESIZABLE
icon = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + r"\Image\Dyde-Mixer-Core.ico") 
pygame.display.set_icon(icon)
pygame.display.set_caption("Dyde Mixer Module")
image1 = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + r"\Image\Dyde-Mixer-Core-Background.bmp")
image2 = pygame.transform.scale(image1,(window_wid,window_hei))
window.blit(image2,(0,0))
pygame.display.flip()
prog_font = pygame.font.Font(os.path.dirname(os.path.realpath(__file__)) + r"\Font\LBRITE.TTF", 26)
prog_text = prog_font.render("Process:%s%%" % str(int(proc)), True, WHITE)
window.blit(prog_text, prog_posi)
pygame.display.update()
# splitChannel(srcMusicFile1,srcMusicFile2,desMusicFile,Aleft1,Aright1,Aleft2,Aright2,SRate,Mode)
splitChannel(str(a),str(b),str(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]),int(sys.argv[8]),int(sys.argv[9]))
print ("Finished." )
pygame.quit()
sys.exit()

# End of source code file of Dyde-Mixer-Core. 
