import json
import urllib.request
import urllib.error
import os
import platform
import errno
import requests
import shutil
from rich.console import Console
from pathlib import Path
import subprocess

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


def log(log, cmd='null', aList=[], custom=""):
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
        cprint(f"Not enough arguments for `{cmd}` command", codes.err)
    elif(log) == "tAIns":
        cprint(f"`{aList[0]}` already installed", codes.err)
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
    elif(log) == "pkgNFound":
        cprint("The specified package was not found in toollist.txt", codes.err)
    elif(log) == "inputNUnderstood":
        cprint("The given answer was not understood please use y/n.", codes.err)
    elif(log) == "listNExists":
        cprint(
            "`listtool.txt` file does not exist, could not remove package(s)", codes.err)
    elif(log) == "toolExists":
        cprint("The specified tool already exists.", codes.err)
    elif(log) == "unknownArgCUSTOM":
        cprint(f"Unknown argument `{custom}`", codes.err)
    else:
        cprint(f"INTERNAL ERROR, UNKNOWN CODE: {cmd}", codes.err)


toollistPath = ""
mainPath = ""
system = ""
toollistcache = ""

if platform.system() == "Windows":
    system = "windows"
elif platform.system() == "Linux":
    system = "linux"

if(system == "windows"):
    toollistPath = "C:\\toolbox\\toollist.txt"
    mainPath = "C:\\toolbox\\"
    toollistcache = "C:\\toolbox\\tool_list_cache.txt"
elif(system == "linux"):
    toollistPath = f"{os.path.expanduser('~')}/.toolboxlauncher/toollist.json"
    mainPath = f"{os.path.expanduser('~')}/.toolboxlauncher/"
    toollistcache = f"{os.path.expanduser('~')}/.toolboxlauncher/tool_list_cache.json"

if(os.path.exists(mainPath) == False):
    try:
        os.mkdir(mainPath)
    except OSError as exc:
        if exc.errno == errno.EACCES or errno.EPERM:
            log("permd")

if(os.path.exists(toollistcache) == False):
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/Indie-Toolbox/Indie-Toolbox/main/tools.json", toollistcache)
else:
    os.remove(toollistcache)
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/Indie-Toolbox/Indie-Toolbox/main/tools.json", toollistcache)


def getTools(isCheck=False):
    with open(toollistcache, "r") as f:
        raw = f.read()
    data = json.loads(raw)
    tools = {}
    for i in range(len(data)):
        tools[f"{data[i]['name']}"] = {"version": data[i]["version"], "title": data[i]["title"], "description": data[i]
                                       ["description"], "git": data[i]["git"], "supportedPlatforms": [x for x in data[i]["supportedPlatforms"]], "run": data[i]["run"], "file": data[i]["file"]}
    return tools


ToolListJSON = getTools()


def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()


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
    urllib.request.urlretrieve(url, path)
    log("gFile")


def parse(command, args):
    if(command == "exit"):
        if(len(args) == 0):
            exit()
        elif(len(args) > 0):
            log("tArgs", "exit")
    elif(command == "listTools"):
        if(len(args) > 2):
            log("tArgs", "listTools")
            return None
        if(len(args) == 0):
            try:
                tools = [x for x in ToolListJSON]
            except:
                return None
            log("availT")
            Iraw = []
            Itools = []
            try:
                with open(toollistPath, "r") as f:
                    Iraw = f.readlines()
                    for i in range(len(Iraw)):
                        Itool = Iraw[i].split(":")[0]
                        Itools.append(Itool)
            except:
                for i in range(len(tools)):
                    print(f"\t\t[ ] {tools[i]}")
            for i in range(len(tools)):
                for j in range(len(Itools)):
                    if tools[i] == Itools[j]:
                        print(f"\t\t[x] {tools[i]}")
                    else:
                        print(f"\t\t[ ] {tools[i]}")
        else:
            if (len(args) == 1):
                if(args[0] == "-i"):
                    if(os.path.isfile(toollistPath) == False):
                        log("nToolsIns")
                    else:
                        log("availInsTools")
                        with open(toollistPath, "r") as f:
                            raw = f.readlines()
                            for i in range(len(raw)):
                                tool = raw[i].split(":")
                                print(f"\t\t{tool[0]}: {tool[1]}", end="")
                        f.close()
                        print()
                elif(args[0] == "-d"):
                    try:
                        tools = [x for x in ToolListJSON]
                    except:
                        return None
                    log("availT")
                    Iraw = []
                    Itools = []
                    try:
                        with open(toollistPath, "r") as f:
                            Iraw = f.readlines()
                            for i in range(len(Iraw)):
                                Itool = Iraw[i].split(":")[0]
                                Itools.append(Itool)
                    except:
                        for i in range(len(tools)):
                            DRaw = ToolListJSON
                            des = DRaw[tools[i]]['description']
                            print(f"\t\t[ ] {tools[i]}")
                            print(f"\t\t\t{des}\n")
                    for i in range(len(tools)):
                        for j in range(len(Itools)):
                            if tools[i] == Itools[j]:
                                DRaw = ToolListJSON
                                des = DRaw[tools[i]]['description']
                                print(f"\t\t[x] {tools[i]}")
                                print(f"\t\t\t{des}\n")
                            else:
                                DRaw = ToolListJSON
                                des = DRaw[tools[i]]['description']
                                print(f"\t\t[ ] {tools[i]}")
                                print(f"\t\t\t{des}\n")
                else:
                    log("unknownArg", aList=args)
            elif(len(args) == 2):
                if(args[0] == "-i"):
                    if(args[1] == "-d"):
                        if(os.path.isfile(toollistPath) == False):
                            log("nToolsIns")
                        else:
                            log("availInsTools")
                            with open(toollistPath, "r") as f:
                                raw = f.readlines()
                                for i in range(len(raw)):
                                    DRaw = ToolListJSON
                                    tool = raw[i].split(":")
                                    des = DRaw[tool[0]]['description']
                                    print(f"\t\t{tool[0]}: {tool[1]}", end="")
                                    print(f"\t\t\t{des}")
                            f.close()
                            print()
                    else:
                        print("unknownArgCUSTOM", custom=args[1])
                elif(args[0] == "-d"):
                    if(args[1] == "-i"):
                        if(os.path.isfile(toollistPath) == False):
                            log("nToolsIns")
                        else:
                            log("availInsTools")
                            with open(toollistPath, "r") as f:
                                raw = f.readlines()
                                for i in range(len(raw)):
                                    DRaw = ToolListJSON
                                    tool = raw[i].split(":")
                                    des = DRaw[tool[0]]['description']
                                    print(f"\t\t{tool[0]}: {tool[1]}", end="")
                                    print(f"\t\t\t{des}")
                            f.close()
                            print()
                    else:
                        print("unknownArgCUSTOM", custom=args[1])
                else:
                    print("unknownArgCUSTOM", custom=args[0])
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
                        log("toolExists")
                        return None
        try:
            raw = ToolListJSON
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
            elif exc == errno.EACCES:
                log("permD")
        try:
            os.mkdir(os.path.join(mainPath, args[0]))
        except OSError as exc:
            if exc == errno.EEXIST:
                pass
            elif exc == errno.EACCES:
                log("permD")
        if system == "windows":
            systemSFile = ToolListJSON[args[0]]['file']['Windows']
            if(len(args) == 1):
                getFile(f"{raw[args[0]]['git']}/releases/download/{raw[args[0]]['version']}/{raw[args[0]]['file']['Windows']}",
                        os.path.join(mainPath, args[0], systemSFile))
            elif(len(args) == 3):
                if args[1] == "-v" or "-version":
                    response = requests.get(
                        f"{raw[args[0]]['git']}/releases/download/{args[2]}/{raw[args[0]]['file']['Windows']}", os.path.join(mainPath, args[0], systemSFile))
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
                        f"{raw[args[0]]['git']}/releases/download/{args[2]}/{raw[args[0]]['file']['Windows']}", os.path.join(mainPath, args[0], systemSFile))
            else:
                log("nEnoughSArgs")
                try:
                    shutil.rmtree(mainPath)
                except:
                    log("unknownDeleteError")
                return None
        elif system == "linux":
            systemSFile = ToolListJSON[args[0]]['file']['Linux']
            if(len(args) == 1):
                getFile(
                    f"{raw[args[0]]['git']}/releases/download/{raw[args[0]]['version']}/{raw[args[0]]['file']['Linux']}", os.path.join(mainPath, args[0], systemSFile))
            elif(len(args) == 3):
                if args[1] == "-v" or "-version":
                    response = requests.get(
                        f"{raw[args[0]]['git']}/releases/download/{args[2]}/{raw[args[0]]['file']['Linux']}", os.path.join(mainPath, args[0], systemSFile))
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
                        f"{raw[args[0]]['git']}/releases/download/{args[2]}/{raw[args[0]]['file']['Linux']}", os.path.join(mainPath, args[0], systemSFile))
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
    elif(command == "purge"):
        if(len(args) < 1):
            log("nArgs", "purge")
            return None
        elif(len(args) > 1):
            log("tArgs", "purge")
            return None
        if((args[0] == "-a") or (args[0] == "-all")):
            inputU = input(
                "\t[ PROMPT ]: Do you Really want to delete all tools (choose y/n)? ")
            if inputU.lower() == "y":
                try:
                    shutil.rmtree(mainPath)
                except:
                    log("unknownDeleteError")
                    return None
            elif inputU.lower() == "n":
                return None
            else:
                log("inputNUnderstood")
                return None
        else:
            with open(toollistPath, "r") as f:
                tools = f.readlines()
                found = False
                for i in range(len(tools)):
                    tool = tools[i].split(":")[0]
                    if(tool == args[0]):
                        found = True
                        tools.pop(i)
                if found == False:
                    log("pkgNFound")
                    return None
            f.close()
            if(len(tools)) == 0:
                rmdir(mainPath)
            else:
                inputU = input(
                    "\t[ PROMPT ]: Do you Really want to delete all tools (choose y/n)? ")
                if inputU.lower() == "y":
                    if os.path.exists(toollistPath):
                        os.remove(toollistPath)
                    else:
                        log("listNExists")
                        return None
                    with open(toollistPath, "w"):
                        for i in range(len(tools)):
                            f.write(f"{tools}\n")
                    try:
                        rmdir(Path(os.path.join(mainPath, args[0])))
                    except:
                        log("unknownDeleteError")
                elif inputU.lower() == "n":
                    return None
                else:
                    log("inputNUnderstood")
                    return None
    elif(command == "run"):
        if(len(args) > 1):
            log("tArgs", "run")
        if(len(args) < 1):
            log("nArgs", "run")
        if system == "windows":
            raw = ToolListJSON[args[0]]['run']['Windows']
            splitted = raw.split()
            subprocess.run(splitted)
        elif system == "linux":
            listT = ToolListJSON[args[0]]['run']['Linux']
            raw = listT.replace("~", os.path.expanduser("~"))
            splitted = raw.split()
            subprocess.run(splitted)
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
