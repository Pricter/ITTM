import json
import urllib.request
import errno
from pathlib import Path
from OsUtil import *
from logger import log


def prepare():
    if(os.path.exists(mainPath) == False):
        try:
            os.mkdir(mainPath)
        except OSError as exc:
            if exc.errno == errno.EACCES or errno.EPERM:
                log("permissionDenied")

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


def getFile(url, path):
    urllib.request.urlretrieve(url, path)
    log("gettingFile")


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
        log("noCommandProvided")
        exit()
    command = splitted[0]
    splitted.pop(0)
    args = splitted
    return [command, args]


def checkArgs(aList, minimum, maximum):
    if(len(aList) > maximum):
        log("tooManyArgs")
        return False
    elif(len(aList) < minimum):
        log("notEnoughArgs")
        return False
    return True


ToolListJSON = getTools()
