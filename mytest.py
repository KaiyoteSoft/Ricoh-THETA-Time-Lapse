import subprocess

# subprocess.call("ptpcam --info", shell=True)

ptpinfo = subprocess.Popen(["ptpcam", "--info"], stdout=subprocess.PIPE)

infoList = []

for line in ptpinfo.stdout.readlines():
    infoList.append(line.rstrip())

def printExtension():
    print(infoList[-2].split(":")[1])

def printDeviceVersion():
    print("The device version is {}".format(infoList[6].split(":")[1]))

printExtension()
printDeviceVersion()
