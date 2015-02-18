#Michael Quinn Parkinson - Three Body RK4 Code
# Calculates the trajectories of N particles around a binary
# Each particle only interacts with the binary graviatationally.
# This code test stable orbits for an object in orbit around the
# center of mass of a binary stellar system.
# The Code uses a fourth order Runge-Kutta Method.

import math
import random
import numpy
import matplotlib
import pylab

g = 39.4 # Gravitational Constant in terms of Solar mass, AU, and Years

m1 = 1.0 # One Solar Mass Star
m2 = 1.0 # One Solar Mass Star
m3 = 10**(-16.0) # Asteroid Like Mass (1 km radius with rho = 3 g/cm^3)

# First Star Position
x1 = 0.25
y1 = 0.0
z1 = 0.0
#First Star Velocity
vx1 = 0.0
vy1 = -14.75
vz1 = 0.0

#Second Star Position
x2 = -0.25
y2 = 0.0
z2 = 0.0
#Second Star Velocity
vx2 = 0.0
vy2 = 14.75
vz2 = 0.0

#Acceleration Functions

#Calculates the acceleration of each of the particles in three dimensions
def m1_ax(x1,y1,z1,x2,y2,z2,x3,y3,z3):# mass one x dimension
    return -(1.0/m1)*( (g*m1*m2*(x1 - x2) )/( (x1 - x2)**(2.0) + (y1 - y2)**(2.0) + (z1 - z2)**(2.0) )**(3.0/2.0) + ( g*m1*m3*(x1 - x3) )/( (x1 - x3)**(2.0) + (y1 - y3)**(2.0) + (z1 - z3)**(2.0) )**(3.0/2.0) )
    
def m1_ay(x1,y1,z1,x2,y2,z2,x3,y3,z3):# mass one y dimension
    return -(1.0/m1)*( (g*m1*m2*(y1 - y2) )/( (x1 - x2)**(2.0) + (y1 - y2)**(2.0) + (z1 - z2)**(2.0) )**(3.0/2.0) + ( g*m1*m3*(y1 - y3) )/( (x1 - x3)**(2.0) + (y1 - y3)**(2.0) + (z1 - z3)**(2.0) )**(3.0/2.0) )
    
def m1_az(x1,y1,z1,x2,y2,z2,x3,y3,z3):# mass one z dimension
    return -(1.0/m1)*( (g*m1*m2*(z1 - z2) )/( (x1 - x2)**(2.0) + (y1 - y2)**(2.0) + (z1 - z2)**(2.0) )**(3.0/2.0) + ( g*m1*m3*(z1 - z3) )/( (x1 - x3)**(2.0) + (y1 - y3)**(2.0) + (z1 - z3)**(2.0) )**(3.0/2.0) )

def m2_ax(x1,y1,z1,x2,y2,z2,x3,y3,z3):# mass two x dimension
    return (1.0/m2)*( (g*m1*m2*(x1 - x2) )/( (x1 - x2)**(2.0) + (y1 - y2)**(2.0) + (z1 - z2)**(2.0) )**(3.0/2.0) - ( g*m2*m3*(x2 - x3) )/( (x2 - x3)**(2.0) + (y2 - y3)**(2.0) + (z2 - z3)**(2.0) )**(3.0/2.0) )

def m2_ay(x1,y1,z1,x2,y2,z2,x3,y3,z3):# mass two y dimension
    return (1.0/m2)*( (g*m1*m2*(y1 - y2) )/( (x1 - x2)**(2.0) + (y1 - y2)**(2.0) + (z1 - z2)**(2.0) )**(3.0/2.0) - ( g*m2*m3*(y2 - y3) )/( (x2 - x3)**(2.0) + (y2 - y3)**(2.0) + (z2 - z3)**(2.0) )**(3.0/2.0) )

def m2_az(x1,y1,z1,x2,y2,z2,x3,y3,z3):# mass two z dimension
    return (1.0/m2)*( (g*m1*m2*(z1 - z2) )/( (x1 - x2)**(2.0) + (y1 - y2)**(2.0) + (z1 - z2)**(2.0) )**(3.0/2.0) - ( g*m2*m3*(z2 - z3) )/( (x2 - x3)**(2.0) + (y2 - y3)**(2.0) + (z2 - z3)**(2.0) )**(3.0/2.0) )

def m3_ax(x1,y1,z1,x2,y2,z2,x3,y3,z3):# mass three x dimension
    return (1.0/m3)*( (g*m1*m3*(x1 - x3) )/( (x1 - x3)**(2.0) + (y1 - y3)**(2.0) + (z1 - z3)**(2.0) )**(3.0/2.0) + ( g*m2*m3*(x2 - x3) )/( (x2 - x3)**(2.0) + (y2 - y3)**(2.0) + (z2 - z3)**(2.0) )**(3.0/2.0) )

def m3_ay(x1,y1,z1,x2,y2,z2,x3,y3,z3):# mass three y dimension
    return (1.0/m3)*( (g*m1*m3*(y1 - y3) )/( (x1 - x3)**(2.0) + (y1 - y3)**(2.0) + (z1 - z3)**(2.0) )**(3.0/2.0) + ( g*m2*m3*(y2 - y3) )/( (x2 - x3)**(2.0) + (y2 - y3)**(2.0) + (z2 - z3)**(2.0) )**(3.0/2.0) )

def m3_az(x1,y1,z1,x2,y2,z2,x3,y3,z3):# mass three z dimension
    return (1.0/m3)*( (g*m1*m3*(z1 - z3) )/( (x1 - x3)**(2.0) + (y1 - y3)**(2.0) + (z1 - z3)**(2.0) )**(3.0/2.0) + ( g*m2*m3*(z2 - z3) )/( (x2 - x3)**(2.0) + (y2 - y3)**(2.0) + (z2 - z3)**(2.0) )**(3.0/2.0) )

# Initial Condition Creator Function
# Creates six arrays of position and velocity N times where N is the number of non interacting test particles
def Test_Particles(N,x1,y1,z1,x2,y2,z2,vx1,vy1,vz1,vx2,vy2,vz2):
    Stars = 10 # For some reason I need to add more velocity
    Pos_Test = []
    Pos_One = []
    Pos_Two = []
    Velo_Test = []
    Velo_One = []
    Velo_Two = []
    for i in range(N):
        Pos_Test.append([])
        Pos_One.append([x1,y1,z1])
        Velo_One.append([vx1,vy1,vz1])
        Pos_Two.append([x2,y2,z2])
        Velo_Two.append([vx2,vy2,vz2])
        for j in range(2):# change to 3 for non coplaner
            Pos_Test[i].extend([random.uniform(-7,7)])
        Pos_Test[i].extend([0]) # Coplaner assumption
        x = Pos_Test[i][0]
        y = Pos_Test[i][1]
        z = Pos_Test[i][2]
        # I derived these formulas. Given any x,y,and z coordinate these formulas will always give the velocities to put a particle in a circular orbit.
        vx = math.sqrt(Stars*39.4)*( y*math.fabs(y) + z*math.fabs(z) ) / ( math.pow(( x**(2.0) + y**(2.0) + z**(2.0) ),1.0/4.0)*math.sqrt( y**(4.0) + z**(4.0) +( y**(2.0) + z**(2.0) )*( x**(2.0) ) + 2.0*y*z*math.fabs(y)*math.fabs(z) ) )
        vy = -math.sqrt(Stars*39.4)*( x*math.fabs(y) ) / ( math.pow(( x**(2.0) + y**(2.0) + z**(2.0) ),1.0/4.0)*math.sqrt( y**(4.0) + z**(4.0) +( y**(2.0) + z**(2.0) )*( x**(2.0) ) + 2.0*y*z*math.fabs(y)*math.fabs(z) ) )
        vz = -math.sqrt(Stars*39.4)*( x*math.fabs(z) ) / ( math.pow(( x**(2.0) + y**(2.0) + z**(2.0) ),1.0/4.0)*math.sqrt( y**(4.0) + z**(4.0) +( y**(2.0) + z**(2.0) )*( x**(2.0) ) + 2.0*y*z*math.fabs(y)*math.fabs(z) ) )
        Velo_Test.append([vx,vy,vz])
    return Pos_Test, Pos_One, Pos_Two, Velo_Test, Velo_One, Velo_Two

t0 = int(raw_input("\nNumber of Iterations? \n"))#Total number of steps to take
NumOfPoints = int(raw_input("\nNumber of Steps For Plotting? \n"))
count = (t0/NumOfPoints) - 1
h = float(raw_input("\nStep Size? \n"))#Step size
N = int(raw_input("\nNumber Of Simultaneous Simulations? \n"))# number of non interacting test particles to simulate

print "\nCreating Initial Conditions...\n"
Pos_Test, Pos_One, Pos_Two, Velo_Test, Velo_One, Velo_Two = Test_Particles(N,x1,y1,z1,x2,y2,z2,vx1,vy1,vz1,vx2,vy2,vz2)
print "\nInitial Conditions Created.\n"
print "\nBeginning Integration...\n"
# RK4 loop

# A Brute force attempt at a RK4 loop
# Not the cleanest way to do this but it works great.
for t in range(0,t0):
    count += 1
    for n in range(0,N):
        #intialize incrementation parameters
        x_1 = Pos_One[n][0]
        y_1 = Pos_One[n][1]
        z_1 = Pos_One[n][2]
    
        x_2 = Pos_Two[n][0]
        y_2 = Pos_Two[n][1]
        z_2 = Pos_Two[n][2]
    
        x_3 = Pos_Test[n][0]
        y_3 = Pos_Test[n][1]
        z_3 = Pos_Test[n][2]
        
        vx1 = Velo_One[n][0]
        vy1 = Velo_One[n][1]
        vz1 = Velo_One[n][2]
        
        vx2 = Velo_Two[n][0]
        vy2 = Velo_Two[n][1]
        vz2 = Velo_Two[n][2]
        
        vx3 = Velo_Test[n][0]
        vy3 = Velo_Test[n][1]
        vz3 = Velo_Test[n][2]
        # K1 terms
        kvx_m1_1 = m1_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m1_1 = vx1
        kvy_m1_1 = m1_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m1_1 = vy1
        kvz_m1_1 = m1_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m1_1 = vz1
    
        kvx_m2_1 = m2_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m2_1 = vx2
        kvy_m2_1 = m2_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m2_1 = vy2
        kvz_m2_1 = m2_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m2_1 = vz2
    
        kvx_m3_1 = m3_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m3_1 = vx3
        kvy_m3_1 = m3_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m3_1 = vy3
        kvz_m3_1 = m3_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m3_1 = vz3
        # increment the incrementation parameters
        x_1 = x_1 + (h/2.0)*kx_m1_1
        y_1 = y_1 + (h/2.0)*ky_m1_1
        z_1 = z_1 + (h/2.0)*kz_m1_1
    
        x_2 = x_2 + (h/2.0)*kx_m2_1
        y_2 = y_2 + (h/2.0)*ky_m2_1
        z_2 = z_2 + (h/2.0)*kz_m2_1
    
        x_3 = x_3 + (h/2.0)*kx_m3_1
        y_3 = y_3 + (h/2.0)*ky_m3_1
        z_3 = z_3 + (h/2.0)*kz_m3_1
        # K2 terms
        kvx_m1_2 = m1_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m1_2 = vx1*kvx_m1_1*(h/2.0)
        kvy_m1_2 = m1_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m1_2 = vy1*kvy_m1_1*(h/2.0)
        kvz_m1_2 = m1_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m1_2 = vz1*kvz_m1_1*(h/2.0)
    
        kvx_m2_2 = m2_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m2_2 = vx2*kvx_m2_1*(h/2.0)
        kvy_m2_2 = m2_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m2_2 = vy2*kvy_m2_1*(h/2.0)
        kvz_m2_2 = m2_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m2_2 = vz2*kvz_m2_1*(h/2.0)
    
        kvx_m3_2 = m3_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m3_2 = vx3*kvx_m3_1*(h/2.0)
        kvy_m3_2 = m3_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m3_2 = vy3*kvy_m3_1*(h/2.0)
        kvz_m3_2 = m3_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m3_2 = vz3*kvz_m3_1*(h/2.0)
        # increment the incrementation parameters
        x_1 = x_1 + (h/2.0)*kx_m1_2
        y_1 = y_1 + (h/2.0)*ky_m1_2
        z_1 = z_1 + (h/2.0)*kz_m1_2
    
        x_2 = x_2 + (h/2.0)*kx_m2_2
        y_2 = y_2 + (h/2.0)*ky_m2_2
        z_2 = z_2 + (h/2.0)*kz_m2_2
    
        x_3 = x_3 + (h/2.0)*kx_m3_2
        y_3 = y_3 + (h/2.0)*ky_m3_2
        z_3 = z_3 + (h/2.0)*kz_m3_2
        #K3
        kvx_m1_3 = m1_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m1_3 = vx1*kvx_m1_2*(h/2.0)
        kvy_m1_3 = m1_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m1_3 = vy1*kvy_m1_2*(h/2.0)
        kvz_m1_3 = m1_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m1_3 = vz1*kvz_m1_2*(h/2.0)
    
        kvx_m2_3 = m2_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m2_3 = vx2*kvx_m2_2*(h/2.0)
        kvy_m2_3 = m2_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m2_3 = vy2*kvy_m2_2*(h/2.0)
        kvz_m2_3 = m2_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m2_3 = vz2*kvz_m2_2*(h/2.0)
    
        kvx_m3_3 = m3_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m3_3 = vx2*kvx_m3_2*(h/2.0)
        kvy_m3_3 = m3_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m3_3 = vy2*kvy_m3_2*(h/2.0)
        kvz_m3_3 = m3_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m3_3 = vz2*kvz_m3_2*(h/2.0)
        # increment the incrementation parameters
        x_1 = x_1 + (h)*kx_m1_3
        y_1 = y_1 + (h)*ky_m1_3
        z_1 = z_1 + (h)*kz_m1_3
    
        x_2 = x_2 + (h)*kx_m2_3
        y_2 = y_2 + (h)*ky_m2_3
        z_2 = z_2 + (h)*kz_m2_3
    
        x_3 = x_3 + (h)*kx_m3_3
        y_3 = y_3 + (h)*ky_m3_3
        z_3 = z_3 + (h)*kz_m3_3
        # K4
        kvx_m1_4 = m1_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m1_4 = vx1*kvx_m1_3*(h)
        kvy_m1_4 = m1_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m1_4 = vy1*kvy_m1_3*(h)
        kvz_m1_4 = m1_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m1_4 = vz1*kvz_m1_3*(h)
    
        kvx_m2_4 = m2_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m2_4 = vx2*kvx_m2_3*(h)
        kvy_m2_4 = m2_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m2_4 = vy2*kvy_m2_3*(h)
        kvz_m2_4 = m2_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m2_4 = vz2*kvz_m2_3*(h)
    
        kvx_m3_4 = m3_ax(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kx_m3_4 = vx2*kvx_m3_3*(h)
        kvy_m3_4 = m3_ay(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        ky_m3_4 = vy2*kvy_m3_3*(h)
        kvz_m3_4 = m3_az(x_1,y_1,z_1,x_2,y_2,z_2,x_3,y_3,z_3)
        kz_m3_4 = vz2*kvz_m3_3*(h)
        
        #Correct velocity for the Nth simulation
        Velo_One[n][0] =  Velo_One[n][0] + (h/6.0)*(kvx_m1_1 + 2.0*kvx_m1_2 + 2.0*kvx_m1_3 + kvx_m1_4)
        Velo_One[n][1] =  Velo_One[n][1] + (h/6.0)*(kvy_m1_1 + 2.0*kvy_m1_2 + 2.0*kvy_m1_3 + kvy_m1_4)
        Velo_One[n][2] =  Velo_One[n][2] + (h/6.0)*(kvz_m1_1 + 2.0*kvz_m1_2 + 2.0*kvz_m1_3 + kvz_m1_4)
    
        Velo_Two[n][0] =  Velo_Two[n][0] + (h/6.0)*(kvx_m2_1 + 2.0*kvx_m2_2 + 2.0*kvx_m2_3 + kvx_m2_4)
        Velo_Two[n][1] =  Velo_Two[n][1] + (h/6.0)*(kvy_m2_1 + 2.0*kvy_m2_2 + 2.0*kvy_m2_3 + kvy_m2_4)
        Velo_Two[n][2] =  Velo_Two[n][2] + (h/6.0)*(kvz_m2_1 + 2.0*kvz_m2_2 + 2.0*kvz_m2_3 + kvz_m2_4)
    
        Velo_Test[n][0] =  Velo_Test[n][0] + (h/6.0)*(kvx_m3_1 + 2.0*kvx_m3_2 + 2.0*kvx_m3_3 + kvx_m3_4)
        Velo_Test[n][1] =  Velo_Test[n][1] + (h/6.0)*(kvy_m3_1 + 2.0*kvy_m3_2 + 2.0*kvy_m3_3 + kvy_m3_4)
        Velo_Test[n][2] =  Velo_Test[n][2] + (h/6.0)*(kvz_m3_1 + 2.0*kvz_m3_2 + 2.0*kvz_m3_3 + kvz_m3_4)
        # Correct Position for the Nth simulation
        Pos_One[n][0] =  Pos_One[n][0] + (h/6.0)*(kx_m1_1 + 2.0*kx_m1_2 + 2.0*kx_m1_3 + kx_m1_4)
        Pos_One[n][1] =  Pos_One[n][1] + (h/6.0)*(ky_m1_1 + 2.0*ky_m1_2 + 2.0*ky_m1_3 + ky_m1_4)
        Pos_One[n][2] =  Pos_One[n][2] + (h/6.0)*(kz_m1_1 + 2.0*kz_m1_2 + 2.0*kz_m1_3 + kz_m1_4)
    
        Pos_Two[n][0] =  Pos_Two[n][0] + (h/6.0)*(kx_m2_1 + 2.0*kx_m2_2 + 2.0*kx_m2_3 + kx_m2_4)
        Pos_Two[n][1] =  Pos_Two[n][1] + (h/6.0)*(ky_m2_1 + 2.0*ky_m2_2 + 2.0*ky_m2_3 + ky_m2_4)
        Pos_Two[n][2] =  Pos_Two[n][2] + (h/6.0)*(kz_m2_1 + 2.0*kz_m2_2 + 2.0*kz_m2_3 + kz_m2_4)
    
        Pos_Test[n][0] =  Pos_Test[n][0] + (h/6.0)*(kx_m3_1 + 2.0*kx_m3_2 + 2.0*kx_m3_3 + kx_m3_4)
        Pos_Test[n][1] =  Pos_Test[n][1] + (h/6.0)*(ky_m3_1 + 2.0*ky_m3_2 + 2.0*ky_m3_3 + ky_m3_4)
        Pos_Test[n][2] =  Pos_Test[n][2] + (h/6.0)*(kz_m3_1 + 2.0*kz_m3_2 + 2.0*kz_m3_3 + kz_m3_4)
        
        # counter so only 50 points get plotted to reduce computational cost
        matplotlib.pyplot.scatter(Pos_One[0][0],Pos_One[0][1])
        matplotlib.pyplot.scatter(Pos_Two[0][0],Pos_Two[0][1])
        for q in range(N):
            matplotlib.pyplot.scatter(Pos_Test[q][0],Pos_Test[q][1])
        #if count == t0/NumOfPoints:
            
         #   count = 0
          #  matplotlib.pyplot.scatter(Pos_One[0][0],Pos_One[0][1])
           # matplotlib.pyplot.scatter(Pos_Two[0][0],Pos_Two[0][1])
            #for q in range(N):
             #   matplotlib.pyplot.scatter(Pos_Test[q][0],Pos_Test[q][1])
print "\nDone!\n"
matplotlib.pyplot.xlim((-10,10))
matplotlib.pyplot.ylim((-10,10))
matplotlib.pyplot.show()
