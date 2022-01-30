# Copyright (c) 2020-2022 Qilu University of Technology, College of Computer Science And Technology,Duyu No.202103180009
# Dyde-Gain-Core.py
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
       
def splitChannel(srcMusicFile,desMusicFile,Aleft,Aright,SRate): # SRate=0 means default.
   # read wav file
   sampleRate, musicData = wavfile.read(srcMusicFile)
   if Aleft == 0:
      Aleft = 1
   if Aright == 0:
      Aright = 1
   if SRate == 0:
      SRate= sampleRate
   left = []
   right = []
   global count
   count = len(musicData)
   pygame.display.update()
   global con
   global proc
   global WHITE
   SECOND = threading.Thread(target=upnew, daemon=True).start()

   for item in musicData:
       left.append((Aleft*item[0]).astype(item[0].dtype))
       right.append((Aright*item[1]).astype(item[1].dtype))
       #(Aleft*item[0]).astype(item[0].dtype)
       #
       con = con + 1
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
       
   mixed_data1 = np.array(left)
   mixed_data2 = np.array(right)
   pygame.display.update()
   mixed_data3 = np.vstack((mixed_data1,mixed_data2)).T
   #mixed_data3 = [list(ite) for ite in zip(mixed_data1,mixed_data2)]
   wavfile.write(desMusicFile, SRate, mixed_data3)
   
# Five Arguments:Input file and output file.
if len(sys.argv)<2:
   print("Argument Error.")
   sys.exit()
a = sys.argv[1]
if len(sys.argv)==2:
   b = str(a) + '_Output.wav'
else:
   b = sys.argv[2]

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  
window = pygame.display.set_mode((window_wid,window_hei)) #,pygame.RESIZABLE
icon = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + r"\Image\Dyde-Gain-Core.ico") 
pygame.display.set_icon(icon)
pygame.display.set_caption("Dyde Sound-Gain Module")
image1 = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + r"\Image\Dyde-Mixer-Core-Background.bmp")
image2 = pygame.transform.scale(image1,(window_wid,window_hei))
window.blit(image2,(0,0))
pygame.display.flip()
prog_font = pygame.font.Font(os.path.dirname(os.path.realpath(__file__)) + r"\Font\LBRITE.TTF", 26)
prog_text = prog_font.render("Process:%s%%" % str(int(proc)), True, WHITE)
window.blit(prog_text, prog_posi)
pygame.display.update()

splitChannel(str(a),str(b),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]))
print ("Finished." )
pygame.quit()
sys.exit()

# End of source code file of Dyde-Gain-Core. 
