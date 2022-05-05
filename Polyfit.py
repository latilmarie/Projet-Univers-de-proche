# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 08:58:43 2022

@author: Joseph
"""

import numpy as np
import matplotlib.pyplot as plt

# %%


def iprint(image, titre=" "):
    plt.figure()
    plt.imshow(image), plt.title(titre, fontsize=18),  # plt.colorbar()


# %%
x_list = [0, 0.059, 0.133, 0.218, 0.312, 0.411, 0.510, 0.610, 0.710, 0.810,
          0.910, 1.010, 1.110, 1.210, 1.310, 1.410, 1.510, 1.610, 1.710, 1.806]
y_list = [0, 0.100, 0.199, 0.299, 0.396, 0.490, 0.577, 0.661, 0.740, 0.817,
          0.892, 0.965, 1.036, 1.106, 1.174, 1.241, 1.306, 1.370, 1.434, 1.495]

x = np.array(x_list)
y = np.array(y_list)

courbe = np.polyfit(x, y, 3)
courbe2 = np.polyfit(x, y, 2)
courbe3 = np.polyfit(x, y, 5)

y1 = np.zeros(20)
for i in range(0, 20):
    y1[i] = ((x[i]*x[i]*x[i])*courbe[0]) + ((x[i]*x[i]) * courbe[1]) + (x[i]*courbe[2]) + courbe[3]

y2 = np.zeros(20)
for i in range(0, 20):
    y2[i] = ((x[i]*x[i])*courbe2[0]) + ((x[i])*courbe2[1]) + (courbe2[2])

y3 = np.zeros(20)
for i in range(0, 20):
    y3[i] = ((x[i]*x[i]*x[i]*x[i]*x[i])*courbe3[0]) + ((x[i]*x[i]*x[i]*x[i])*courbe3[1]) + (x[i]*x[i]*x[i]*courbe3[2]) + (x[i]*x[i])*courbe3[3] + x[i]*courbe3[4] + courbe3[5]

fig = plt.figure(figsize=(14, 8))

# le paramètre alpha atténue l'intensité de la couleur représentée par la courbe
plt.plot(x, y3, alpha=1, label='Ordre 5', color='green', linestyle='dotted', linewidth=2)

# plt.plot(x, y1, alpha=2, label='Ordre 3',
#          color='red', linestyle='dashed', linewidth=2)
# plt.plot(x, y2, linestyle='dashdot', label='Ordre 2', color='green')

plt.plot(x, y, label='Courbe initiale')
plt.legend()
plt.title('Approximation de la Courbure')
plt.xlabel('x')
plt.ylabel('y')
# alpha = 0.7
plt.grid(alpha=.6, linestyle=':')
plt.show()

