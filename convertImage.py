import PIL
import os

def change_DPI():

    files = os.listdir(r'.\Images')
    print files
    for f in files:
        if f.endswith(('.jpg', '.png')):
            path_name = os.path.join()
change_DPI()
