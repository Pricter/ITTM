import os
import errno
import requests
import shutil
from pathlib import Path
import subprocess
##################################
from logger import *
from utils import *
from OsUtil import *

prepare()


def parse(command, args):
    if(command == "exit"):
        if checkArgs(args, 0, 0) == False:
            return None
        exit()
    elif(command == "listTools"):
        if checkArgs(args, 0, 2) == False:
            return None
        if(len(args) == 0):
            try:
                tools = [x for x in ToolListJSON]
            except:
                return None
            log("availableTools")
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
                        log("noToolsInstalled")
                    else:
                        log("availableInstalledTools")
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
                    log("availableTools")
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
                    log("unknownArgument", aList=args)
            elif(len(args) == 2):
                if(args[0] == "-i"):
                    if(args[1] == "-d"):
                        if(os.path.isfile(toollistPath) == False):
                            log("noToolsInstalled")
                        else:
                            log("availableInstalledTools")
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
                        print("unknownArgumentCUSTOM", custom=args[1])
                elif(args[0] == "-d"):
                    if(args[1] == "-i"):
                        if(os.path.isfile(toollistPath) == False):
                            log("noToolsInstalled")
                        else:
                            log("availableInstalledTools")
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
                        print("unknownArgumentCUSTOM", custom=args[1])
                else:
                    print("unknownArgumentCUSTOM", custom=args[0])
    elif(command == "install"):
        if checkArgs(args, 1, 3) == False:
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
            log("toolNotFoundInJson", aList=args)
            return None
        try:
            os.mkdir(mainPath)
        except OSError as exc:
            if exc == errno.EEXIST:
                pass
            elif exc == errno.EACCES:
                log("permissionDenied")
        try:
            os.mkdir(os.path.join(mainPath, args[0]))
        except OSError as exc:
            if exc == errno.EEXIST:
                pass
            elif exc == errno.EACCES:
                log("permissionDenied")
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
                        log("versionGetError")
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
                        log("versionGetError")
                        try:
                            shutil.rmtree(mainPath)
                        except:
                            log("unknownDeleteError")
                        return None
                    getFile(
                        f"{raw[args[0]]['git']}/releases/download/{args[2]}/{raw[args[0]]['file']['Linux']}", os.path.join(mainPath, args[0], systemSFile))
            else:
                log("notEnoughSubarguments")
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
        if checkArgs(args, 1, 1) == False:
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
                log("inputNotUnderstood")
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
                    log("packageNotFound")
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
                        log("listNotExists")
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
                    log("inputNotUnderstood")
                    return None
    elif(command == "run"):
        if checkArgs(args, 1, 1) == False:
            return None
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
        log("unknownCommand")


try:
    while True:
        inputU = getInput()
        parse(inputU[0], inputU[1])
except KeyboardInterrupt:
    log("keyCombination")
