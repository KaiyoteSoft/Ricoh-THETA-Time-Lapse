import subprocess
import time, os, datetime, glob, shutil

## example of taking a picture

response = raw_input("Photos will be saved in the Downloads folder\nPlease indicate the number of seconds you would like the delay to be (Eg. 10): ")
delay = int(response)
if delay < 9:
    warningResponse = raw_input("The delay has to be greater than or equal to 9 seconds due to the processing time of the images. Please select a longer delay: ")
    delay = int(warningResponse) - 8
else:
    delay = delay - 8
    print(delay)

def takePicture():
    startTime = time.time()

## Simply gets the date and time to create a unique directory for
## the photos to be stored in
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    sec = date.second
    compiledDate = ("%i-%i-%i %i:%i.%i" % (year, month, day, hour, minute, sec))

### Users will have to change where the variable file path points to
##### so that it will save to a directory that exists on their computer
    filePath = '/home/craig/Downloads/Ricoh Timelapse {}'.format(compiledDate)
    # print(compiledDate)
    if not os.path.exists(filePath):
        os.mkdir(filePath)

    # example of grabbing device info and using it in your python program.
    ptpinfo = subprocess.Popen(["ptpcam", "--info"], stdout=subprocess.PIPE)
    # although this simply prints to stdout, you can parse
    # the response for your program
    for line in ptpinfo.stdout.readlines():
        print(line.rstrip())

    while True:
        elapsedTime = time.time() - startTime
        if elapsedTime > delay:
            subprocess.call("ptpcam -c", shell=True)

            # find the last picture taken. Modify to parse for date or other. Will eventually be used to delete the
            #pictures when the camera is full
            files = []
            listFiles = subprocess.Popen(["ptpcam", "-L"], stdout=subprocess.PIPE)
            for line in listFiles.stdout.readlines():
                files.append(line.rstrip())
            lastLine = files[len(files) - 2].split(" ")
            lastPicture = lastLine[0][:-1]
            lastPictureName = lastLine[1][:-1]

            # print("The handle for the last picture taken is " + lastPicture)
            #
            # # download the picture
            ptpcommand = "ptpcam --get-file=" + lastPicture
            subprocess.call(ptpcommand, shell=True)

            files = glob.iglob(os.path.join('/home/craig/Documents/Accounts/ricoh/Development/usb/subprocess', "*.JPG"))
            for file in files:
                if os.path.isfile(file):
                    shutil.move(file, filePath)

            # print(elapsedTime)
            startTime = time.time()

takePicture()
