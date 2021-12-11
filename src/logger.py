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


def log(log, cmd='null', aList=[], custom=""):
    if(log) == "noCommandProvided":
        cprint("No command provided, Quitting the program", codes.err)
    elif(log) == "gettingFile":
        cprint("Getting release file, this may take some time", codes.inst)
    elif(log) == "tooManyArgs":
        cprint(f"Too many arguments", codes.err)
    elif(log) == "availableTools":
        cprint("Available Tools:", codes.info)
    elif(log) == "noToolsInstalled":
        cprint("No tools currently installed", codes.info)
    elif(log) == "availableInstalledTools":
        cprint("Current installed tool list:", codes.info)
    elif(log) == "notEnoughArgs":
        cprint(f"Not enough arguments", codes.err)
    elif(log) == "toolNotFoundInJson":
        cprint(
            f"`{aList[0]}` was not found in the main list of tools", codes.err)
    elif(log) == "permissionDenied":
        cprint(
            "Permission denied run ittm using sudo or as administrator", codes.err)
    elif(log) == "missingTool":
        cprint(
            f"`{aList[0]}` seems to be installed but could not find it in `toollist.txt`", codes.err)
    elif(log) == "versionGetError":
        cprint(
            "Version does not exist or server may be down", codes.err)
    elif(log) == "unknownDeleteError":
        cprint(
            "Could not delete directory upon failure", codes.err)
    elif(log) == "notEnoughSubarguments":
        cprint("Invalid argument or not enough sub arguments", codes.err)
    elif(log) == "unknownCommand":
        cprint("Unknown command, Please use valid commands", codes.err)
    elif(log) == "keyCombination":
        cprint("You are pressing a key combination. Using key combinations for terminal may result in unwanted results", codes.key)
    elif(log) == "unableFetch":
        cprint(
            "Unable to fetch the specified file, might be an internet issue", codes.err)
    elif(log) == "packageNotFound":
        cprint("The specified package was not found in toollist.txt", codes.err)
    elif(log) == "inputNotUnderstood":
        cprint("The given answer was not understood please use y/n.", codes.err)
    elif(log) == "listNotExists":
        cprint(
            "`listtool.txt` file does not exist, could not remove package(s)", codes.err)
    elif(log) == "toolExists":
        cprint("The specified tool already exists.", codes.err)
    elif(log) == "unknownArgumentCUSTOM":
        cprint(f"Unknown argument `{custom}`", codes.err)
    elif(log) == "unknownArgument":
        cprint(f"Unkown argument `{aList[0]}`", codes.err)
    else:
        cprint(f"INTERNAL ERROR, UNKNOWN CODE: {cmd}", codes.err)
