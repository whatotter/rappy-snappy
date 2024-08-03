import os
import pystray
from PIL import Image, ImageDraw

def menuQuit():
    os.kill(os.getpid(), 1)

def doNothing():
    return

def openSettings():
    os.system("cmd.exe /C \"keys.toml\"")

def ico(width, height, color1, color2):
    """i cannot be assed to make an icon, so i took this from https://pystray.readthedocs.io/en/latest/usage.html"""
    
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

def setupIcon(config):
    sysMenu = pystray.Menu(
        pystray.MenuItem("Settings", pystray.Menu(
                pystray.MenuItem('Open Settings', openSettings),
                pystray.MenuItem('Polling Rate: {}'.format(config["pollingRate"]), doNothing),
                pystray.MenuItem('Listening to keys: {}'.format(config["keys"]), doNothing)
            )
        ), 
        pystray.MenuItem("Quit", menuQuit)
        )

    sysIcon = pystray.Icon(
        'Rappy Snappy', icon=ico(64, 64, 'black', 'white'), menu=sysMenu, title="Rappy Snappy"
    )

    sysIcon.run_detached()