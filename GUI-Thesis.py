# Michael Quinn Parkinson - GUI interface for my thesis (VERY EARLY VERSION)
# This program takes in a file name and creates a file.
# It will then generate initial conditions and test if the IC file is ready to be used.
# Once the IC file is created, the program will call Gadget2 and run a simulation.
# Besides running a simulation the program also allows the visualization of SPH data via gsplash.


# New Changes will be to include an option to pick the location and destination of files and folders.
# As well as allow for the customization of the Gadget2 System Parameter File. 

# Import Modules Needed to Create Initial Condition Files
# Default Python Modules 2.7+ Will Always Have These Modules Installed
print "\nChecking Default Installed Modules...\n"
import struct
import array
import random
import time
import os
import sys
print "\nDefault Modules Located and Imported.\n"
from subprocess import Popen
print "\nChecking Specific Installed Modules...\n"
# Tkinter For GUI Interaction
try:
	import Tkinter
	from Tkinter import *
	from tkFileDialog import askopenfilename
	print "\nTkinter Module Installed.\n"
except ImportError:
	print "Please Install Tkiner."
	sys.exit(0)
# NUMPY For Data Implementation 
try:
	import numpy
	print "\nNumPy Module Installed.\n"
except ImportError:
	print "Please Install NumPy."
	sys.exit(0)
##########################################################################################

def GUIWindow():
# MAIN GUI WINDOW
    global root,text
    root = Tkinter.Tk()
    root.title('v05')
    # Creates A Default Window Of 800x600
    screen_reso = str(800)+'x'+str(600)
    root.geometry(screen_reso)
    # Welcome Screen Text
    text = Text(root,width=72, height=12,borderwidth=4)
    text.insert(INSERT,"\nWelcome to the /ICs File Creator.\nNbody Simulator\nCurrent Version\nAlpha V0.05\n")
    text.insert(END,"")
    text.see(END)
    text.config(state=DISABLED)
    text.grid()
    QuitButton = Button(root, text="Quit", command=lambda root=root:Quit(root),borderwidth=3)
    QuitButton.grid(row=55,column=4,padx=1,pady=10)
    GraphButton = Button(root,text="Begin Visualization",command=Graph)
    GraphButton.grid(row=0,column=4,padx=1,pady=10)
##########################################################################################

def callbackfilename(event):
# Loads/Creates Random Dat IC File (IF IT DOES NOT EXIST IT CREATES FILE)
# FName is the Global File Name Variable From The Function GetFileName()
# the global variable file is the true filename + path for the initial condition file
    global files, filename
    fname = FName.get()
    # 	Checks file name is correctly entered into the GetFileName()
    if fname != '':
        # 	Creates File
        FileName = str(fname)
        # Linux File Path
        try:
            filename = '/media/CRUNCHBANG/Files/'+str(FileName)
            text.config(state=NORMAL)
            text.insert(INSERT,"\nInitial Condition File Name:\n")
            text.insert(INSERT,FileName)
            text.insert(INSERT,'\n')
            text.see(INSERT)
            text.config(state=DISABLED)
            text.grid()
        except IOError:
            text.insert(INSERT,"\nFolder Not Found.\n")
            text.insert(INSERT,filename)
            text.insert(INSERT,"\n")
# Destroys Data Entry, Label, and Button from GetFileName()
        FName.destroy()
        FLabel.grid_remove()	
        FButton.grid_remove()
# Test if the File already Exists
# If file Exist Validate the File and Proceed with the Simulation
# Else Create File and begin the Initialization Process
        testfile = os.path.isfile(filename)
        if testfile == True:
            text.config(state=NORMAL)
            text.insert(INSERT,"\nFile Already Exists...Validate Data.\n")
            text.insert(INSERT,FileName)
            text.insert(INSERT,"\n")
            text.see(INSERT)
            text.config(state=DISABLED)
            global ValidateButton
            ValidateButton = Button(root,text='Validate Data')
            ValidateButton.bind('<Return>',trydata)
            ValidateButton.bind('<KP_Enter>',trydata)
            ValidateButton.bind('<Button-1>',trydata)
            ValidateButton.grid()
        else:
            text.config(state=NORMAL)
            text.insert(INSERT,"\nCreating Initial Condition File...\n")
            text.insert(INSERT,filename)
            text.insert(INSERT,"\n")
            text.see(INSERT)
            text.config(state=DISABLED)
            try:
                files = open(filename,mode='wb+')
                WriteFile()
            except IOError:
                text.insert(INSERT,"\nFolder Not Found.\n")
                text.insert(INSERT,filename)
                text.insert(INSERT,"\n")
    else:
        text.config(state=NORMAL)
        text.insert(INSERT,'\nMissing File Name From Entry Box\n')
        text.see(INSERT)
        text.config(state=DISABLED)
        text.grid()
##########################################################################################

def GetFileName():
# Adds a Save Button and Entry Window on the First Screen
# Rows and Columns are for object location
# FButton.bind Allows for keyboard and mouse data entry
# Adds A Text Label and Save Button and Text Entry Window To GUI
# The Entry Function Gives a Name For The Initial Condition File
# FName does not include the .dat Just the File Name 
# FLabel,FName,FButton Are Global Variables to be Destroy upon Data Entry
    global FLabel,FName,FButton
    FLabel = Label(root,text="\nWhat is the Initial Condition File Name?\n")
    FLabel.grid(row=23,column=0)
    FName = Entry(root)
    FName.grid(row=24,column=0)
    FName.focus_set()
    FButton = Button(root,text='Save File Name',borderwidth=4)
    FButton.bind('<Return>',callbackfilename)
    FButton.bind('<KP_Enter>',callbackfilename)
    FButton.bind('<Button-1>',callbackfilename)
    FButton.grid(row=25,column=3)
##########################################################################################

def GetHeader():
# Loads the predefined header
    try:
# The Header Needs to Be a Global Variable that is Referenced BY:    
        global Header
# LINUX PATH
        HeadPath = '/media/CRUNCHBANG/Files/header-10.dat'
# MAC PATH
#         HeadPath = '/Volumes/CRUNCHBANG/Files/header-4.dat'
        Header = numpy.loadtxt(HeadPath, unpack = True)
        text.config(state=NORMAL)
        text.insert(INSERT,"\nHeader File Imported.\n")
        text.see(INSERT)
        text.config(state=DISABLED)
        text.grid()
# If Header Can Not be Found Kill the Program Since IT IS ABSOLUTELY NECESSARY
    except IOError:
        text.config(state=NORMAL)
        text.insert(INSERT,"\nHeader Not Found. Please Create Header.\n")
        text.see(INSERT)
        text.config(state=DISABLED)
        text.grid()
        #sys.exit(0)
##########################################################################################

def GetInputFile():
# Loads Predefined Input File
    try:
#Each Data Array From Input File is Referenced BY:
#The Length Of Each Array is Determined By NumberOfObjects
		global NumberOfObjects,ObjectMass,XPosition,YPosition,ZPosition,XVelocity,YVelocity,ZVelocity
		InputFile =  '/media/CRUNCHBANG/Files/input-10.dat'
		ObjectMass,XPosition,YPosition,ZPosition,XVelocity,YVelocity,ZVelocity = numpy.loadtxt(InputFile, unpack = True)
		NumberOfObjects = len(ObjectMass)
		text.config(state=NORMAL)
		text.insert(INSERT,"\nInitial Data Imported.\n")
		text.see(INSERT)
		text.config(state=DISABLED)
		text.grid()
# If Input Data Can Not Be Found Kill the Program Since IT IS ABSOLUTELY NECESSARY
    except IOError:
        text.config(state=NORMAL)
        text.insert(INSERT,"\nInitial Dat File Not Found. Please Create Initial Data File.\n")
        text.see(INSERT)
        text.config(state=DISABLED)
        text.grid()
        #sys.exit(0)
##########################################################################################

def Quit(root):
# Quits the program and processes
	root.destroy()
	sys.exit(0)	

##########################################################################################

def WriteFile():
    text.config(state=NORMAL)
    text.insert(INSERT,"Creating N Body Distribution...\n")
    text.see(INSERT)
    text.config(state=DISABLED)
    text.grid()
    for i in range(7):
        if i == 3:
            files.write(struct.pack("i",0))
        else:
            files.write(struct.pack("i",Header[i]))
    for i in range(7,15):
        files.write(struct.pack("d",Header[i]))
    for i in range(15,26):
        if i == 19:
            files.write(struct.pack("i",0))
        else:
            files.write(struct.pack("i",Header[i]))
    for i in range(26,31):
        files.write(struct.pack("d",Header[i]))
    for i in range(31,53):
        files.write(struct.pack("i",Header[i]))
# Position Creator
    files.write(struct.pack("i",NumberOfObjects+1))
# Objects
    text.config(state=NORMAL)
    text.insert(INSERT,"\nCreating Object Positions...\n")
    text.see(INSERT)
    text.config(state=DISABLED)
    text.grid()
    for l in range(NumberOfObjects):
        files.write(struct.pack("f",XPosition[l]))
        files.write(struct.pack("f",YPosition[l]))
        files.write(struct.pack("f",ZPosition[l]))
# Main Object
    text.config(state=NORMAL)
    text.insert(INSERT,"\nCreating Main Position...\n")
    text.see(INSERT)
    text.config(state=DISABLED)
    text.grid()
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("i",NumberOfObjects+1))
# Velocities
    files.write(struct.pack("i",NumberOfObjects+1))
# Objects
    text.config(state=NORMAL)
    text.insert(INSERT,"\nCreating Objects Velocities...\n")
    text.see(INSERT)
    text.config(state=DISABLED)
    text.grid()
    for d in range(0,7):
        files.write(struct.pack("f",float(365.25*XVelocity[d])))
        files.write(struct.pack("f",float(365.25*YVelocity[d])))
        files.write(struct.pack("f",float(365.25*ZVelocity[d])))
    for d in range(7,NumberOfObjects):
        files.write(struct.pack("f",float(XVelocity[d])))
        files.write(struct.pack("f",float(YVelocity[d])))
        files.write(struct.pack("f",float(ZVelocity[d])))
# Main Object
    text.config(state=NORMAL)
    text.insert(INSERT,"\nCreating Main Velocities...\n")
    text.see(INSERT)
    text.config(state=DISABLED)
    text.grid()
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("i",NumberOfObjects+1))
# Particle ID
    files.write(struct.pack("i",NumberOfObjects+1))
    for i in range(NumberOfObjects+1):
        files.write(struct.pack("I",int(i+1)))
    files.write(struct.pack("i",NumberOfObjects+1))
# Particle Mass
    files.write(struct.pack("i",NumberOfObjects))
    for s in range(NumberOfObjects):
        files.write(struct.pack("f",ObjectMass[s]))
    files.write(struct.pack("i",NumberOfObjects))
    text.config(state=NORMAL)
    text.insert(INSERT,"\nDistribution Created!\n")
    text.see(INSERT)
    text.config(state=DISABLED)
    text.grid()
    files.close()
    global ValidateButton
    ValidateButton = Button(root,text='Validate Data')
    ValidateButton.bind('<Return>',trydata)
    ValidateButton.bind('<KP_Enter>',trydata)
    ValidateButton.bind('<Button-1>',trydata)
    ValidateButton.grid()

##########################################################################################

def ValidateData():
    with open(filename, mode='rb') as file:
		    fileContent = file.read()
    answer = 1
    while(int(answer) != 0):
        if int(answer) == 1:
            bitlength = struct.unpack("i",fileContent[:4])
            Npart = struct.unpack("iiiiii",fileContent[4:28])
            totalN = sum(Npart)
            Massarr = struct.unpack("dddddd", fileContent[28:76])
            Time = struct.unpack("d", fileContent[76:84])
            RedShift = struct.unpack("d", fileContent[84:92])
            FlagSfr = struct.unpack("i",fileContent[92:96])
            FlagFeedBack = struct.unpack("i",fileContent[96:100])
            Nall = struct.unpack("iiiiii",fileContent[100:124])
            FlagCooling = struct.unpack("i",fileContent[124:128])
            NumFiles = struct.unpack("i",fileContent[128:132])
            BoxSize= struct.unpack("d", fileContent[132:140])
            Omega0 = struct.unpack("d", fileContent[140:148])
            OmegaLambda = struct.unpack("d", fileContent[148:156])
            HubbleParam = struct.unpack("d", fileContent[156:164])
            FlagAge = struct.unpack("i",fileContent[164:168])
            FlagMetals = struct.unpack("i",fileContent[168:172])
            NallHW = struct.unpack("i",fileContent[172:176])
            flag_entr_ics = struct.unpack("i",fileContent[176:180])
            unused = struct.unpack("iiiiiiiiiiiiiiiiiiiii",fileContent[180:bitlength[0]+8])
            data_answer = 1
            totalN = sum(Npart)
            currentlength = bitlength[0]+12
            for i in range(totalN):
                pos = struct.unpack("fff", fileContent[currentlength:currentlength+12])
                currentlength = currentlength + 12
            currentlength = currentlength + 8
            for i in range(totalN):
                velo = struct.unpack("fff", fileContent[currentlength:currentlength+12])
                currentlength = currentlength + 12
            currentlength = currentlength + 8
            for i in range(totalN):
                ID = struct.unpack("I", fileContent[currentlength:currentlength+4])
                currentlength = currentlength + 4
            currentlength = currentlength + 8
            for i in range(totalN-2):
                mass = struct.unpack("f", fileContent[currentlength:currentlength+4])
                currentlength = currentlength + 4
            answer = 0
        file.close()
def trydata(event):
	text.config(state=NORMAL)
	text.insert(INSERT,"\nVerifying IC File...\n")
	text.see(INSERT)
	text.config(state=DISABLED)
	text.grid()
	try:
		ValidateData()
		text.config(state=NORMAL)
		text.insert(INSERT,"\nIC File Complete.\n")
		text.see(INSERT)
		text.config(state=DISABLED)
		text.grid()
		ValidateButton.destroy()
		global SimulateButton
		SimulateButton = Button(root,text="Begin Simulation",command=Simulate)
		SimulateButton.grid()
		global RestartSimulation
		RestartSimulation = Button(root,text="Restart Simulation",command=RestartSimulate)
		RestartSimulation.grid()
	except struct.error:
		text.config(state=NORMAL)
		text.insert(INSERT,"\nIC File Incomplete.\n")
		text.see(INSERT)
		text.config(state=DISABLED)
		text.grid()
##########################################################################################
		
def Simulate():
	text.config(state=NORMAL)
	text.insert(INSERT,"\nBeginning Gadget2 Simulation...\n")
	text.see(INSERT)
	text.config(state=DISABLED)
	text.grid()
	os.chdir("/home/quinn/documents/research/Gadget/Gadget-2.0.7/Gadget2/")
	gadget=Popen(['LD_LIBRARY_PATH=/usr/local/lib mpirun -np 6 ./Gadget2 randnbody.param'],shell=True)
##########################################################################################

def RestartSimulate():
	text.config(state=NORMAL)
	text.insert(INSERT,"\nRestarting Gadget2 Simulation...\n")
	text.see(INSERT)
	text.config(state=DISABLED)
	text.grid()
	os.chdir("/home/quinn/documents/research/Gadget/Gadget-2.0.7/Gadget2/")
	gadget=Popen(['LD_LIBRARY_PATH=/usr/local/lib mpirun -np 6 ./Gadget2 randnbody.param 1'],shell=True)
##########################################################################################

# Opens GSPLASH CREATES PNG files
def Graph():
    try:
        text.config(state=NORMAL)
        text.insert(INSERT,"Opening GSplash Data Visualtion...\n")
        text.see(INSERT)
        text.config(state=DISABLED)
        text.grid()
        try:
		    os.chdir("/media/MyPassport/NBody")
		    gsplash=Popen(["gsplash snapshot_***"], shell=True)
		    MovieButton = Button(root,text="Convert PNG2MP4",command=MovieMaker)
		    MovieButton.grid(row=3,column=4)
        except OSError:
            text.insert(INSERT,"Folder Does Not Exist...\n")
    except IOError:
        text.config(state=NORMAL)
        text.insert(INSERT,"There Are No GSplash Files To Visualize.\n")
        text.see(INSERT)
        text.config(state=DISABLED)
        text.grid()
##########################################################################################

## Opens FFMPEG CREATES MP4 movie
#
def MovieMaker():
	try:
		os.path.isfile('/media/MyPassport/NBody/splash_0000.png')
		makefilm = True
	except IOError:
		text.config(state=NORMAL)
		text.insert(INSERT,"There Are No Splash Files To Convert.\n")
		text.see(INSERT)
		text.config(state=DISABLED)
		text.grid()
	if makefilm == True:
		text.config(state=NORMAL)
		text.insert(INSERT,"Opening FFMPEG...\n")
		text.see(INSERT)
		text.config(state=DISABLED)
		text.grid()
		os.chdir("/media/MyPassport/NBody/")
		gsplash=Popen(["ffmpeg -i splash_%04d.png random.mp4"], shell=True)
##########################################################################################
# MAIN LOOP

GUIWindow()
GetFileName()
GetHeader()
GetInputFile()
root.mainloop()
