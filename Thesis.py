# Michael Quinn Parkinson - Terminal Based IC Creator
# This program will increment inclination, inner disk radius, and binary seperation.
# It will then generate all IC files and update the Gadget2 System Parameter file.
# It will auto run and stop gadget2. This code is used for an automated simulation.
# After the simulation has completed a file will be created with an ordered list.
# This is done to allow for easy data visualization with gsplash.
import AutoRun
import Analysis
import SetParam
import glob
import csv
import numpy
quit = 0
print "\nPROGRAM WORKS WITH NEW FOLDERS ONLY!\n"
while (quit == 0):
    try:
        Answer = int(raw_input("Run Gadget2 (1)\n Analysis (2)\n Set Parameters (3)\n Quit (4)\n "))
        if Answer == 1:
            pass
            Direct_Path = '/Users/quinn/Documents/Research/Thesis/Scripts/Data/Data_'   #default mac folder path
            File_Name = '/input-14.dat'     #default input file name
            Head_Name = '/header-10.dat'    #defualt header file name
            h_r, N_Rmin, h_i, N_Inc, h_s, N_Semi = AutoRun.GetParam(Direct_Path)        #Open the Parameter file
            for i in range(int(N_Rmin)):#10
                print "\nPicking Parameters...\n"
                Rmin = 1 + i*h_r        #increments inner disk radius
                for j in range(int(N_Inc)):#10
                    Inc = 0.0 + j*h_i       #increments disk inclination
                    for k in range(int(N_Semi)):#10
                        Semi = 0.1 + k*h_s      #increments binary semi major axis
                        Direct_ = Direct_Path + str(Rmin) + '_' + str(Inc) + '_' + str(Semi)        #path to outpute directory
                        print "\nWriting Initial Condition File...\n"
                        print "\n","R_min: ",Rmin," Inclin: ",Inc," SM Axis: ",Semi,"\n"
                        File_Path = Direct_ + File_Name     #path to input file
                        Head_Path = Direct_ + Head_Name     #path to header file
                        AutoRun.Make(Direct_,File_Path,Head_Path)       #creates directory and files
                        AutoRun.Create_Input(File_Path,Rmin,Inc)        #fills in input file
                        AutoRun.Create_Header(Head_Path,File_Path)      #fills in header file
                        AutoRun.Create_IC(Direct_,Head_Path,File_Path,Semi)     #creates initial condition file for gadget2
                        AutoRun.Update_Param(Direct_)       #corrects the parameter file for gadget2
                        print "\nStarting Simulation...\n"
                        AutoRun.Simulate()      #starts simulation
                        # real time for simulation ---> Change this
                        delt = 15      #time in seconds
                        ts = time.time()
                        tf = ts + delt
                        t = 0
                        while t <= tf:
                            t = time.time()
                        os.chdir(Direct_)       #changes directory to output directory
                        Popen(['echo > stop'],shell=True)       #Ends simulation
                        print "Stopping Simulation."
                        time.sleep(1)
                        AutoRun.Order(Direct_)
            print "\nSimulation Done!\n"
        if Answer == 2:
            Direct_Path = '/Users/quinn/Documents/Research/Thesis/Scripts/Data/Data_'   #default mac folder path
            h_r, N_Rmin, h_i, N_Inc, h_s, N_Semi = Analysis.GetParam(Direct_Path)        #Open the Parameter file 
            for i in range(int(N_Rmin)):
                print "\nPicking Parameters...\n"
                Rmin = 1 + i*h_r        #increments inner disk radius
                for j in range(int(N_Inc)):
                    Inc = 0.0 + j*h_i       #increments disk inclination
                    for k in range(int(N_Semi)):
                        Semi = 0.1 + k*h_s      #increments binary semi major axis
                        Direct_ = Direct_Path + str(Rmin) + '_' + str(Inc) + '_' + str(Semi)        #path to outpute directory
                        print "\n","R_min: ",Rmin," Inclin: ",Inc," SM Axis: ",Semi,"\n"
                        N_Files = len(glob.glob(Direct_ + '/snapshot_*'))
                        if N_Files != 0:
                            Volume = []
                            for n in range(N_Files):
                                Name = '/snapshot_' + '{0:0{width}}'.format(n,width=3)
                                filename = Direct_ + Name
                                print "\nFile: \n",Name
                                Position,Velocity,PartID = Analysis.UnPackData(filename)     #Unpacks Data for Analysis
                                Volume = Analysis.MonteCarlo(Position,Velocity,Volume)       #Monte Carlo Integration 
                            Analysis.Stability(Volume,Rmin,Inc,Semi,Direct_Path)
                        else:
                            print "\nNo Snapshots with:" , "\n","R_min: ",Rmin," Inclin: ",Inc," SM Axis: ",Semi,"\n"
        if Answer == 3:
            h_r, N_Rmin, h_i, N_Inc, h_s, N_Semi = SetParam.Set()
            data = [h_r,N_Rmin,h_i,N_Inc,h_s,N_Semi]
            numpy.savetxt('Parameter',data,delimiter='\t',newline=" ")
        if Answer == 4:
            quit = 1
    except ValueError:
        pass
