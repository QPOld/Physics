#Michael Quinn Parkinson - SDSS IC Creator And Analysis Program
# This program import SDSS data of RA,Dec, and Redshift for every galaxy
# in the SDSS databass as of DS7. It will create an IC file for gadget2.
# It will also calculate the two point correlation function for the subset
#of data from the SDSS

# SDSS RA DEC REDSHIFT FILE
import csv
import math
import numpy
import matplotlib
import pylab
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# TEST RUN OF SQL W NOQSO
# SELECT 
#    ra,dec,z_noqso
# FROM
#    SpecObjAll
# WHERE
#    class = 'Galaxy'
#    and zWarning_noqso = 0
#    and z_noqso > 0.0002
#    and z_noqso < 0.3

# TEST RUN OF SQL W QSO
# SELECT 
#    ra,dec,z
# FROM
#    SpecObjAll
# WHERE
#    class = 'Galaxy'
#    and zWarning = 0
#    and z > 0.0002
#    and z < 0.3

# RA DEC REDSHIFT
# Converts RA Dec and Redshift Into A Cartesian Coordinate System
# Align RA 0 degree with X axis allow it to open into Y
# Dec is pi/2 - dec = phi the polar angle
def GetPosition(filename,MaxRedShift,MinDec,MaxDec):
    c = 299792.458
    H0 = 71
    with open(filename,'r') as file:
        ReadData = csv.reader(file,delimiter=',')
        Position = []
        print "\nBeginning Coordinate Transformation...\n"
        for row in ReadData:
			if (float(row[1]) >= MinDec) and (float(row[1]) <= MaxDec):
#				RedShift = c*abs(float(row[2]))/H0
				RedShift = abs(float(row[2]))
				x = RedShift*math.sin(math.radians(float(row[0])))*math.cos(math.pi/2.0 - math.radians(float(row[1])))
				y = RedShift*math.sin(math.radians(float(row[0])))*math.sin(math.pi/2.0 - math.radians(float(row[1])))
				z = RedShift*math.cos(math.radians(float(row[0])))
				if RedShift <= MaxRedShift:
					Position.append([x,y,z])
				else:
					continue
        print "\nCoordinate Transformation Into Cartesian RedShift Space Complete.\n"
    return Position
# Plots the Cartesian RedShift Space Distribution
def PlotPosition(Position):
#	fig = plt.figure()
#	ax = fig.add_subplot(111, projection='3d')
	NumberOfData = len(Position)
	print "\nNumber Of Objects In Survey", NumberOfData,"\n"
	for i in range(NumberOfData):
#		ax.scatter(Position[i][0],Position[i][1],Position[i][2])
		matplotlib.pyplot.scatter(Position[i][0],Position[i][1])
		matplotlib.pyplot.title("Galactic Distribution")
		matplotlib.pyplot.xlabel("X-RedShift")
		matplotlib.pyplot.ylabel("Y-Redshift")
# Calculates the Radius of the Galaxy to us then Iterates through to Calculate
# The Differences in the Radius distance
def Correlation(Position,MaxRedShift,NumberOfBins,SeperationDistance):
    Store = numpy.zeros((NumberOfBins,2))
    Annulus = MaxRedShift/NumberOfBins
    Step = Annulus
    NumberOfData = len(Position)
    print "\nNumber Of Objects In Survey", NumberOfData,"\n"
    for i in range(NumberOfBins):
        print "Bin Number: ", i+1 ,'\t', " RedShift Annulus Size: ", Annulus
        for j in range(NumberOfData):
            for k in range((j+1),NumberOfData-1):
                FirstRadius = ( (Position[j][0])**(2.0) + (Position[j][1])**(2.0) + (Position[j][2])**(2.0) )**(1.0/2.0)
                SecondRadius = ( (Position[k][0])**(2.0) + (Position[k][1])**(2.0) + (Position[k][2])**(2.0) )**(1.0/2.0)
                Difference = ((Position[j][0] - Position[k][0])**(2.0) + (Position[j][1] - Position[k][1])**(2.0) + (Position[j][2] - Position[k][2])**(2.0))**(1.0/2.0)
                if (FirstRadius > (Annulus - Step)) and (FirstRadius <= Annulus) and (SecondRadius > (Annulus - Step)) and (SecondRadius <= Annulus):
                    if Difference <= SeperationDistance:
                        Store[i][0] += 1
                        Store[i][1] = Annulus
                    else:
                        continue
                else:
                    continue
        try:
            matplotlib.pyplot.scatter(math.log10(Store[i][1]),math.log10(Store[i][0]))
            matplotlib.pyplot.title("Two Point Correlation Function For The SDSS")
            matplotlib.pyplot.xlabel("Log10(RedShift)")
            matplotlib.pyplot.ylabel("Number Of Pairs")
        except ValueError:
            print "\nMissing Values...\n"
        Annulus = Annulus + Step
# 
def InitialCondition(Position,DataName):
	print "\nNumber Of Objects:\n"
	print len(Position)
	with open(DataName,'w') as datafile:
		datawrite = csv.writer(datafile,delimiter='\t')
		NumberOfData = len(Position)
		for i in range(NumberOfData):
			DATA = [1.0,Position[i][0]+4216.79207424,Position[i][1]+4216.79207424,Position[i][2]+4216.79207424,0.0,0.0,0.0]
			datawrite.writerow(DATA)
# 
def GetParameters():
	try:
    		MaxRedShift = float(raw_input("\nWhat Is The Maximum Redshift: \n"))
	except ValueError:
		print "Invalid Maximum Redshift..."
	try:
    		SeperationDistance = float(raw_input("\nWhat Is The Maximum Seperation Redshift: \n"))
	except ValueError:
		print "Invalid Seperation Redshift"
	print "\nThe Optimal Number Of Bins Is: "
	NumberOfBins = int( MaxRedShift / SeperationDistance ) - 1
	if NumberOfBins <= 0:
		NumberOfBins = 1
		print "\nDefault \n" , NumberOfBins
	else:
		print NumberOfBins
	try:
    		MinDec = float(raw_input("\nWhat Is The Minimum Declination: \n"))
	except ValueError:
		print "Invalid Minimum Declination"
	try:
    		MaxDec = float(raw_input("\nWhat Is The Maximum Declination: \n"))
	except ValueError:
		print "Invalid Maximum Declination"
	return MaxRedShift,SeperationDistance,NumberOfBins,MinDec,MaxDec
# User Selects Which Function To Call
def SurveyOptions(Position,MaxRedShift,NumberOfBins,SeperationDistance,DataName):
    Answer = int(raw_input("\n Plot Position (1) \n Calculate Correlation (2) \n Create Initial Condition File (3) \n Quit (4) \n"))
    if Answer == 1:
        PlotPosition(Position)
    if Answer == 2:
        Correlation(Position,MaxRedShift,NumberOfBins,SeperationDistance)
    if Answer == 3:
        InitialCondition(Position,DataName)
    if Answer == 4:
        sys.exit()
##
###
####   
### 
##
#
# DOUBLE CHECK RESULT CSV FOR CORRECT DATA POINTS
if __name__ == '__main__':
	try:
		print "\nSloan Digital Sky Survey Data Analysis Program\n"
		FileName ='/Users/quinn/Documents/Research/NBody/corr/position_000'
		DataName = '/Users/quinn/Documents/Research/NBody/input4-7.dat' 
		MaxRedShift,SeperationDistance,NumberOfBins,MinDec,MaxDec = GetParameters()
		Position = GetPosition(FileName,MaxRedShift,MinDec,MaxDec)
		print "\nMaximum Position:\n"
		print max(max(l) for l in Position)
		print "\nMinimum Position:\n"
		print min(min(l) for l in Position)
		while True:
			SurveyOptions(Position,MaxRedShift,NumberOfBins,SeperationDistance,DataName)
			matplotlib.pyplot.show()
	except KeyboardInterrupt:
		print "\nCrtl-C Caught Closing Processes...\n"
		matplotlib.pyplot.show()
