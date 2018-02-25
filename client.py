#!/usr/bin/env python 3.6
# Version 0.2.2 - by TianqiW

# This version of the program cannot launch fresh-start game due to some mysterious reasons
# modern original versions and optiFine versions are tested to be successfully launched
# forge versions are not yet to be tested

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import re
import datetime
import os
import json
import sys
import urllib.request


# main class of the launcher
class App:
    def __init__(self):
        # initialization of the root and configuration windows
        self.root = Tk()
        self.config = Tk()
        self.__alreadyconfig = False
        self.config.withdraw()
        self.root.title('Minecraft Launcher')
        self.root.geometry('720x450')
        self.root.resizable(FALSE, FALSE)
        self.root.attributes('-alpha', 0.95)
        self.root.protocol('WM_DELETE_WINDOW', self.closeall)
        self.config.protocol('WM_DELETE_WINDOW', self.config.withdraw)
        self.config.resizable(FALSE, FALSE)
        self.config.title('Launcher Config')
        self.config.geometry('380x250')

        # initialization of config variables
        self.close = IntVar(self.config)
        self.folderpath = StringVar(self.config)
        self.javapath = StringVar(self.config)
        self.user = StringVar(self.config)
        self.version = StringVar(self.config)
        self.maxmemory = StringVar(self.config)
        self.minmemory = StringVar(self.config)
        self.height = StringVar(self.config)
        self.width = StringVar(self.config)
        # default value
        self.close.set(1)
        self.user.set('Player')
        self.folderpath.set(os.getcwd().replace("\\", '/')+'/.minecraft')
        self.javapath.set('Default')
        self.maxmemory.set('2048')
        self.minmemory.set('512')
        self.version.set(self.findversion())
        self.height.set('768')
        self.width.set('1024')
        # initialization of menu bar
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Run", command=self.run)
        filemenu.add_command(label="Setup", command=self.configminecraft)
        filemenu.add_command(label="Save", command=self.saveconfig)
        filemenu.add_command(label="Export BAT", command=self.exportbat)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Main", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.showabout)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

        # initialization of the background for the main interface
        self.background = Canvas(self.root, width=720, height=450, bg='lightgrey')
        self.background.pack()

        try:
            self.bgimage = PhotoImage(file='background.gif')
            self.background.create_image(0,0,image=self.bgimage, anchor=NW)
        except:
            self.background.config(bg='lightblue')
        # start button
        startbutton = Button(self.root, text="Craft", command=self.run, height=1, width=9, compound=LEFT,bg='brown',
                             font=('Helvetica_Neue', 20), foreground='#998')
        startbutton.place(relx=0.95, rely=0.95, anchor=SE)

    # the method when executing run instruction or being hit the start button
    def run(self):
        if self.close.get():
            self.closeall()

        execute_cmd(rungame(self.user.get(),self.folderpath.get(),self.javapath.get(),self.maxmemory.get(),self.minmemory.get(),
                self.version.get(),self.width.get(),self.height.get()))

    # as the name of the method, just for testing
    def donothing(self):
        pass

    # the method is invoked when the About in the menu is clicked
    def showabout(self):
        messagebox.showinfo("About", "A Minecraft launcher\n version-0.2.0",)

    # the method is invoked when the Setup in the menu is clicked
    def configminecraft(self):
        # if the the config window has already been inited, the program will not re-init it
        if self.__alreadyconfig:
            self.config.deiconify()
        else:
            self.__alreadyconfig = True
            self.config.deiconify()

            try:
                # loading config from the config file (if exists)
                self.configfile = open("launcher.cfg", 'r+')
                config = self.configfile.read()
                #print(config)
                user = re.search("(?<=user=).*", config)
                gamefoler = re.search("(?<=gameFolder=).*", config)
                javapath = re.search("(?<=javaPath=).*", config)
                maxmemory = re.search("(?<=maxMemory=).*", config)
                minmemory = re.search("(?<=minMemory=).*", config)
                version = re.search("(?<=version=).*", config)
                width = re.search("(?<=width=).*", config)
                height = re.search("(?<=height=).*", config)

                self.modifytime = re.search("(?<=modifyTime=).*", config)  # this is useless now

                if gamefoler:
                    self.folderpath.set(gamefoler.group(0))
                if user:
                    self.user.set(user.group(0))
                if javapath:
                    self.javapath.set(javapath.group(0))
                if maxmemory:
                    self.maxmemory.set(maxmemory.group(0))
                if minmemory:
                    self.minmemory.set(minmemory.group(0))
                if version:
                    self.version.set(version.group(0))
                if height:
                    self.height.set(height.group(0))
                if width:
                    self.width.set(width.group(0))

                self.configfile.close()

            except FileNotFoundError:
                pass

            # initialization of the labels at the start of each entry
            Label(self.config, text="Username").grid(row=0, sticky=W)
            Label(self.config, text="Game folder path").grid(row=1, sticky=W)
            Label(self.config, text="Java path").grid(row=2, sticky=W)
            Label(self.config, text="Max-Memory(M)").grid(row=3, sticky=W)
            Label(self.config, text="Min-Memory(M)").grid(row=4, sticky=W)
            Label(self.config, text="Version").grid(row=5, sticky=W)
            Label(self.config, text="Width").grid(row=6, sticky=W)
            Label(self.config, text="Height").grid(row=7, sticky=W)
            # initialization of the buttons for looking path and listing versions
            Button(self.config, text="Find", command=self.findminecraft, height=1, width=6, compound=LEFT).grid(row=1, column=3, sticky=W, padx=11)
            Button(self.config, text="Find", command=self.findjava, height=1, width=6, compound=LEFT).grid(row=2, column=3, sticky=W, padx=11)
            Button(self.config, text="List", command=self.listversion, height=1, width=6, compound=LEFT).grid(row=5, column=3, sticky=W, padx=11)
            # the entries that following the labels
            Entry(self.config, textvariable=self.user, width=30).grid(column=1, row=0, sticky=W)
            Entry(self.config, textvariable=self.folderpath, width=30).grid(column=1, row=1, sticky=W)
            Entry(self.config, textvariable=self.javapath, width=30).grid(column=1, row=2, sticky=W)
            Entry(self.config, textvariable=self.maxmemory, width=12).grid(column=1, row=3, sticky=W)
            Entry(self.config, textvariable=self.minmemory, width=12).grid(column=1, row=4, sticky=W)
            Entry(self.config, textvariable=self.version, width=30).grid(column=1, row=5, sticky=W)
            Entry(self.config, textvariable=self.width, width=12).grid(column=1, row=6, sticky=W)
            Entry(self.config, textvariable=self.height, width=12).grid(column=1, row=7, sticky=W)
            # the button that will close the config window
            configbutton = Button(self.config, text="Done!", command=self.configdone, height=1, width=5, compound=LEFT,bg='White',
                                 font=('Helvetica_Neue', 10), foreground='#998')
            configbutton.place(relx=0.95, rely=0.95, anchor=SE)
            # If the check box is selected (by default), the launcher will close after launching the game.
            Checkbutton(self.config, text="Close after launch", variable=self.close, offvalue=0, onvalue=1).grid(row=9, sticky=W)

        self.config.mainloop()

    def findminecraft(self):  # folder selector for looking for .minecraft folder
        self.folderpath.set(filedialog.askdirectory(initialdir="/", title="Select .minecraft Folder"))
        self.version.set(self.findversion())

    def findjava(self):  # file selector for looking for javaw executable (useless for now)
        self.javapath.set(filedialog.askopenfilename(initialdir="/", title="Select Java", filetypes=(("executable files", "*.exe"), ("all files", "*.*"))))

    def findversion(self):  # will try to find all versions which are available in the dir and return the latest one
        try:
            self.versions = os.listdir(self.folderpath.get() + '/versions/')
            self.versions.sort(reverse=True)
            version = self.versions[0]
        except FileNotFoundError:
            version = None
        return version

    def listversion(self):  # list all versions which are available in the dir with a info message box
        ver = self.findversion()
        if ver:
            v = ''
            for i in self.versions:
                v = v + i + '\n'
            messagebox.showinfo("Available versions on current dir", v)
        else:
            messagebox.showerror("No Version Found", "No version is available in this dir!", )

    def configdone(self):  # close the config window if this method is called
        self.config.withdraw()

    # save the config at present to the config file
    # this method is called when clicking save in the menu or closing the main window
    def saveconfig(self):
        newconfig = "user=%s\ngameFolder=%s\njavaPath=%s\nmaxMemory=%s\nminMemory=%s\nversion=%s\nwidth=%s\nheight=%s\nmodifyTime=%s\n"\
                    % (self.user.get(),
                       self.folderpath.get(),
                       self.javapath.get(),
                       self.maxmemory.get(),
                       self.minmemory.get(),
                       self.version.get(),
                       self.width.get(),
                       self.height.get(),
                       datetime.time())

        self.configfile = open("launcher.cfg", 'w')
        self.configfile.write(newconfig)
        self.configfile.close()

    # this method will output the script for launching the game
    def exportbat(self):
        cmd = rungame(self.user.get(), self.folderpath.get(), self.javapath.get(), self.maxmemory.get(), self.minmemory.get(),
                self.version.get(), self.width.get(), self.height.get())

        a = open("launcher.bat", "w")
        a.write(cmd)
        a.close()

        messagebox.showinfo("Export", "Successfully generate launcher.bat!")  # a feedback message box

    # this method is called when the main window is closed
    def closeall(self):
        self.saveconfig()
        self.root.destroy()
        self.config.destroy()


# combine the jar information
def getJars(gamefolder, version):
    jsonFilePath = gamefolder + '/versions/' + version + '/' + version + '.json'

    with open(jsonFilePath, 'r') as jsonFile:
        jsonFileContent = jsonFile.read()

    jsonFileKeys = json.loads(jsonFileContent)

    jars = ''
    for x in jsonFileKeys['libraries']:
        jarFileParts = x['name'].split(':')
        jarFile = gamefolder + '/libraries/' + \
                  jarFileParts[0].replace('.', '/') + '/' + jarFileParts[1] + '/' + jarFileParts[2] + '/' + \
                  jarFileParts[1] + '-' + jarFileParts[2] + '.jar'

        jars += jarFile + ';'

    if 'inheritsFrom' in jsonFileKeys.keys():
        jars += getJars(gamefolder, jsonFileKeys['inheritsFrom'])

    return jars


# generate the Minecraft Argvs from the json file
def getMinecraftArgvs(gamefolder, version, ID):
    jsonFilePath = gamefolder + '/versions/' + version + '/' + version + '.json'
    with open(jsonFilePath, 'r') as jsonFile:
        jsonFileContent = jsonFile.read()

    jsonFileKeys = json.loads(jsonFileContent)
    argvs = jsonFileKeys['minecraftArguments']
    argvs = argvs.replace('${auth_player_name}', ID) \
        .replace('${version_name}', '{}') \
        .replace('${game_directory}', gamefolder) \
        .replace('${assets_root}', gamefolder + '/assets') \
        .replace('${assets_index_name}', jsonFileKeys['assets']) \
        .replace('${auth_uuid}', '{}') \
        .replace('${auth_access_token}', '{}') \
        .replace('${user_type}', 'Legacy') \
        .replace('${version_type}', jsonFileKeys['type']) \
        .replace('${user_properties}', '{}')
    argvs = jsonFileKeys['mainClass'] + ' ' + argvs

    return argvs


# rungame() actually does run the game but check, combine and return the script for launching
def rungame(player, gamefolder, java, maxm, minm, version, width, height):
    # process argvs for this script
    if player == '':  # if do not specify a ID, print the usage and exit
        messagebox.showerror("Error", "A Username must be given!",)
        sys.exit()

    if version == '':  # if do not specify a version, set the Version value to the latest version
        versions = os.listdir(gamefolder + '/versions/')  # FIXME:file may not found here..
        versions.sort(reverse=True)
        version = versions[0]
        print(versions)

    # generate command to launch Minecraft
    before = 'java -XX:-UseAdaptiveSizePolicy -XX:-OmitStackTraceInFastThrow -Xmn' + minm + 'm' + ' -Xmx' + maxm + 'm -Djava.library.path=' + gamefolder + '/versions/' + version + '/' + version + '-natives "-Dminecraft.launcher.brand=PY Minecraft Launcher" -Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true -Duser.home=/ -cp '

    after = getMinecraftArgvs(gamefolder, version, player)
    after += ' --width %s --height %s' % (width, height)

    jars = getJars(gamefolder, version)
    jars += gamefolder + '/versions/' + version + '/' + version + '.jar '

    cmd = before + jars + after

    return cmd


# invoke the terminal to run the script
def execute_cmd(cmd):
    os.system(cmd)


# authentication for legal user
def authenticate(username, password, clientToken = ""):
    # TODO Not Yet Implement
    url = 'https://authserver.mojang.com/authenticate'
    params = json.dumps({
              "agent": {
                        "name": "Minecraft",
                        "version": 1
                       },
              "username": username,
              "password": password,
              "clientToken": clientToken,
            }).encode()
    header = {'Content-type': 'application/json'}
    req = urllib.request.Request(
        url=url,
        data=params,
        headers=header
    )
    res = json.loads(urllib.request.urlopen(req).read().decode())
    return {"accessToken" : res["accessToken"],
            "clientToken" :res["clientToken"],
            "uuid" : res["selectedProfile"]["id"],
            "name" : res["selectedProfile"]["name"],
            }


def main():
    app = App()
    app.root.mainloop()


main()
