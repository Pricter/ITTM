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


while True:
    print(getInput())
