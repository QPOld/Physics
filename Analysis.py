#Michael Quinn Parkinson - Stability Analysis
# This is a work in progress. The analysis of stability for a circumbinary disk
# will probably change. Though this file is the base for any corrections.
import struct
import glob
import random
import math
import csv
import time
import numpy
#Unpacks data from snapshot files. It goes bit by bit and unpacks position, velocity, and particle ID. Any data can be retrieve if needed.
# Check the gadget2 manual for bit by bit object locations
def UnPackData(filename):
    print "\nUnpacking Snapshot...\n"
    Position = []
    Velocity = []
    PartID = []
    with open(filename, mode='rb') as file:
        fileContent = file.read()
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
    currentlength = bitlength[0]+12
    print "\nSaving Positions...\n"
    #   Gets All Position Data
    for i in range(totalN):
        pos = struct.unpack("fff", fileContent[currentlength:currentlength+12])
        X = pos[0]  # X position
        Y = pos[1]  # Y Position
        Z = pos[2]  # Z Position
        Position.append([X,Y,Z])
        currentlength = currentlength + 12
    print "Positions Saved.\n"
    currentlength = currentlength + 8
    print "\nSaving Velocities...\n"
    for j in range(totalN):
        velo = struct.unpack("fff", fileContent[currentlength:currentlength+12])
        Vx = velo[0]
        Vy = velo[1]
        Vz = velo[2]
        Velocity.append([Vx,Vy,Vz])
        currentlength = currentlength + 12
    currentlength = currentlength + 8
    print "\nVelocities Saved.\n"
    #   Gets All Planet, Asteroid, and Solar IDs
    for k in range(totalN):
        ID = struct.unpack("I", fileContent[currentlength:currentlength+4])
        PartID.extend([ID[0]])
        currentlength = currentlength + 4
    currentlength = currentlength + 8
    for l in range(totalN-1):
        mass = struct.unpack("f", fileContent[currentlength:currentlength+4])
        currentlength = currentlength + 4
    file.close()
    print "Unpacking Completed.\n"
    return Position, Velocity, PartID
# Performs a 6 dimensional monte carlo integration
def MonteCarlo(Position,Velocity,Volume):
    N = 1000
    count_y = 0
    count_z = 0
    count_vx = 0
    count_vy = 0
    count_vz = 0
    X = []
    Y = []
    Z = []
    Vx = []
    Vy = []
    Vz = []
    for q in range(len(Position)):
        X.extend([Position[q][0]])
        Y.extend([Position[q][1]])
        Z.extend([Position[q][2]])
        Vx.extend([Velocity[q][0]])
        Vy.extend([Velocity[q][1]])
        Vz.extend([Velocity[q][2]])
    for i in range(N):
        val_x = random.choice(X)
        ind = X.index(val_x)
        val_vx = Vx[ind]
        val_vy = Vy[ind]
        val_vz = Vz[ind]
        val_y = Y[ind]
        val_z = Z[ind]
        if val_y > 0.0 and val_vx > 0.0 and val_vy > 0.0:
            count_y = count_y + val_y
            count_vx = count_vx + val_vx
            count_vy = count_vy + val_vy
        if val_z > 0.0 and val_vz > 0:
            count_z = count_z + val_z
            count_vz = count_vz + val_vz
    count_y = count_y / N
    count_z = count_z / N
    count_vx = count_vx / N
    count_vy = count_vy / N
    count_vz = count_vz / N
    if count_z == 0.0 and count_vz == 0:
        Vol = count_y*count_vx*count_vy
    else:
        Vol = count_y*count_z*count_vx*count_vy*count_vz
    Volume.extend([2.0*Vol])
    return Volume
def Stability(Volume,Rmin,Inc,Semi,Direct_Path):
    Vol_Path = Direct_Path.replace("Data_","")
    N = len(Volume)
    mean = sum(Volume)/N
    for j in range(N):
        Volume[j] = math.log(Volume[j]/mean)
    Vol_Path = Vol_Path + '/Vol_Data.dat'
    with open(Vol_Path,'a+') as file:
        Data = csv.writer(file)
        for k in range(1,N-1):
            dif_V = math.fabs((Volume[k] - Volume[k-1]))
            if dif_V > 1.0:
                Data.writerow(["UNSTABLE",str(Rmin),str(Inc),str(Semi)])
                break
            if k == N-2:
                Data.writerow(["STABLE",str(Rmin),str(Inc),str(Semi)])   
def GetParam(Direct_Path):
    Param_Path = Direct_Path.replace("Data/Data_","")+"/Parameter"     
    h_r, N_Rmin, h_i, N_Inc, h_s, N_Semi = numpy.loadtxt(Param_Path, unpack = True)
    return h_r, N_Rmin, h_i, N_Inc, h_s, N_Semi
