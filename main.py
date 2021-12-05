import json
import urllib.request
import urllib.error
import os
import platform
import errno
import requests
import shutil
from rich.console import Console

console = Console()


class codes:
    err = "-1"
    warning = "0"
    key = "1"
    info = "2"
    inst = "3"
    tool = "4"


def cprint(text, code):
    if(code == codes.err):
        console.print(f"[ ERROR ]: {text}\n", style="red")
    if(code == codes.key):
        console.print(f"[ KEY ]: {text}\n", style="green")
    if(code == codes.info):
        console.print(f"\n[ INFO ]: {text}", style="blue")
    if(code == codes.inst):
        console.print(f"\t[ INSTALL ]: {text}\n", style="yellow")
    if(code == codes.tool):
        console.print(f"\n\t[ TOOLS ]: {text}\n", style="magenta")


def log(log, cmd='null', aList=[]):
    if(log) == "nCmd":
        cprint("No command provided, Quitting the program", codes.err)
    elif(log) == "gFile":
        cprint("Getting release file, this may take some time", codes.inst)
    elif(log) == "tArgs":
        cprint(f"Too many arguments for `{cmd}` command", codes.err)
    elif(log) == "availT":
        cprint("Available Tools:", codes.info)
    elif(log) == "nToolsIns":
        cprint("No tools currently installed", codes.info)
    elif(log) == "availInsTools":
        cprint("Current installed tool list:", codes.info)
    elif(log) == "unknownArg":
        cprint(f"Unknown argument `{aList[0]}`", codes.err)
    elif(log) == "nArgs":
        cprint("Not enough arguments for `{cmd}` command", codes.err)
    elif(log) == "tAIns":
        cprint("`{aList[0]}` already installed", codes.err)
    elif(log) == "toolNotFoundMain":
        cprint(
            f"`{aList[0]}` was not found in the main list of tools", codes.err)
    elif(log) == "permD":
        cprint(
            "Permission denied run ittm using sudo or as administrator", codes.err)
    elif(log) == "missingTool":
        cprint(
            f"`{aList[0]}` seems to be installed but could not find it in `toollist.txt`", codes.err)
    elif(log) == "vGetError":
        cprint(
            "Version does not exist or server may be down", codes.err)
    elif(log) == "unknownDeleteError":
        cprint(
            "Could not delete directory upon failure", codes.err)
    elif(log) == "nEnoughSArgs":
        cprint("Invalid argument or not enough sub arguments", codes.err)
    elif(log) == "unknownCmd":
        cprint("Unknown command, Please use valid commands", codes.err)
    elif(log) == "key":
        cprint("You are pressing a key combination. Using key combinations for terminal may result in unwanted results", codes.key)
    elif(log) == "unableFetch":
        cprint(
            "Unable to fetch the specified file, might be an internet issue", codes.err)
    else:
        cprint(f"INTERNAL ERROR, UNKNOWN CODE: {cmd}", codes.err)


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


def getTools(isCheck=False):
    try:
        raw = urllib.request.urlopen(
            "https://raw.githubusercontent.com/Indie-Toolbox/Indie-Toolbox/main/tools.json").read()
    except Exception as exc:
        if isCheck == True:
            log("unableFetch")
            return None
        else:
            return None
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
        log("ncmd")
        exit()
    command = splitted[0]
    splitted.pop(0)
    args = splitted
    return [command, args]


def getFile(url, path):
    log("gFile")
    file_name = url.split('/')[-1]
    fp = os.path.join(path, file_name)
    urllib.request.urlretrieve(url, fp)


def parse(command, args):
    if(command == "exit"):
        if(len(args) == 0):
            exit()
        elif(len(args) > 0):
            log("tArgs", "exit")
    elif(command == "listTools"):
        if(len(args) > 1):
            log("tArgs", "listTools")
            return None
        if(len(args) == 0):
            try:
                tools = [x for x in getTools()]
            except:
                return None
            log("availT")
            for i in range(len(tools)):
                print(f"\t\t{tools[i]}")
        if(len(args) == 1):
            if(args[0] == "-i" or "-installed"):
                if(os.path.isfile(toollistPath) == False):
                    log("nToolsIns")
                else:
                    log("availInsTools")
                    with open(toollistPath, "r") as f:
                        raw = f.readlines()
                        tools = []
                        for i in range(len(raw)):
                            tool = raw[i].split(":")
                            print(f"\t{tool[0]}: {tool[1]}", end="")
                    f.close()
                    print()
            else:
                log("unknownArg", aList=args)
    elif(command == "install"):
        if(len(args) > 3):
            log("tArgs", "install")
            return None
        elif(len(args) < 1):
            log("nArgs", "install")
            return None
        raw = []
        if(os.path.isfile(toollistPath) == True):
            with open(toollistPath, "r") as f:
                raw = f.readlines()
                tools = []
                for i in range(len(raw)):
                    tool = raw[i].split(":")
                    tools.append(tool[0])
                for i in range(len(tools)):
                    if(tools[i] == args[0]):
                        return None
        try:
            raw = getTools()
        except:
            return None
        try:
            tools = [x for x in getTools(True)]
        except:
            return None
        isThere = False
        for i in range(len(tools)):
            if tools[i] == args[0]:
                isThere = True
        if isThere == False:
            log("toolNotFoundMain", aList=args)
            return None
        try:
            os.mkdir(mainPath)
        except OSError as exc:
            if exc == errno.EEXIST:
                pass
            elif exc == errno.EACCES or errno.EPERM:
                log("permD")
                return None
        try:
            os.mkdir(os.path.join(mainPath, args[0]))
        except OSError as exc:
            if exc == errno.EEXIST:
                log("missingTool", aList=args)
                return None
            elif exc == errno.EACCES or errno.EPERM:
                log("permD")
                return None
        if system == "windows":
            if(len(args) == 1):
                getFile(
                    f"{raw[args[0]]['git']}/releases/tag/{raw[args[0]]['version']}/{raw[args[0]]['file']['Windows']}", os.path.join(mainPath, args[0]))
            elif(len(args) == 3):
                if args[1] == "-v" or "-version":
                    response = requests.get(
                        f"{raw[args[0]]['git']}/releases/tag/{args[2]}/{raw[args[0]]['file']['Windows']}", os.path.join(mainPath, args[0]))
                    if response.status_code == 200:
                        pass
                    else:
                        log("vGetError")
                        try:
                            shutil.rmtree(mainPath)
                        except:
                            log("unknownDeleteError")
                        return None
                    getFile(
                        f"{raw[args[0]]['git']}/releases/tag/{args[2]}/{raw[args[0]]['file']['Windows']}", os.path.join(mainPath, args[0]))
            else:
                log("nEnoughSArgs")
                try:
                    shutil.rmtree(mainPath)
                except:
                    log("unknownDeleteError")
                return None
        if system == "linux":
            if(len(args) == 1):
                getFile(
                    f"{raw[args[0]]['git']}/releases/tag/{raw[args[0]]['version']}/{raw[args[0]['version']]['file']['Linux']}", os.path.join(mainPath, args[0]))
            elif(len(args) == 3):
                if args[1] == "-v" or "-version":
                    response = requests.get(
                        f"{raw[args[0]]['git']}/releases/tag/{args[2]}/{raw[args[0]]['file']['Linux']}", os.path.join(mainPath, args[0]))
                    if response.status_code == 200:
                        pass
                    else:
                        log("vGetError")
                        try:
                            shutil.rmtree(mainPath)
                        except:
                            log("unknownDeleteError")
                        return None
                    getFile(
                        f"{raw[args[0]]['git']}/releases/tag/{args[2]}/{raw[args[0]]['file']['Linux']}", os.path.join(mainPath, args[0]))
            else:
                log("nEnoughSArgs")
                try:
                    shutil.rmtree(mainPath)
                except:
                    log("unknownDeleteError")
                return None
        try:
            f = open(toollistPath, "x")
            f.close()
        except OSError as exc:
            if exc == errno.EEXIST:
                pass
        with open(toollistPath, "a") as f:
            if(len(args) == 1):
                f.write(f"{args[0]}:{raw[args[0]]['version']}\n")
            else:
                f.write(f"{args[0]}:{args[2]}\n")
        f.close()
    elif(command == "clear"):
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        log("unknownCmd")


try:
    while True:
        inputU = getInput()
        parse(inputU[0], inputU[1])
except KeyboardInterrupt:
    log("key")
