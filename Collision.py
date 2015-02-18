#Michael Quinn Parkinson - A Simple Collisional RK4 Code
# This code calculates the dynamics of two-dimensional particles
# Each particle is the same mass and mutually interacting gravitationally
# The Particles are allowed to collide but the approach for collison is
# extremely simple. This program was created to test a simple accretion model.
# Object accretion has not been added yet.
# The integration method is a fourth order Runge-Kutta method.
# A Picture is created of the interactions which then can be made
#into a movie via ffmpeg.


import math
import random
import numpy
import matplotlib
import pylab

g = 39.4 # Gravitational Constant in terms of Solar mass, AU, and Years

m1 = 1.0 # One Solar Mass Star
m2 = 1.0 # One Solar Mass Star
#Acceleration Functions

def acc(Pos,Acc):# mass one x dimension
    for i in range(len(Pos)):
        for j in range(i+1,len(Pos)):
            Acc[i][0] += -( (g*m1*m2*(Pos[i][0] - Pos[j][0]) )/( (Pos[i][0] - Pos[j][0])**(2.0) + (Pos[i][1] - Pos[j][1])**(2.0) )**(3.0/2.0))  #X acceleration
            Acc[i][1] += -( (g*m1*m2*(Pos[i][1] - Pos[j][1]) )/( (Pos[i][0] - Pos[j][0])**(2.0) + (Pos[i][1] - Pos[j][1])**(2.0) )**(3.0/2.0))  #Y acceleration
            if j == N - 1:
                Acc[j][0] += -( (g*m1*m2*(Pos[i][0] - Pos[j][0]) )/( (Pos[i][0] - Pos[j][0])**(2.0) + (Pos[i][1] - Pos[j][1])**(2.0) )**(3.0/2.0))  #X Acceleration 
                Acc[j][1] += -( (g*m1*m2*(Pos[i][0] - Pos[j][0]) )/( (Pos[i][0] - Pos[j][0])**(2.0) + (Pos[i][1] - Pos[j][1])**(2.0) )**(3.0/2.0))  #Y Acceleration
    return Acc
    
# Creates three arrays that will contain all position, velocity, and acceleration data
# The positions and velocities are randomly generated.
def Create(N):
    Pos = []
    Vel = []
    Acc = []
    for i in range(N):  #N Particles in the simulation
        Pos.append([random.random(),random.random()])
        Vel.append([random.random(),random.random()])
        Acc.append([0,0])   # Initial accelerations are set to zero
    return Pos, Vel, Acc

# Calculates the magnitude of the seperation vector between two particles.
# if the magnitude is less than the particle size then a collision will
# take place. A collision just sets the accelerations to zero and changes 
# the direction of the velocity.
def Coll(Pos,Vel):
    for i in range(len(Pos)):
        for j in range(i+1,len(Pos)):
            r1 = ( Pos[i][0]**(2.0) + Pos[i][1]**(2.0) )**(1.0/2.0)
            r2 = ( Pos[j][0]**(2.0) + Pos[j][1]**(2.0) )**(1.0/2.0)
            if math.fabs(r1 - r2) <= 0.0001:
                for d in range(2):
                    Vel[i][d] = -Vel[i][d]
                    Vel[j][d] = -Vel[j][d]
                    Acc[i][d] = 0
                    Acc[j][d] = 0
t0 = 100    # The total length of the integration.
h = 0.00001 #the step size for the integrator.
N = 100 #The number of particles in the simualtion.

Pos,Vel,Acc = Create(N) # Create initial conditions.

for t in range(t0):
    fig = matplotlib.pyplot.figure()
    Acc = acc(Pos,Acc)  # Each time step is calculated then saved to a .png file
    for n in range(N):
        for d in range(2):
            Vel[n][d] += h*Acc[n][d]
            Pos[n][d] += h*Vel[n][d]
            Coll(Pos,Vel)
            matplotlib.pyplot.scatter(Pos[n][0],Pos[n][1])
            name = 'pic_' + '{0:0{width}}'.format(t,width=3)    #increments the png files
    print "Saving ..." , name
    matplotlib.pyplot.xlim([-3,3])
    matplotlib.pyplot.ylim([-3,3])
    fig.savefig(name)
    matplotlib.pyplot.close(fig)

        
  
