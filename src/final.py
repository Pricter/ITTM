import subprocess
import sys
from rich.console import Console
import os
import errno
import requests
import shutil
from pathlib import Path
import platform
import json
import urllib.request
from tqdm import tqdm
import warnings

warnings.simplefilter("ignore")

toollistPath: str = ""
mainPath: str = ""
system: str = ""
toollistcache: str = ""

console = Console()

def log(text: str, code: str) -> None:
    code = code.lower()
    if(code == "error"):
        console.print(f"[ ERROR ]: {text}\n", style="red")
    elif(code == "key"):
        console.print(f"[ KEY ]: {text}\n", style="green")
    elif(code == "info"):
        console.print(f"[ INFO ]: {text}\n", style="blue")
    elif(code == "install"):
        console.print(f"[ INSTALL ]: {text}\n", style="yellow")
    elif(code == "tool"):
        console.print(f"[ TOOLS ]: {text}\n", style="magenta")

class ittm:
    def __init__(self):
        self.initOS()
        self.getCache()
        self.ToolListJSON = self.getToolsJson()
        self.Tools = [x for x in self.ToolListJSON]
        self.ITools = [x for x in self.getInstalledTools()]
        self.IToolsVersionSpecification = self.getInstalledTools()

    def initOS(self) -> None:
        global toollistPath
        global mainPath
        global system
        global toollistcache

        if platform.system() == "Windows":
            system = "windows"
        elif platform.system() == "Linux":
            system = "linux"
        elif platform.system() == "Darwin":
            system = "mac"

        if(system == "windows"):
            toollistPath = "C:\\toolbox\\toollist.txt"
            mainPath = "C:\\toolbox\\"
            toollistcache = "C:\\toolbox\\tool_list_cache.json"
        elif(system == "linux"):
            toollistPath = f"{os.path.expanduser('~')}/.toolboxlauncher/toollist.json"
            mainPath = f"{os.path.expanduser('~')}/.toolboxlauncher/"
            toollistcache = f"{os.path.expanduser('~')}/.toolboxlauncher/tool_list_cache.json"
        elif(system == "mac"):
            toollistPath = f"{os.path.expanduser('~')}/.toolboxlauncher/toollist.json"
            mainPath = f"{os.path.expanduser('~')}/.toolboxlauncher/"
            toollistcache = f"{os.path.expanduser('~')}/.toolboxlauncher/tool_list_cache.json"
        else:
            print("You are running an unsupported OS ( ._.)")
            exit()

        if(os.path.exists(mainPath) == False):
            try:
                os.mkdir(mainPath)
            except OSError as exc:
                if exc.errno == errno.EACCES or errno.EPERM:
                    log("Permission denied, run as sudo or administrator", "error")

    def getToolsJson(self) -> None:
        with open(toollistcache, "r") as f:
            raw = f.read()
        data = json.loads(raw)
        tools = {}
        for i in range(len(data)):
            tools[f"{data[i]['name']}"] = {"version": data[i]["version"], "title": data[i]["title"], "description": data[i]
                                        ["description"], "git": data[i]["git"], "supportedPlatforms": [x for x in data[i]["supportedPlatforms"]], "install": data[i]["install"], "run": data[i]["run"], "file": data[i]["file"]}
        return tools
    
    def getCache(self) -> None:
        if(os.path.exists(toollistcache) == False):
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/Indie-Toolbox/Indie-Toolbox/main/tools.json", toollistcache)
        else:
            os.remove(toollistcache)
            urllib.request.urlretrieve(
                "https://raw.githubusercontent.com/Indie-Toolbox/Indie-Toolbox/main/tools.json", toollistcache)

    def getFile(self, url: str, path: str) -> None:
        chunk_size = 1024
        r = requests.get(url, stream = True)
        total_size = int(r.headers['Content-Length'])

        with open(path, "wb") as f:
            for data in tqdm(iterable = r.iter_content(chunk_size=chunk_size), total = total_size / chunk_size, unit="KB"):
                f.write(data)

        print("\nDownload complete.")

    def rmdir(self, directory: str):
        directory = Path(directory)
        for item in directory.iterdir():
            if item.is_dir():
                self.rmdir(item)
            else:
                item.unlink()
        directory.rmdir()

    def checkArgs(self, argList: list, minimum: int, maximum: int) -> bool:
        if(len(argList) > maximum):
            log("Too many arguments provided.", "error")
            return False
        elif(len(argList) < minimum):
            log("Not enough arguments provided.", "error")
            return False
        return True

    def getInstalledTools(self) -> dict:
        raw = []
        tools = {}
        if(os.path.isfile(toollistPath) == True):
            with open(toollistPath, "r") as f:
                raw = f.readlines()
                for i in range(len(raw)):
                    toolCache = raw[i].split(":")
                    tools[toolCache[0]] = toolCache[1]
        return tools

    def isToolInstalled(self, tool: str) -> bool:
        for i in range(len(self.ITools)):
            if self.ITools[i] == tool:
                return True
        return False
    
    def doesToolExist(self, tool: str) -> bool:
        tools = [x for x in self.ToolListJSON]
        for i in range(len(tools)):
            if tools[i] == tool:
                return True
        return False

    def run(self) -> None:
        inputU = input("> ")
        if(inputU == ""):
            print("No command provided, Quitting Automatically.")
            exit()
        splitted = inputU.split()
        command = splitted[0]
        splitted.pop(0)
        args = splitted
        self.parse(command, args)
    
    def purgeTool(self, tool: str) -> bool:
        purged = False
        if(len(self.ITools) == 0):
            try: shutil.rmtree(mainPath)
            except: log("Unable to delete tool, try running as sudo or administrator", "error"); return False
            return True
        for i in range(len(self.ITools)):
            if(self.ITools[i] == tool):
                self.IToolsVersionSpecification.pop(self.Itools[i])
                self.ITools.pop(i)
                purged = True
        if(purged != True):
            log("The specified package was not found.", "error")
            return False
        with open(toollistPath, "w") as f:
            for i in range(len(self.ITools)):
                f.write(f"{self.ITools[i]}:{self.IToolsVersionSpecification[self.ITools[i]]}")
        f.close()
        return True
        
    
    def parse(self, command: str, args: list) -> None:
        if(command == "exit"):
            if self.checkArgs(args, 0, 0) == False:
                return None
            exit()
        elif(command == "listTools"):
            if self.checkArgs(args, 0, 2) == False:
                return None
            if(len(args) == 0):
                log("Available tools:\n", "tools")
                for i in range(len(self.Tools)):
                    if(self.isToolInstalled(self.Tools[i])):
                        print(f"\t[x] {self.Tools[i]}")
                    else:
                        print(f"\t[ ] {self.Tools[i]}")
            elif(len(args) == 1):
                if(args[0] == "-i"):
                    if(os.path.isfile(toollistPath) == False):
                        log("You have no tools currently installed", "info")
                        return None
                    print()
                    for i in range(len(self.IToolsVersionSpecification)):
                        print(f"\t{self.Tools[i]}: {self.ToolListJSON[self.Tools[i]]['title']}", end="")
                    print()
                elif(args[0] == "-d"):
                    for i in range(len(self.Tools)):
                        supportedPlatforms = [x for x in self.ToolListJSON[self.Tools[i]]['supportedPlatforms']]
                        if(self.isToolInstalled(self.Tools[i])):
                            print(f"\t[x] {self.Tools[i]}")
                        else:
                            print(f"\t[ ] {self.Tools[i]}")
                        print(f"\t    Latest Version: {self.ToolListJSON[self.Tools[i]]['version']}")
                        print(f"\t    Title: {self.ToolListJSON[self.Tools[i]]['title']}")
                        print(f"\t    Description: {self.ToolListJSON[self.Tools[i]]['description']}")
                        print(f"\t    Git repo: {self.ToolListJSON[self.Tools[i]]['git']}")
                        print(f"\t    Supported Platforms: ", end="")
                        for i in range(len(supportedPlatforms)):
                            print(f"{supportedPlatforms[i]}, ", end="")
                        print()
            elif(len(args) == 2):
                if(((args[0] == "-i") and (args[1] == "-d")) or ((args[0] == "-d") and (args[1] == "-i"))):
                    if(os.path.isfile(toollistPath) == False):
                        log("You have no tools currently installed", "info")
                    else:
                        log("Available Tools:", "info")
                        for i in range(len(self.ITools)):
                            supportedPlatforms = [x for x in self.ToolListJSON[self.ITools[i]]['supportedPlatforms']]
                            if(self.isToolInstalled(self.ITools[i])):
                                print(f"\t[x] {self.ITools[i]}")
                            else:
                                print(f"\t[ ] {self.ITools[i]}")
                            print(f"\t    Latest Version: {self.ToolListJSON[self.Tools[i]]['version']}")
                            print(f"\t    Installed Version: {self.IToolsVersionSpecification[self.ITools[i]]}", end="")
                            print(f"\t    Title: {self.ToolListJSON[self.ITools[i]]['title']}")
                            print(f"\t    Description: {self.ToolListJSON[self.ITools[i]]['description']}")
                            print(f"\t    Git repo: {self.ToolListJSON[self.ITools[i]]['git']}")
                            print(f"\t    Supported Platforms: ", end="")
                            for i in range(len(supportedPlatforms)):
                                print(f"{supportedPlatforms[i]}, ", end="")
                            print()
                        print()
                else:
                    log("Unknown Argument.", "error")
        elif(command == "install"):
            if(self.checkArgs(args, 1, 3) == False):
                return None
            for i in range(len(self.ITools)):
                if(self.isToolInstalled(args[0])):
                    log("The specified tool already exists.", "error")
                    return None
            if(self.doesToolExist(args[0]) == False):
                log("The specified tool was not found in the main json list.", "error")
                return None
            try:
                os.makedirs(os.path.join(mainPath, args[0].lower()))
            except OSError as exc:
                if exc == errno.EEXIST:
                    log("The folder in which the tool is supposed to be in is already occupied.", "error")
                    return None
                elif exc == errno.EACCES:
                    log("Permission denied, run using sudo or administrator", "error")
                    return None
            ############# FETCH FILE #############
            if(len(args) == 3):
                if args[1] == "-v" or "-version":
                    response = requests.get(
                        f"{self.ToolListJSON[args[0]]['git']}/releases/download/{args[2]}/{self.ToolListJSON[args[0]]['file']['Windows']}",os.path.join(mainPath, args[0], self.ToolListJSON[args[0]]['file'][platform.system()]))
                    if(response.status_code != 200):
                        log("The specified version does not exist.", "error")
                        return None
                    if((system == "windows") or (system == "linux")):
                        self.getFile(
                            f"{self.ToolListJSON[args[0]]['git']}/releases/download/{args[2]}/{self.ToolListJSON[args[0]]['file'][platform.system()]}", os.path.join(mainPath, args[0], self.ToolListJSON[args[0]]['file'][platform.system()]))
                        self.ITools.append(args[0])
                        self.IToolsVersionSpecification[args[0]] = args[2]
                        if len(self.ToolListJSON[args[0]]["install"]) > 0:
                            scripts = self.ToolListJSON[args[0]]["install"]
                            systems = list(scripts.keys())
                            for i in range(len(self.ToolListJSON[args[0]]["install"])):
                                if systems[i] == "" or systems[i] != system or scripts[systems[i]] == []:
                                    pass
                                print("[ INFO ] Running install script: " + scripts[systems[i]])
                                subprocess.run(self.ToolListJSON[args[0]]["install"][i], shell=True)
                    else:
                        log("MacOS supported but not fully implemented until there is atleast one tool that supports mac.", "error")
                        exit()
                else:
                    log("Unknown Argument.", "error")
            elif(len(args) == 1):
                if(system == "windows" or system == "linux"):
                    self.getFile(
                            f"{self.ToolListJSON[args[0]]['git']}/releases/download/{self.ToolListJSON[args[0]]['version']}/{self.ToolListJSON[args[0]]['file'][platform.system()]}", os.path.join(mainPath, args[0], self.ToolListJSON[args[0]]['file'][platform.system()]))
                    if len(self.ToolListJSON[args[0]]["install"]) > 0:
                        for i in range(len(self.ToolListJSON[args[0]]["install"][f"{system.capitalize()}"])):
                            print("[ INFO ] Running install script: " + self.ToolListJSON[args[0]]["install"][f"{system.capitalize()}"][i])
                            subprocess.run(self.ToolListJSON[args[0]]["install"][f"{system.capitalize()}"][i], shell=True)
                    self.ITools.append(args[0])
                    self.IToolsVersionSpecification[args[0]] = self.ToolListJSON[args[0]]['version']
                else:
                    log("MacOS supported but not fully implemented until there is atleast one tool that supports mac.", "error")
                    exit()
            else:
                log("Invalid number of arguments.", "error")
            try:
                f = open(toollistPath, "x")
                f.close()
            except OSError as exc:
                pass
            with open(toollistPath, "a") as f:
                if(len(args) == 1):
                    f.write(f"{args[0]}:{self.ToolListJSON[args[0]]['version']}\n")
                else:
                    f.write(f"{args[0]}:{args[2]}\n")
            f.close()
        elif(command == "purge"):
            if(self.checkArgs(args, 1, 1)) == False:
                return None
            if((args[0] == "-a") or (args[0] == "-all")):
                inputU = input(
                "\t[ PROMPT ]: Do you Really want to delete all tools (choose y/n)? ")
                if(inputU.lower() == "y" or inputU.lower() == "yes"):
                    try: shutil.rmtree(mainPath); self.ITools = []; self.IToolsVersionSpecification = {}
                    except:
                        log("Could not reset ittm, maybe try running with sudo or administrator.", "error")
                        return None
                elif(inputU.lower() == "n" or inputU.lower() == "no"):
                    return None
                else:
                    log("The given input was not understood.", "error")
                    return None
            else:
                if(self.purgeTool(args[0]) == False):
                    return None
        elif(command == "run"):
            if self.checkArgs(args, 1, 1) == False:
                return None
            if not self.isToolInstalled(args[0]):
                log("The specified tool is not installed.", "error")
                return None
            if(system == "windows"):
                raw = self.ToolListJSON[args[0]]['run']['Windows']
                splitted = raw.split()
                subprocess.run(splitted)
            elif(system == "linux"):
                listT = self.ToolListJSON[args[0]]['run']['Linux']
                raw = listT.replace("~", os.path.expanduser("~"))
                splitted = raw.split()
                subprocess.run(splitted)
        elif(command == "cls"):
            os.system('cls' if os.name == 'nt' else 'clear')
        elif(command == "clear"):
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            log(f"Unknown command `{command}`.", "error")
            return None

instance = ittm()

try:
    while True:
        instance.run()
except KeyboardInterrupt:
    log("You pressed a key combination, Using a key combination in this prompt may result in weird issues.", "key")