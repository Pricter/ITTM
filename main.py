import json
import urllib.request


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


def getTools():
    raw = urllib.request.urlopen(
        "https://raw.githubusercontent.com/Indie-Toolbox/Indie-Toolbox/main/tools.json").read()
    data = json.loads(raw)
    tools = {}
    for i in range(len(data)):
        tools[f"{data[i]['name']}"] = {"version": data[i]["version"], "title": data[i]["title"], "description": data[i]
                                       ["description"], "git": data[i]["title"], "supportedPlatforms": [x for x in data[i]["supportedPlatforms"]]}
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


def parse(command, args):
    if(command == "exit"):
        if(len(args) == 0):
            exit()
        elif(len(args) > 0):
            print(
                f"\n{colors.fg.red}[ ERROR ]: Too many arguments for `exit` command.{colors.reset}")
    elif(command == "listTools"):
        tools = [x for x in getTools()]
        print("\n\t[ TOOLS ]: Available Tools:")
        for i in range(len(tools)):
            print(f"\t\t{tools[i]}")
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
