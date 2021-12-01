def getInput():
    UserData = input("> ")
    splitted = UserData.split()
    if(len(splitted) < 1):
        print("[ ERROR ]: No command provided, Quitting the program\n")
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
            print("[ ERROR ]: Too many arguments for `exit` command.")


while True:
    inputU = getInput()
    parse(inputU[0], inputU[1])
