'''
Image to ASCII by Clarence Yang 7/10/2022
can convert an image to ASCII or convert camera feed to ASCII

'w' - increase contrast
's' - decrease contrast
'm' - 'matrix toggle'
'q' - quit
'''

from PIL import Image
import cv2
import math
import curses



class ASCII:
    def __init__(self, stdscr):

        self.const = "Ñ@#W$9876543210?!abc;:+=-,._"

        self.contrast = 5

        self.density = (self.const + (" " * self.contrast))

        self.camera = True
        self.id = 1
        self.stdscr = stdscr

        self.preload()

    # Change contrast 
    def addContrast(self, increase): 
        if increase and self.contrast < 20:
            self.contrast += 1
            
        elif increase == False and self.contrast > 0:
            self.contrast -= 1
            

        self.density = (self.const + (" " * self.contrast))

    # main Loop - will load image 
    def preload(self):
        
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.stdscr.nodelay(True)
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        bwidth = 64
        k=0
        input = cv2.VideoCapture(0)
        self.stdscr.clear()
        while True:

            k = self.stdscr.getch()
            if k == ord('w'):
                self.addContrast(False)
            elif k == ord('s'):
                self.addContrast(True)
            elif k == ord('q'):
                break
            elif k == ord('m'):
                if self.id == 1:
                    self.id = 2
                else:
                    self.id = 1

            if self.camera:
                ret, Frame = input.read()
                c = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(c)
            else:     
                img = Image.open("test.jpg", 'r')
            
            wpercent = (bwidth/float(img.size[0]))
            hsize = int(float(img.size[1])*float(wpercent))
            img = img.resize((bwidth, hsize), Image.ANTIALIAS)
            width, height = img.size
            #img.show()
            self.stdscr.addstr(0,0,f"CONTRAST: {self.contrast}", curses.color_pair(self.id))
            self.draw(width, height, list(img.getdata()))

    def translate (self, val, min1, max1, min2, max2):
        lS = max1 - min1
        rS = max2 - min2
        scaled = float(val-min1)/float(lS)
        return min2 + scaled*rS

    def draw(self, w, h, img):
        self.stdscr.refresh()
        
        for i in range(h):
            text = ""
            for j in range(w):
                RGB = img[w*i+j]
                R = RGB[0]
                G = RGB[1]
                B = RGB[2]
                #print(RGB)
                avg = (R+G+B)/3
                charind = math.floor(self.translate(avg, 0, 255, len(self.density)-1, 0))
                text += f" {self.density[charind]}" 
            
            try:
                self.stdscr.addstr(i+1,0,text, curses.color_pair(self.id))
            except:
                pass
    
    
def main(stdscr):
    ASCII(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)