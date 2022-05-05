#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  5 04:26:03 2022

@author: marie
"""

#%%
from math import *
import numpy as np
import skimage.io as skio
from skimage import color
from skimage import feature
from skimage import filters
import skimage as sk
import matplotlib.pyplot as plt
import skimage.morphology as skm
import matplotlib.pyplot as plt
import cv2
import os
plt.rcParams['image.cmap'] = 'gray'

#%% Filtre de Canny

plt.close('all')
os.chdir("...")

img = skio.imread("3kg.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = sk.img_as_float(img)

# Seuillage pour distinguer le lycra et le fond en noir
img[img>0.45]=1
img[img<0.45]=0
figure0 = plt.figure(0)

# Détection de coutours par filtre de Canny
img_canny = feature.canny(img, sigma=5, low_threshold = 0.3 , high_threshold = .4)
img_canny = sk.img_as_float32(img_canny)
plt.imshow(1-img_canny)


#%% Skeletonize pour récupérer la courbe pixel à pixel

plt.close('all')

img_skel = skm.skeletonize(img_canny)
plt.imshow(1-img_skel)


#%% Transformer l'image en fonction mathématique

plt.close('all')

x=[]
y=[]

for i in range (img_skel.shape[1]): # abscisse
    for j in range (img_skel.shape[0]): # ordonnée
        if img_skel[j,i] == True:
            x.append(img_skel.shape[1]-i)
            y.append(img_skel.shape[0]-j)

# Avoir une liste de valeurs croissantes (optionnel)
x = x[::-1]
y = y[::-1]
a=min(x)
b=min(y)

# Placer l'origine (0,0) au début du tableau
for i in range (len(x)):
    x[i] = x[i]-a
    y[i] = y[i]-b
    
plt.plot(x,y)


#%% Récupération d'un échantillon de coordonnées à traiter ensuite comme données

plt.close('all')

x1=[]
y1=[]

for i in range (0,len(x)-1000,10):
    x1.append(x[i])

for j in range (0,len(y)-1000,10):
    y1.append(y[j])
    
 
plt.plot(x1,y1,'b.')

