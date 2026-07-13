"""

Hi, Im Calak de Astora thank you to download this repo!

Author: https://github.com/elcalak
OG Repo: https://github.com/elcalak/Waving-CLI-Player

Waving is a music player based on Textual for creating menus 
and on miniaudio to process audio files, supports wav, mp3 and ogg.

The player searches in /home/Music and, if the folder doesnt exist creates it.
If you dont have any files or folder here, you will be notified.

You can navigate through the menus using keyboard Arrows and Enter to select file or folder.

If you selected a folder, browse within this folder.

If selected a file, add it to a playlist; if you then want to select another file,
that file will be placed next in the playlist.

to build the project you can install all dependencies with pip install -r requirements.txt

"""

import sys #Import system library to close the binary
from time import sleep #From time import sleep to pause
from rich.console import Console #Import Console from rich.console to clear and print with style
import textual_apps as ta #Call textual_app.py

console = Console() #Create a object console to style prints and inputs
console.clear() #Clear the console with rich library

title = r"""

 ██████╗ █████╗ ██╗      █████╗ ██╗  ██╗    ██████╗ ███████╗     █████╗ ███████╗████████╗ ██████╗ ██████╗  █████╗ 
██╔════╝██╔══██╗██║     ██╔══██╗██║ ██╔╝    ██╔══██╗██╔════╝    ██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗
██║     ███████║██║     ███████║█████╔╝     ██║  ██║█████╗      ███████║███████╗   ██║   ██║   ██║██████╔╝███████║
██║     ██╔══██║██║     ██╔══██║██╔═██╗     ██║  ██║██╔══╝      ██╔══██║╚════██║   ██║   ██║   ██║██╔══██╗██╔══██║
╚██████╗██║  ██║███████╗██║  ██║██║  ██╗    ██████╔╝███████╗    ██║  ██║███████║   ██║   ╚██████╔╝██║  ██║██║  ██║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

""" #Title ascii art

console.rule(title = "Development by: ", characters = "=") #Print rule with rich library
console.print(title, style="bold blue", justify="center") #Print title with rich style
console.rule(title = "Christopher G. Linares", characters = "=") #Print rule with rich library

sleep(0.25)

console = Console() #Create a object console to style prints and inputs
console.clear() #Clear the console with rich library

title = r"""

 __        __     ________  ________   ______  
|  \      |  \   |        \|        \ /      \ 
| $$      | $$    \$$$$$$$$| $$$$$$$$|  $$$$$$\
| $$      | $$      | $$   | $$__    | $$___\$$
| $$      | $$      | $$   | $$  \    \$$    \ 
| $$      | $$      | $$   | $$$$$    _\$$$$$$\
| $$_____ | $$_____ | $$   | $$      |  \__| $$
| $$     \| $$     \| $$   | $$       \$$    $$
 \$$$$$$$$ \$$$$$$$$ \$$    \$$        \$$$$$$               

""" #Title ascii art

console.rule(title = "LONG LIVE TO FREE SOFTWARE", characters = "=") #Print rule with rich library
console.print(title, style="bold blue", justify="center") #Print title with rich style
console.rule(title = "LONG LIVE TO FREE SOFTWARE", characters = "=") #Print rule with rich library

sleep(0.25)

app = ta.TableApp() #Create a TableApp object

while True: #Start function main

    app.run() #Run the app

    console = Console() #Create a object console to style prints and inputs
    console.clear() #Clear the console with rich library

    title_menu = r"""

__/\\\______________/\\\_______________________________________________________________        
 _\/\\\_____________\/\\\_______________________________________________________________       
  _\/\\\_____________\/\\\_______________________________/\\\_________________/\\\\\\\\__      
   _\//\\\____/\\\____/\\\___/\\\\\\\\\_____/\\\____/\\\_\///___/\\/\\\\\\____/\\\////\\\_     
    __\//\\\__/\\\\\__/\\\___\////////\\\___\//\\\__/\\\___/\\\_\/\\\////\\\__\//\\\\\\\\\_    
     ___\//\\\/\\\/\\\/\\\______/\\\\\\\\\\___\//\\\/\\\___\/\\\_\/\\\__\//\\\__\///////\\\_   
      ____\//\\\\\\//\\\\\______/\\\/////\\\____\//\\\\\____\/\\\_\/\\\___\/\\\__/\\_____\\\_  
       _____\//\\\__\//\\\______\//\\\\\\\\/\\____\//\\\_____\/\\\_\/\\\___\/\\\_\//\\\\\\\\__ 
        ______\///____\///________\////////\//______\///______\///__\///____\///___\////////___

""" #Title Menu ascii art

    console.rule(title = "You used: ", style = "bold blue") #Print rule with rich library
    console.print(title_menu, style = "bold white", justify = "center") #Print title with rich style
    #Print rule with rich library
    console.rule(title = "Development by: Calak de Astora", style = "bold blue")

    sleep(0.25) #Sleep a moment

    console = Console() #Create a object console to style prints and inputs
    console.clear() #Clear the console with rich library

    sys.exit(0) #Close the program

#Start fucntion main

#End of the program

#Thank you for read, contribute, use and share! Att: Calak De Astora
#LLTFS (LONG LIVE TO FREE SOFTWARE)
