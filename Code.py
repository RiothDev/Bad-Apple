import os, cv2, fpstimer, sys, screeninfo, math
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from PIL import Image

asciiChars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ","]
asciiImages = []

class sizes:
    def __init__(self, width, height):
        self.Width = int(width)
        self.Height = int(height)

frameCount = 1

cap = None

def main():
    os.system("title Bad apple")

    sys.stdout.write("--------------\n")
    sys.stdout.write("Start\n")
    sys.stdout.write("--------------\n")

    def getSize():
        sizes = [m for m in screeninfo.get_monitors()]
        monitor = 1

        if len(sizes) > 1:
            monitor = input("> Monitor (1 - {}) : ".format(len(sizes)))
        
        return sizes[(int(monitor) - 1)].height, sizes[(int(monitor) - 1)].width
    
    askSize = input("> Use screen sizes? (Y / N) : ")

    if askSize.lower() == "y":
        monitorHeight, monitorWidth = getSize()
    else:
        monitorHeight, monitorWidth = int(input("> Height (190) : ")), int(input("> Width (160) : "))

    def loadMusic(song):
        pygame.mixer.init()
        pygame.mixer.music.load(f"Assets/{song}")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

    def playVideo(totalFrames):
        print("Starting...")
        os.system("cls")

        timer = fpstimer.FPSTimer(30)
        loadMusic("Song.mp3")

        for frame in range(0, totalFrames):
            try:
                #sys.stdout.write("\n\n\n\n")
                sys.stdout.write("\r" + asciiImages[frame])
                sys.stdout.flush()

            except Exception as error:
                print(error)

            timer.sleep()
    
    def loadFrames(totalFrames):
        global frameCount
        global asciiImages
        global cap

        print("Loading frames...")
        r, frm = cap.read()

        while r and frameCount <= totalFrames:
            r, frm = cap.read()
            frameCount += 1

            try:
                img = Image.fromarray(frm)
                asciiImg = transform(img)
                asciiImages.append(asciiImg)

            except Exception as error:
                continue
        
        cap.release()
        playVideo(frameCount)
    
    def getFrames(path):
        checkCap = cv2.VideoCapture(path)
        totalFrames = int(checkCap.get(cv2.CAP_PROP_FRAME_COUNT))

        checkCap.release()

        fpp = totalFrames - 1
        loadFrames(fpp)

    def loadVideo(vid):
        global cap
        cap = cv2.VideoCapture(f"Assets/{vid}")
        getFrames(f"Assets/{vid}")

    def transform(img):
        global mainSizes

        oldWidth, oldHeight = img.size
        oldSizes = sizes(oldWidth, oldHeight)

        ratio = (oldSizes.Height / float(oldSizes.Width * 2.5))

        newSizes = sizes(monitorWidth / 2, math.floor((ratio * float(monitorHeight / 5.5))))
        #print(math.floor((ratio * float(monitorSizes.height / 5.6))))

        img = img.resize((newSizes.Width, newSizes.Height))
        img = img.convert("L")

        pixels = img.getdata()

        newPixels = [asciiChars[pixel // 25] for pixel in pixels]
        newPixels = "".join(newPixels)
        pixelsLen = len(newPixels)

        asciiImage = [newPixels[index:(index + newSizes.Width)] for index in range(0, pixelsLen, newSizes.Width)]
        asciiImage = "\n".join(x for x in asciiImage)

        return asciiImage
    
    loadVideo("Video.mp4")

if __name__ == "__main__":
    main()
