#Michael Quinn Parkinson - Sets Gadget2 Parameters
# This file is a bunch of functions that are just answer to questions about how
# the simulation will run.
def Set():
    print "\n"
    while True:
        try:
            h_r = raw_input("What Is The Step Size For The Inner Disk Radius? (default = 0.75) ")
            if h_r == "":
                h_r = 0.75
            else:
                h_r = float(h_r)
        except ValueError:
            continue
        else:
            break
    while True:
        try:
            N_Rmin = raw_input(">>>How Many Steps For The Inner Disk Radius? (default = 1) ")
            if N_Rmin == "":
                N_Rmin = 1.0
            else:
                N_Rmin = float(N_Rmin)
        except ValueError:
            continue
        else:
            break
    while True:
        try:
            h_i = raw_input("What Is The Step Size For The Disk Inclination? (default = 10.0) ")
            if h_i == "":
                h_i = 10.0
            else:
                h_i = float(h_i)
        except ValueError:
            continue
        else:
            break
    while True:
        try:
            N_Inc = raw_input(">>>How Many Steps For The Disk? (default = 1) ")
            if N_Inc == "":
                N_Inc = 1.0
            else:
                N_Inc = float(N_Inc)
        except ValueError:
            continue
        else:
            break
    while True:
        try:
            h_s = raw_input("What Is The Step Size For The Binary Semi Major Axis? (default = 0.1) ")
            if h_s == "":
                h_s = 0.1
            else:
                h_s = float(h_s)
        except ValueError:
            continue
        else:
            break
    while True:
        try:
            N_Semi = raw_input(">>>How Many Step For The Binary Semi Major Axis? (default = 1) ")
            if N_Semi == "":
                N_Semi = 1.0
            else:
                N_Semi = float(N_Semi)
        except ValueError:
            continue
        else:
            break
    print "\n"
    return h_r, N_Rmin, h_i, N_Inc, h_s, N_Semi
