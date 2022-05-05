#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 04:52:11 2022

@author: marie
"""

from math import *
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

# Paramètres optimaux trouvés par optimisation
a = -0.2958
b = 0.9932
c = 6.9997
d = 0.2978

# Conditions initiales
r_px_m = 1.4/460            # rapport pixel à mètre, pour convertir les pixels en mètre
distance0 = 188.22          # rayon de la position de départ, en pixels
alpha0 = 0.657 - pi         # coordonnée polaire de la position initiale
vx0 = -90.91                # vitesse initiale selon axe x, en pixels
vy0 = 363.64                # vitesse initiale selon axe y, en pixels
f = 0.3                     # coefficient de frottement
disk = 0.08                 # rayon de la masse centrale

dt = 0.033                  # pas de temps (frame utilisée sur le traitement vidéo)
g = 9.81
   
# initialisation des conditions initiales
vx = vx0*r_px_m             # vitesse en mètres
vy = vy0*r_px_m
Vx = [vx]
Vy = [vy]
distance = distance0*r_px_m # passage en mètre
alpha = alpha0
X = [distance*cos(alpha)]
Y = [distance*sin(alpha)]
i = 1
   
# itération des variables
while i<10000 and distance>disk:
    truc = 2*pi-((b+distance*c)**2)/(a*c)
    a_norme = g*sin(atan(truc))
    X.append(X[i-1]+vx*dt+(a_norme*cos(alpha-pi)-vx*f)*dt*dt/2)
    Y.append(Y[i-1]+vy*dt+(a_norme*sin(alpha-pi)-vy*f)*dt*dt/2)
    
    # mise à jour des variables
    vx = (X[i]-X[i-1])/dt
    vy = (Y[i]-Y[i-1])/dt
    
    Vx = np.array([[Vx, vx]])
    Vy = np.array([[Vy, vy]])
     
    distance = sqrt(X[i]**2 + Y[i]**2)
       
    # calcul de l'angle (coordonnées polaires)
    if X[i]>0:
        alpha = atan(Y[i]/X[i])
    else:
        if X[i]==0:
            if Y[i]>0:
                alpha = pi/2
            else:
                alpha = -pi/2
        else:
            if Y[i]>= 0:
                alpha = pi+atan(Y[i]/X[i])
            else:
                alpha = atan(Y[i]/X[i]) - pi
    i+=1

   
# Affichage des figures
plt.plot(X, Y)
plt.xlabel("x")
plt.ylabel("y")






