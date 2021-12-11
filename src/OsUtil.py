import platform
import os

toollistPath = ""
mainPath = ""
system = ""
toollistcache = ""

if platform.system() == "Windows":
    system = "windows"
elif platform.system() == "Linux":
    system = "linux"
elif platform.system() == "Darwin":
    system = "mac"

if(system == "windows"):
    toollistPath = "C:\\toolbox\\toollist.txt"
    mainPath = "C:\\toolbox\\"
    toollistcache = "C:\\toolbox\\tool_list_cache.txt"
elif(system == "linux"):
    toollistPath = f"{os.path.expanduser('~')}/.toolboxlauncher/toollist.json"
    mainPath = f"{os.path.expanduser('~')}/.toolboxlauncher/"
    toollistcache = f"{os.path.expanduser('~')}/.toolboxlauncher/tool_list_cache.json"
elif(system == "mac"):
    toollistPath = f"{os.path.expanduser('~')}/.toolboxlauncher/toollist.json"
    mainPath = f"{os.path.expanduser('~')}/.toolboxlauncher/"
    toollistcache = f"{os.path.expanduser('~')}/.toolboxlauncher/tool_list_cache.json"
