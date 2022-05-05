# Projet-Univers-de-proche


**Programme Python trajectoire_theorique.py
Code qui permet de tracer la trajectoire théorique d’une bille avec une masse centrale de 3kg et les
conditions initiales utilisées expérimentalement.

**Programme Python extraction_donnees_courbe.py

Code qui permet de :
- récupérer les contours de la déformation du lycra avec un filtre de Canny,
- skeltonize le contour pixel à pixel,
- transforme la courbe visible sur l’image en fonction mathématique (coordonnées des pixels de la
courbe stockés dans des tableaux),
- sélection d’un échantillon de coordonnées

**Programme Matlab optimisation.m

Code qui permet de déterminer les coefficients a, b, c et d minimisant l’EQM par descente du gradient
afin de trouver l’équation de la courbe.

**Programme Python Polyfit.py

Utilise la méthode polyfit pour approximer l’équation de la courbe.

**Programme Python trajectoire_theorique.py

Code qui permet de déterminer la trajectoire expérimentale d’une bille autour d’une masse de 3kg.

**Programme Python tracker_OpenCV.py

Code de détection de la trajectoire de la bille par les traqueurs automatiques d’OpenCV.

**Programme Python find_hsv_values.py

Code qui permet de déterminer les plages HSV inférieures et supérieures de la bille.

**Programme Python hsv_tracking.py

Code qui permet de détecter la trajectoire d’une ou plusieurs billes par HSV.

**Programme Python code_HSV_barycentre.py

Code de la méthode de détection de la trajectoire par passage par l’histogramme HSV et détection de
position par barycentre (avec adaptation pour retirer le fond).
