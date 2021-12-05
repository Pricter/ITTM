import json
from ssl import match_hostname
import urllib.request
import os
import platform
import errno
import requests


class colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


toollistPath = ""
mainPath = ""
system = ""
if platform.system() == "Windows":
    system = "windows"
elif platform.system() == "Linux":
    system = "linux"

if(system == "windows"):
    toollistPath = "C:\\toolbox\\toollist.txt"
    mainPath = "C:\\toolbox\\"
elif(system == "linux"):
    toollistPath = "/usr/toolbox/toollist.txt"
    mainPath = "/usr/toolbox/"


def getTools():
    raw = urllib.request.urlopen(
        "https://raw.githubusercontent.com/Indie-Toolbox/Indie-Toolbox/main/tools.json").read()
    data = json.loads(raw)
    tools = {}
    for i in range(len(data)):
        tools[f"{data[i]['name']}"] = {"version": data[i]["version"], "title": data[i]["title"], "description": data[i]
                                       ["description"], "git": data[i]["git"], "supportedPlatforms": [x for x in data[i]["supportedPlatforms"]], "run": data[i]["run"], "file": data[i]["file"]}
    return tools


def getInput():
    UserData = input("> ")
    splitted = UserData.split()
    if(len(splitted) < 1):
        print(
            f"\n{colors.fg.red}[ERROR]: No command provided, Quitting the program{colors.reset}\n")
        exit()
    command = splitted[0]
    splitted.pop(0)
    args = splitted
    return [command, args]


def getFile(url, path):
    print(
        f"\t{colors.fg.yellow}[ INSTALL ]: Getting release file, this may take some time.{colors.reset}\n")
    file_name = url.split('/')[-1]
    fp = os.path.join(path, file_name)
    urllib.request.urlretrieve(url, fp)


def parse(command, args):
    if(command == "exit"):
        if(len(args) == 0):
            exit()
        elif(len(args) > 0):
            print(
                f"\n{colors.fg.red}[ ERROR ]: Too many arguments for `exit` command.{colors.reset}")
    elif(command == "listTools"):
        if(len(args) > 1):
            print(
                f"\n{colors.fg.red}[ ERROR ]: Too many arguments for `listTools` command.{colors.reset}")
            return None
        if(len(args) == 0):
            tools = [x for x in getTools()]
            print("\n\t[ TOOLS ]: Available Tools:")
            for i in range(len(tools)):
                print(f"\t\t{tools[i]}")
        if(len(args) == 1):
            if(args[0] == "-i" or "-installed"):
                if(os.path.isfile(toollistPath) == False):
                    print(
                        f"\n{colors.fg.blue}[ INFO ]: No tools currently installed.{colors.reset}")
                else:
                    print(
                        f"\n{colors.fg.blue}[ INFO ]: Current installed tool list:{colors.reset}")
                    with open(toollistPath, "r") as f:
                        raw = f.readlines()
                        for i in range(len(raw)):
                            print("\t" + raw[i], end="")
                    f.close()
                    print()
            else:
                print(
                    f"\n{colors.fg.red}[ ERROR ]: Unknown argument `{args[0]}`.{colors.reset}")
    elif(command == "install"):
        if(len(args) > 1):
            print(
                f"\n{colors.fg.red}[ ERROR ]: Too many arguments for `install` command.{colors.reset}")
            return None
        elif(len(args) < 1):
            print(
                f"\n{colors.fg.red}[ ERROR ]: Not enough arguments `install` command.{colors.reset}")
            return None
        raw = []
        if(os.path.isfile(toollistPath) == True):
            with open(toollistPath, "r") as f:
                raw = f.readlines()
                for i in range(len(raw)):
                    if(raw[i] == args[0]):
                        print(
                            f"\n{colors.fg.red}[ ERROR ]: `{args[0]}` already installed.{colors.reset}")
                        return None
        raw = getTools()
        tools = [x for x in getTools()]
        isThere = False
        for i in range(len(tools)):
            if tools[i] == args[0]:
                isThere = True
        if isThere == False:
            print(
                f"\n{colors.fg.red}[ ERROR ]: `{args[0]}` was not found in the main list of tools.{colors.reset}")
            return None
        try:
            os.mkdir(mainPath)
        except OSError as exc:
            if exc == errno.EEXIST:
                pass
            elif exc == errno.EACCES or errno.EPERM:
                print(
                    f"{colors.fg.red}[ ERROR ]: Permission denied run ittm using sudo.{colors.reset}")
                return None
        try:
            os.mkdir(os.path.join(mainPath, args[0]))
        except OSError as exc:
            if exc == errno.EEXIST:
                print(
                    f"\n{colors.fg.red}[ ERROR ]: `{args[0]}` seems to be installed but could not find it in `toollist.txt`.{colors.reset}")
                return None
            elif exc == errno.EACCES or errno.EPERM:
                print(
                    f"{colors.fg.red}[ ERROR ]: Permission denied run ittm using sudo.{colors.reset}")
                return None
        if system == "windows":
            getFile(
                f"{raw[args[0]]['git']}/releases/tag/{raw[args[0]]['version']}/{raw[args[0]]['file']['Windows']}", os.path.join(mainPath, args[0]))
        if system == "linux":
            getFile(
                f"{raw[args[0]]['git']}/releases/tag/{raw[args[0]]['version']}/{raw[args[0]]['file']['Linux']}", os.path.join(mainPath, args[0]))
        try:
            f = open(toollistPath, "x")
            f.close()
        except OSError as exc:
            if exc == errno.EEXIST:
                pass
        with open(toollistPath, "a") as f:
            f.write(f"\n{args[0]}")
        f.close()
    elif(command == "clear"):
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print(
            f"\n{colors.fg.red}[ ERROR ]: Unknown command, Please use valid commands.{colors.reset}")


try:
    while True:
        inputU = getInput()
        parse(inputU[0], inputU[1])
except KeyboardInterrupt:
    print(
        f"\n{colors.fg.green}[ KEY ]: You are pressing a key combination. The proper way to quit the program is using `exit`{colors.reset}\n")
