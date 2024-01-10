from copyreg import constructor
from genericpath import isfile
from mimetypes import init
import tkinter as tk
from tkinter import Frame, Label, filedialog
from tkinter.constants import *
from lzstring import LZString as lz
import math
import base64
import json
import os
def main():

    # Same algorithm as aimozg's but implimented in python #
    
    class JsonCompressor:
            def constructor(self, wellKnownValues = []):
                self.wellKnownValues = wellKnownValues
                next = 0
                for wkv in self.wellKnownValues:
                    id = next + 1 
                    val2idx = map(self, wkv, id)

                self.initial_val2idx = val2idx

            def get(self, value):
                if value in self.val2idx:
                    return value
                id = self.next + 1
                self.val2idx(self, value, id)
                self.idx2val.append(value)
            
            def compress1(self, obj):
                    if type(obj) == int:
                        if not math.isfinite(obj) | obj < 0 | math.floor(obj) != obj:
                            return obj
                        return self.get(obj)
                    if type(obj) == str | type(obj) == bool | type(obj) == None:
                        return self.get(obj)
                    if type(obj) != object:
                        return obj
                    if type(obj) == list:
                        if len(obj) == 0:
                            return []
                        return [0, self.compress1(obj)]
                    result = [1]
                    for [k, v] in object:
                        k = self.get(k)
                        result.append(k)
                        v = self.compress1(v)
                        result.append(v)
                    return result
                    
            def reset(self):
                self.val2idx = map(self.initial_val2idx)
                self.idx2val = []
                self.next = len(self.val2idx)
            
            def compress(self, obj):
                self.reset()
                data = self.compress1(obj)
                return "{ compressed :1, \
                values:" + self.idx2val + data + "}"
        
    class JsonDecompressor:
        def constructor(self, wellKnownValues = []):
            self.wellKnownValues = wellKnownValues
        
        def decompress1(self, obj):
            if type(obj) == int:
                if math.isfinite(obj) and obj >= 0 and math.floor(obj) == obj and obj < len(self.idx2val):
                    return self.idx2val[obj]
            if type(obj) == str and obj in self.idx2val:
                return self.idx2val[obj]
            if type(obj) == object and obj != None:
                if type(obj) == list:
                    if len(obj) == 0:
                        return []
                    if obj[0] == 0:
                        i = 1
                        result = list(len(obj) - 1)
                        while i < len(obj): 
                            result[i - 1] = self.decompress1(obj[i])
                            i += 1
                        return result
                    elif obj[0] == 1:
                        i = 1
                        result = {}
                        while i < len(obj):
                            k = self.decompress1(obj[i])
                            i += 1
                            v = self.decompress1(obj[i])
                            i += 1
                            result[k] = v
                        
                        return result
                return obj
            return obj
        def decompress(self, obj):
            if  JsonCompressor.isCompressed(obj) == True:
                self.idx2val = [self.wellKnownValues, obj]
            elif JsonCompressor.isCompressed(obj) == False:
                print("Not a valid compressed object")
                return
        
        







    dataDir = os.getenv("LOCALAPPDATA") + "\DOLUnpacker\\"
    dataFile = dataDir + "default.json"


    if not os.path.exists(dataDir):
        os.mkdir(dataDir)
        configdata = {"dir" : "None", "mode" : 1}
        jsonString = json.dumps(configdata)
        f = open(dataFile, "w")
        f.write(jsonString)
        f.close()

    elif not os.path.exists(dataFile):
        configdata = {"dir" : "None", "mode" : 1}
        jsonString = json.dumps(configdata)
        f = open(dataFile, "w")
        f.write(jsonString)
        f.close()
    else:
        with open(dataFile, "r") as filedata:
            data = json.loads(filedata.read())

    def openfile():
        config = data
        if config["dir"] != "None":
            initdir = config["dir"]
        else:
            initdir = "/"
        file = filedialog.askopenfilename(initialdir= initdir, title="Select File", filetypes=(("Save Files", "*.save"),("Json Files", "*.json"),("All Files","*.*")))
        entry.delete(0,END)
        entry.insert(0,file)

    def opendir():
        dir = filedialog.askdirectory(initialdir='/', title="Select Folder")
        config = data
        config["dir"] = dir
        jsonString = json.dumps(config)
        f = open(dataFile, "w+")
        f.write(jsonString)
        f.close() 
    

    def unpack():
        path = entry.get()
        newfile = path.rsplit(".", 1)
        newfile = (newfile[0] + ".json")
        packed_file = open(path, "r").read()
        decompressed_file = lz.decompressFromBase64(packed_file + "===")
        
        
        f = open(newfile, "w+", encoding="UTF-8")

        f.write(decompressed_file)
        f.close()

    def repack():
        path = entry.get()
        newfile = path.rsplit(".", 1)
        newfile = (newfile[0] + ".save")
        unpacked_file = open(path, "r", errors="ignore").read()
        encoded_file = lz.compressToBase64(unpacked_file)
        f = open(newfile, "w+")
        f.write(encoded_file)
        f.close()

    def movewindow(move):
        window.geometry(f"+{move.x_root}+{move.y_root}")

    def exit(e):
        window.destroy()
    

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
    #icon = tk.PhotoImage(data=icon)
    #window.tk.call("wm", "iconphoto", window._w, icon)

    window.overrideredirect(True)
    #Forced Sizing
    xOffset = 2
    yOffset = 32

    xSize = 300
    ySize = 105

    window.geometry(str(xSize) + "x" + str(ySize) + "+" + str(xOffset) + "+" + str(yOffset))

    if data["mode"] == 0:

        windowbg = "#fefefe"
        titlebg = "#b0aca4"
        buttonbg = "#cbcac4"
        borderbg = "#b2b0a8"
        themefg = "#000000"
        window.config(bg=windowbg)

        titlebar = Frame(window, bg=titlebg, bd=0)
        titlebar.pack(expand=1, fill=X)
        titlebar.bind("<B1-Motion>", movewindow)

        title = Label(titlebar, text="DOL Save Unpacker", bg=titlebg, fg=themefg)
        title.pack(side=LEFT)
        title.bind("<B1-Motion>", movewindow)

        close = Label(titlebar, text="  X  ", bg=titlebg, fg=themefg)
        close.pack(side=RIGHT)
        close.bind("<Button-1>", exit)
        
        MenuFrame = Frame(window, bg=titlebg, height=25)
        MenuFrame.pack(expand=1, fill=X)
        MenuFrame.pack_propagate(False)
        MenuBorder = Frame(MenuFrame, bg=windowbg, height=2)
        MenuBorder.pack(expand=1, fill=X)
        TopFrame = Frame(window, bg=windowbg)
        TopFrame.pack(expand=1, fill=X)
        BottomFrame = Frame(window, bg=windowbg)
        BottomFrame.pack(expand=1, fill=X, pady=5)

        dirButton = tk.Button(MenuFrame, height=10, text="Change Default Folder", bg=buttonbg, fg=themefg, command=opendir)
        dirButton.pack(side=LEFT)

        entry = tk.Entry(TopFrame, width=35, bg=titlebg, fg=themefg, insertbackground=themefg)
        entry.pack(side=LEFT, padx=7)

        fileButton = tk.Button(TopFrame, text= "Select Save", width=10, command=openfile, bg=buttonbg, fg=themefg)
        fileButton.pack()

        unpackButton = tk.Button(BottomFrame, text= "Unpack Save", width=10, command=unpack, bg=buttonbg, fg=themefg)
        unpackButton.pack(side= LEFT, padx=35)

        repackButton = tk.Button(BottomFrame, text= "Repack Save", width=10, command=repack, bg=buttonbg, fg=themefg)
        repackButton.pack()

        window.mainloop()
    
    elif data["mode"] == 1:

        windowbg = "#454545"
        titlebg = "#4f535b"
        buttonbg = "#34353b"
        borderbg = "#4d4f57"
        themefg = "#ffffff"
        window.config(bg=windowbg)

        titlebar = Frame(window, bg=titlebg, bd=0)
        titlebar.pack(expand=1, fill=X)
        titlebar.bind("<B1-Motion>", movewindow)

        title = Label(titlebar, text="DOL Save Unpacker", bg=titlebg, fg=themefg)
        title.pack(side=LEFT)
        title.bind("<B1-Motion>", movewindow)

        close = Label(titlebar, text="  X  ", bg=titlebg, fg=themefg)
        close.pack(side=RIGHT)
        close.bind("<Button-1>", exit)

        MenuFrame = Frame(window, bg=titlebg, height=25)
        MenuFrame.pack(expand=1, fill=X)
        MenuFrame.pack_propagate(False)
        MenuBorder = Frame(MenuFrame, bg=borderbg, height=2)
        MenuBorder.pack(expand=1, fill=X)
        TopFrame = Frame(window, bg=windowbg)
        TopFrame.pack(expand=1, fill=X)
        BottomFrame = Frame(window, bg=windowbg)
        BottomFrame.pack(expand=1, fill=X, pady=5)

        dirButton = tk.Button(MenuFrame, height=10, text="Change Default Folder", bg=buttonbg, fg=themefg, command=opendir)
        dirButton.pack(side=LEFT)

        entry = tk.Entry(TopFrame, width=35, bg=titlebg, fg=themefg, insertbackground=themefg)
        entry.pack(side=LEFT, padx=7)

        fileButton = tk.Button(TopFrame, text= "Select Save", width=10, command=openfile, bg=buttonbg, fg=themefg)
        fileButton.pack()

        unpackButton = tk.Button(BottomFrame, text= "Unpack Save", width=10, command=unpack, bg=buttonbg, fg=themefg)
        unpackButton.pack(side= LEFT, padx=35)

        repackButton = tk.Button(BottomFrame, text= "Repack Save", width=10, command=repack, bg=buttonbg, fg=themefg)
        repackButton.pack()

        window.mainloop()

main()