import os, cv2, fpstimer, sys, screeninfo, math, sys, traceback, colorama
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from PIL import Image

ASCII_CHARS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ","]
ASCII_IMAGES = []
TITLE = """
██████╗░░█████╗░██████╗░  ░█████╗░██████╗░██████╗░██╗░░░░░███████╗  ██████╗░██╗░░░██╗
██╔══██╗██╔══██╗██╔══██╗  ██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔════╝  ██╔══██╗╚██╗░██╔╝
██████╦╝███████║██║░░██║  ███████║██████╔╝██████╔╝██║░░░░░█████╗░░  ██████╦╝░╚████╔╝░
██╔══██╗██╔══██║██║░░██║  ██╔══██║██╔═══╝░██╔═══╝░██║░░░░░██╔══╝░░  ██╔══██╗░░╚██╔╝░░
██████╦╝██║░░██║██████╔╝  ██║░░██║██║░░░░░██║░░░░░███████╗███████╗  ██████╦╝░░░██║░░░
╚═════╝░╚═╝░░╚═╝╚═════╝░  ╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░╚══════╝╚══════╝  ╚═════╝░░░░╚═╝░░░

██████╗░██╗░█████╗░████████╗██╗░░██╗██████╗░███████╗██╗░░░██╗
██╔══██╗██║██╔══██╗╚══██╔══╝██║░░██║██╔══██╗██╔════╝██║░░░██║
██████╔╝██║██║░░██║░░░██║░░░███████║██║░░██║█████╗░░╚██╗░██╔╝
██╔══██╗██║██║░░██║░░░██║░░░██╔══██║██║░░██║██╔══╝░░░╚████╔╝░
██║░░██║██║╚█████╔╝░░░██║░░░██║░░██║██████╔╝███████╗░░╚██╔╝░░
╚═╝░░╚═╝╚═╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░╚══════╝░░░╚═╝░░░
"""

class sizes:
    def __init__(self, width, height):
        self.Width = int(width)
        self.Height = int(height)

frame_count = 1

cap = None

def main():
    os.system("title Bad apple")

    print(colorama.Fore.CYAN + TITLE + colorama.Fore.RESET)

    def get_size() -> int:
        screen_sizes = [m for m in screeninfo.get_monitors()]
        monitor = 1

        if len(screen_sizes) > 1: monitor = input(colorama.Fore.BLUE + "> Monitor (1 - {}) : ".format(len(screen_sizes)) + colorama.Fore.CYAN)
        
        return math.floor(screen_sizes[(int(monitor) - 1)].height / 5.5), math.floor(screen_sizes[(int(monitor) - 1)].width / 10)
    
    ask_size = input(colorama.Fore.BLUE + "> Use screen sizes? (Y / N) : " + colorama.Fore.CYAN)

    if ask_size.lower() == "y":
        monitor_height, monitor_width = get_size() 
    else: 
        monitor_height, monitor_width = int(input(colorama.Fore.BLUE + "> Height (190) : " + colorama.Fore.CYAN)), int(input(colorama.Fore.BLUE + "> Width (160) : " + colorama.Fore.CYAN))

    def play_music(song) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(f"Assets/{song}")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

    def play_video(total_frames) -> None:
        print(colorama.Fore.YELLOW + "Starting..." + colorama.Fore.RESET)
        os.system("cls")

        timer = fpstimer.FPSTimer(30)
        play_music("Song.mp3")

        for frame in range(0, total_frames):
            try:
                #sys.stdout.write("\n\n\n\n")
                sys.stdout.write("\r" + ASCII_IMAGES[frame])
                sys.stdout.flush()

            except Exception as error:
                print(error)

            timer.sleep()
    
    def load_frames(total_frames) -> None:
        global frame_count
        global ASCII_IMAGES
        global cap

        print(colorama.Fore.YELLOW + "Loading frames..." + colorama.Fore.RESET)
        r, frm = cap.read()

        while r and frame_count <= total_frames:
            r, frm = cap.read()
            frame_count += 1

            try:
                img = Image.fromarray(frm)
                ASCII_img = transform(img)
                ASCII_IMAGES.append(ASCII_img)

            except Exception as error:
                continue
        
        cap.release()
        play_video(frame_count)
    
    def get_frames(path) -> None:
        check_cap = cv2.VideoCapture(path)
        total_frames = int(check_cap.get(cv2.CAP_PROP_FRAME_COUNT))

        check_cap.release()

        fpp = total_frames - 1
        load_frames(fpp)

    def load_video(vid) -> None:
        global cap
        cap = cv2.VideoCapture(f"Assets/{vid}")
        get_frames(f"Assets/{vid}")

    def transform(img) -> str:
        global main_sizes

        old_width, old_height = img.size
        old_sizes = sizes(old_width, old_height)

        ratio = (old_sizes.Height / float(old_sizes.Width * 2.5))

        new_sizes = sizes(monitor_width, math.floor((ratio * monitor_height)))
        #print(math.floor((ratio * float(monitorSizes.height / 5.6))))

        img = img.resize((new_sizes.Width, new_sizes.Height))
        img = img.convert("L")

        pixels = img.getdata()

        new_pixels = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
        pixels_len = len(new_pixels)

        ASCII_Image = [new_pixels[index:(index + new_sizes.Width)] for index in range(0, pixels_len, new_sizes.Width)]
        ASCII_Image = "\n".join(x for x in ASCII_Image)

        return ASCII_Image
    
    load_video("Video.mp4")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(traceback.format_exc())
        input("")
        sys.exit(-1)
