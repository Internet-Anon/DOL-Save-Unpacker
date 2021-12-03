import tkinter as tk
from tkinter import filedialog
from tkinter.constants import *
from lzstring import LZString as lz
import json
import os

dataDir = os.getenv("LOCALAPPDATA") + "\DOLUnpacker\\"
dataFile = dataDir + "default.json"

def openfile():
    if os.path.exists(dataFile):
        f = open(dataFile, "r")
        jsonContent = f.read()
        initdir= json.loads(jsonContent)
    else:
        initdir = "/"
    file = filedialog.askopenfilename(initialdir= initdir, title="Select File", filetypes=(("Save Files", "*.save"),("Json Files", "*.json"),("All Files","*.*")))
    entry.delete(0,END)
    entry.insert(0,file)

def opendir():
    dir = filedialog.askdirectory(initialdir='/', title="Select Folder")
    if not os.path.exists(dataDir):
        os.mkdir(dataDir)
    jsonString = json.dumps(dir)
    f = open(dataFile, "w+")
    f.write(jsonString)
    f.close()    

def unpack():
    path = entry.get()
    newfile = path.rsplit(".", 1)
    newfile = (newfile[0] + ".json")
    packed_file = open(path, "r").read()
    unpacked_file = lz.decompressFromBase64(packed_file)
    f = open(newfile, "w+")
    f.write(unpacked_file)
    f.close()

def repack():
    path = entry.get()
    newfile = path.rsplit(".", 1)
    newfile = (newfile[0] + ".save")
    unpacked_file = open(path, "r").read()
    encoded_file = lz.compressToBase64(unpacked_file)
    f = open(newfile, "w+")
    f.write(encoded_file)
    f.close()



#GUI
window = tk.Tk()

#Base64 Icon
icon = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAGJUExURUdwTM5+RYZPI4BVKoRNH4lQIwAAAHU7H6xoMo1SI
        nlRG4ZMIYNGIa5oNJdaLKtnNK5qNo5VHMJ3QKdkMZ1cMJ5dLqBfLaJgMqRfMJhYKYdQKNGvo6FhM6tkNJRVJ4tGF8B4QZ1cLaliM5FUJ5ZWKPbXxuPBs5NWJ4xSJKhiNJlZKPrp3
        9Krmb2qpKBdLdGom927oo9SI7qHZJpaKbiWiruhmYlRIpVbNtqHTP/u4rVpOqhiMr9xP61jM7FnN7hrO7ttPptbK89+RumaVteFSL90PadbHN2PSKVYHLN1S6ZgMuO7n+3j3P/s34
        NOI/3p3ZRXKadjNOCPUOOTUsh6Qs59QPCiWsh3O7ZmKrh1Oo9NGMJ2Qp9YJrhqOrBkLtvSz694UpBSIOCUU7CFaNikhKdoOq9ySfHby6OZlHR4f6FvRp9TFpVTIP7o15t7ZqmHbY2
        YqODEruXEr7K3wC5ejfrNsODi5s+omPTazSJSgb29whxOfvLTxfzk1b+Ma8PEyfPj2+Hm63iNotY+v8UAAAA4dFJOUwD8PQYhfQEEtkkJKhexXbrGEu+WdaXC/rPoRln8+HUL++r0
        vIX1kPSx4p7s9q7OOP6Y1P1r/av8OyD8ogAAAOZJREFUGBk1wIWWglAUBdCjggzqdHd3N/chpWKP6HR3d3d/ubhcbtjczuIiW4kXeVypQ8oJVFR6YHOXBeelPLPaBUB0SAtLy6FwM
        BLZaGsAULMYWlldM/374XVlq90Drj4eiJrb5zLbPdrUO1ohMtkfvUjdxGMnB6ra6YLIZO0y9f94fUene0oXIDJZ0xN/Hw9EZ4bWAvj6FZah57d3otvjZh+AEd3I0O+PRbQTqxMA9K
        ks/fJlvVpzidoq2Jy9k0b6+/N+7LCJL0cO5x2fmX2a4Ad4AQVT01dDw6MoEHoGk0TJ7kbYsoQUMAKQPM6bAAAAAElFTkSuQmCC"""

#Magic Icon Fuckery
icon = tk.PhotoImage(data=icon)
window.tk.call("wm", "iconphoto", window._w, icon)

window.title("DoL Save Unpacker")

#Forced Sizing
xOffset = 2
yOffset = 32

xSize = 280
ySize = 100

xReal = xSize - xOffset
yReal = ySize - yOffset

window.geometry(str(xReal) + "x" + str(yReal))
window.minsize(xReal,yReal)
window.maxsize(xReal,yReal)

#Grid Borders
window.columnconfigure([0,1,2], minsize= 5)
window.rowconfigure([0,1], minsize= 30)

#GUI Elements
menu = tk.Menu(window)
menu.add_command(label= "Set Default Folder", command= opendir)

window.config(menu= menu)

entry = tk.Entry(window, width=30)
entry.grid(row=0, column=0, columnspan= 2)

fileButton = tk.Button(window, text= "Select Save", width=10, command=openfile)
fileButton.grid(row=0, column=3, sticky=W)

unpackButton = tk.Button(window, text= "Unpack Save", width=10, command=unpack)
unpackButton.grid(row=1, column=0, sticky=N)

repackButton = tk.Button(window, text= "Repack Save", width=10, command=repack)
repackButton.grid(row=1, column=1, sticky=NW)


window.mainloop()

