import os, cv2, fpstimer, sys
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
frameSize = 180

cap = None

def main():
    os.system("title Bad apple")

    sys.stdout.write("--------------\n")
    sys.stdout.write("Start\n")
    sys.stdout.write("--------------\n")

    input()

    def loadMusic(song):
        pygame.mixer.init()
        pygame.mixer.music.load(f"Assets/{song}")
        pygame.mixer.music.play()

    def playVideo(totalFrames):
        print("Starting...")
        os.system("cls")

        timer = fpstimer.FPSTimer(30)
        loadMusic("Song.mp3")

        for frame in range(0, totalFrames):
            sys.stdout.write("\r" + asciiImages[frame])
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

        newSizes = sizes(frameSize, (ratio * frameSize))

        img = img.resize((newSizes.Width, newSizes.Height))
        img = img.convert("L")

        pixels = img.getdata()

        newPixels = [asciiChars[pixel // 25] for pixel in pixels]
        newPixels = "".join(newPixels)
        pixelsLen = len(newPixels)

        asciiImage = [newPixels[index:index + newSizes.Width] for index in range(0, pixelsLen, newSizes.Width)]
        asciiImage = "\n".join(asciiImage)

        return asciiImage
    
    loadVideo("Video.mp4")

if __name__ == "__main__":
    main()