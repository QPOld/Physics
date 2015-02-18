#Michael Quinn Parkinson - Automated Running
# This program will create directories, IC files, and run gadget2.
#Before gadget2 runs it will update the parameter file.
#When gadget2 is finished running and order file will be created.
# All functions that are associated with the gadget2 are in this file.
#
#   Thesis.py - SetParam.py - Analysis.py - AutoRun.py
# CHANGE DIRECTORY PATH FOR LINUX
# CALCULATE THE COMPUTATION TIME FOR T = 50 YEARS
print "\nChecking Default Installed Modules...\n"
import struct
import array
import random
import time
import os
import sys
import math
import csv
import math
import signal
import glob
print "\nDefault Modules Located and Imported.\n"
from subprocess import Popen
print "\nChecking Specific Installed Modules...\n"
Stars = 2
# NUMPY For Data Implementation 
try:
	import numpy
	print "\nNumPy Module Installed.\n"
except ImportError:
	print "Please Install NumPy."
	sys.exit(0)
    

def Make(Direct_,File_Path,Head_Path):
    if not os.path.exists(Direct_):     #checks if directory already exists
        print "\nCreating Directory...\n",Direct_       #creates directory if it does not exist
        os.makedirs(Direct_)       #creates directory if it does not exist
    if not os.path.isfile(File_Path):       #checks if inpute file exists
        print "\nCreating Input File...\n"
        open(File_Path,'w+').close()        #creates input file if it does not exist
    if not os.path.isfile(Head_Path):     #checks if header file exists
        print "\nCreating Header File...\n"
        open(Head_Path,'w+').close()        #creates header file if it does not exist
def Create_Input(File_Path,Rmin,Inc):
    N = 10000       # number of planetesimals --> may change
    TotalMass = 0.0001      #total disk mass 10^{-4} solar masses
    print "\nWriting IC File...\n"
    DelR = 25       #the difference between the inner and outer disk radius
    Rmax = Rmin + DelR
    deltaR = 0.01       #the differential width of an annulus.
    p = 3.0/2.0        #the power of the number density
    count = 0      #counts the number of planetesimals in a differential annulus
    Stars = 2       # the number of stars in teh system
    with open(File_Path,'a') as datafile:
        datawrite = csv.writer(datafile,delimiter='\t')     #writes the input file
        while count <= N:        #the number of planetesimals is less than or equal to the total number of planetesimals
            for j in range(int((Rmax - Rmin)/deltaR)):
                R1 = Rmin + j*deltaR        #inner disk radius
                R2 = Rmin + (j+1)*deltaR        #outer disk radius
                n = int(round(-((N*(-1 + p)*(R1**(1 - p) - R2**(1 - p))*(Rmax**p)*(Rmin**p))/((1 - p)*((Rmax**p)*Rmin - Rmax*(Rmin**p))))))     #number of objects
                for i in range(0,n):
                    r = random.uniform(R1,R2)
                    theta = random.uniform(0.0,2.0*math.pi)
                    degree = Inc
                    Inc = degree*math.pi/180.0
                    x = r*math.cos(theta)
                    y = r*math.sin(theta)
                    z = y*math.tan(Inc)     #the z is given such that a plane exist with a given inclination wrt x-y plane.
                    #calculates circular orbits
                    vx = math.sqrt(Stars*39.4)*( y*math.fabs(y) + z*math.fabs(z) ) / ( math.pow(( x**(2.0) + y**(2.0) + z**(2.0) ),1.0/4.0)*math.sqrt( y**(4.0) + z**(4.0) +( y**(2.0) + z**(2.0) )*( x**(2.0) ) + 2.0*y*z*math.fabs(y)*math.fabs(z) ) )
                    vy = -math.sqrt(Stars*39.4)*( x*math.fabs(y) ) / ( math.pow(( x**(2.0) + y**(2.0) + z**(2.0) ),1.0/4.0)*math.sqrt( y**(4.0) + z**(4.0) +( y**(2.0) + z**(2.0) )*( x**(2.0) ) + 2.0*y*z*math.fabs(y)*math.fabs(z) ) )
                    vz = -math.sqrt(Stars*39.4)*( x*math.fabs(z) ) / ( math.pow(( x**(2.0) + y**(2.0) + z**(2.0) ),1.0/4.0)*math.sqrt( y**(4.0) + z**(4.0) +( y**(2.0) + z**(2.0) )*( x**(2.0) ) + 2.0*y*z*math.fabs(y)*math.fabs(z) ) )
                    Mass = TotalMass/N      #equal mass planetesimals
                    DATA = [Mass,x,y,z,vx,vy,vz]
                    datawrite.writerow(DATA)
                    count += 1
                    if count > N:
                        break
                    else:
                        continue
def Create_Header(Head_Path,File_Path):
    print "\nCreating Header File...\n"
    ObjectMass,XPosition,YPosition,ZPosition,XVelocity,YVelocity,ZVelocity = numpy.loadtxt(File_Path, unpack = True)        #Loads inputfile
    Stars = 2
    with open(Head_Path,'a') as headfile:
        headwrite = csv.writer(headfile,delimiter=' ')
        #header file reference gadget2 manual for location defintions
        data = [256,0,0,0,len(XPosition),Stars,0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0,0,0,0,0,len(XPosition),Stars,0,0,1,0.0,0.0,0.0,0.0,0,0,0,0,0,0,0,0,0.0,0,0,0,0.0,0,0,0.0,0,0.0,0,0,0,0,0,256]
        headwrite.writerow(data)
    print "\nDone\n"
def Create_IC(Direct_,Head_Path,File_Path,Semi):
    FileName = Direct_ +'/System.dat'
    Header = numpy.loadtxt(Head_Path, unpack = True)        #loads header file
    ObjectMass,XPosition,YPosition,ZPosition,XVelocity,YVelocity,ZVelocity = numpy.loadtxt(File_Path, unpack = True)        #loads input file
    NumberOfObjects = len(ObjectMass)
    files = open(FileName,mode='wb+')
    print "\nCreating IC File...\n"
    #creates initial conidition file reference gadget2 manual for location defintions
    #max stars is two
    # loads header information
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
    files.write(struct.pack("i",NumberOfObjects+Stars))
    # Object position information
    for l in range(NumberOfObjects):
        files.write(struct.pack("f",XPosition[l]))
        files.write(struct.pack("f",YPosition[l]))
        files.write(struct.pack("f",ZPosition[l]))
    # Main Object position information
    X1 = Semi
    X2 = -X1
    V1 = -math.sqrt(39.4*X1/(X1 - X2)**2.0 )
    V2 = -V1
    files.write(struct.pack("f",X1))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",X2))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("i",NumberOfObjects+Stars))
    # Velocities
    files.write(struct.pack("i",NumberOfObjects+Stars))
    # Object velocity information
    for d in range(0,NumberOfObjects):
        files.write(struct.pack("f",float(XVelocity[d])))
        files.write(struct.pack("f",float(YVelocity[d])))
        files.write(struct.pack("f",float(ZVelocity[d])))
    # Main Object velocity information
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",V1))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("f",V2))
    files.write(struct.pack("f",0.0))
    files.write(struct.pack("i",NumberOfObjects+Stars))
    # Particle ID includes stars
    files.write(struct.pack("i",NumberOfObjects+Stars))
    for i in range(NumberOfObjects+Stars):
        files.write(struct.pack("I",int(i+1)))
    files.write(struct.pack("i",NumberOfObjects+Stars))
    # Particle Mass does not include stars
    files.write(struct.pack("i",NumberOfObjects))
    for s in range(NumberOfObjects):
        files.write(struct.pack("f",ObjectMass[s]))
    files.write(struct.pack("i",NumberOfObjects))
    files.close()
    print "\nDone\n"
def Update_Param(Direct_):
    Param_Path = '/Users/quinn/Documents/Research/Thesis/Gadget-2.0.7/Gadget2/System.param'
    with open(Param_Path,'r') as file:
        data = file.readlines()
    data[2] = 'InitCondFile'+ "\t" + Direct_ +'/System.dat'+'\n'        # new initial condition file location for gadget2
    data[3] = 'OutputDir' + '\t' + Direct_  + '\n'      #new output locaiton for gadget2
    with open(Param_Path,'w') as file:
        file.writelines(data)     
def Simulate():
    Param_Path = '/Users/quinn/Documents/Research/Thesis/Gadget-2.0.7/Gadget2/'
    os.chdir(Param_Path)
    # gadget=Popen(['LD_LIBRARY_PATH=/usr/local/lib mpirun -np 6 ./Gadget2 randnbody.param'],shell=True)
    gadget=Popen(['mpirun -np 4 ./Gadget2 System.param'],shell=True)
def Order(Direct_):
    N_Files = len(glob.glob(Direct_ + '/snapshot_*'))
    Order_Path = Direct_ +'/splash.filenames'
    print "\nOrdering Snapshot Files...\n"
    with open(Order_Path,'w+') as DataFile:
        Data = csv.writer(DataFile,delimiter='\n')
        for i in range(N_Files):
            Name = 'snapshot_' + '{0:0{width}}'.format(i,width=3)
            Data.writerow([Name])
    print "\nOrdering Completed.\n"
def GetParam(Direct_Path):
    Param_Path = Direct_Path.replace("Data/Data_","")+"/Parameter"     
    h_r, N_Rmin, h_i, N_Inc, h_s, N_Semi = numpy.loadtxt(Param_Path, unpack = True)
    return h_r, N_Rmin, h_i, N_Inc, h_s, N_Semi
