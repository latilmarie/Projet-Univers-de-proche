import cv2
import numpy as np
import matplotlib.pyplot as plt

#Paramètres plt
plt.rcParams["figure.figsize"] = (12,20)
plt.close('all')

#Définition fonctions
def recherche_voisinage(A,M,N,i,j):
    if A[i,j]==255:
        return([i,j])
    q=0
    while True and q<50:
        q+=1
        print(q)
        for l in range(i-q,i+q+1):
            m=j-q
            if l>=0 and l<M and m>=0 and m<N and A[l,m]==255:
                return([l,m])
            m=j+q
            if l>=0 and l<M and m>=0 and m<N and A[l,m]==255:
                return([l,m])
        for m in range(j-q+1,j+q):
            l=i-q
            if l>=0 and l<M and m>=0 and m<N and A[l,m]==255:
                return([l,m])
            l=i+q
            if l>=0 and l<M and m>=0 and m<N and A[l,m]==255:
                return([l,m])
    return([i,j])


def test_pixel_objet(A,M,N,i,j,liste_pixels):
    liste_pixels.append([i,j])
    A[i,j]=100
    voisins=[(i+1,j),(i-1,j),(i,j-1),(i,j+1)]
    for (k,l) in voisins:
        if k>=0 and k<M and l>=0 and l<N:
            if A[k,l]==255:
                test_pixel_objet(A,M,N,k,l,liste_pixels)

def barycentre(liste_pixels):
    N=len(liste_pixels)
    xG=0.0
    yG=0.0
    for pixel in liste_pixels:
        xG += pixel[1]
        yG += pixel[0]
    xG /= N
    yG /= N
    return ([xG,yG])

def onMouse(event,x,y,flags,param):
    global i0,j0
    global i1,j1
    if event==cv2.EVENT_LBUTTONDOWN:
        if i0== 0 and j0==0:
            j0=x
            i0=y
            print(i0,j0)
        else:
            j1=x
            i1=y
            print(i1,j1)

def cart2pol(x, y,pos_centre):
    X = x-pos_centre[1]
    Y = y-pos_centre[0]
    print(x,X)
    rho = np.sqrt((X)**2 + (Y)**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def cart2pol_list(list,pos_centre):
    X = list[:,0]
    Y = list[:,1]
    R,P = [],[]
    for j in range(len(list)):
        res=cart2pol(X[j],Y[j],pos_centre)
        R.append(res[0])
        P.append(res[1])
    R = np.array(R)
    P = np.array(P)
    return (R,P)

#Définition constante
ESC_KEY = 27     #Touche Echap
PAUSE_KEY = 32   #Touche espace
INTERVAL= 33     #intervalle
FRAME_RATE = 30  #fps

WINDOW_ORG = "org"
WINDOW_BACK = "back"
WINDOW_DIFF = "diff"
WINDOW_THRESH = "thresh"

pos_centre = (480,276)

FILE_ORG = "2_billes.mp4"

#constantes morpho
size_elem1 = 7
size_elem2 = 5
type_elem = cv2.MORPH_ELLIPSE
kernel = cv2.getStructuringElement(type_elem,(size_elem1,size_elem1))
kernel2 = cv2.getStructuringElement(type_elem,(size_elem2,size_elem2))

#constantes position
i0,j0 = 0,0
i1,j1 = 0,0
liste_G0 = []
liste_G1 = []

#Préparation de la fenêtre
cv2.namedWindow(WINDOW_THRESH)
cv2.namedWindow(WINDOW_ORG)
cv2.namedWindow(WINDOW_BACK)
cv2.namedWindow(WINDOW_DIFF)

#Lire le fichier vidéo original
mov_org = cv2.VideoCapture(FILE_ORG)

#Première image lue
has_next, i_frame = mov_org.read()
i_frame =  cv2.resize(i_frame, (i_frame.shape[1]//2,i_frame.shape[0]//2))

(M,N,c)=i_frame.shape


#Cadre de fond
back_frame = i_frame.astype(np.float32)

#Boucle de traitement de conversion
while has_next == True:
    cv2.setMouseCallback(WINDOW_THRESH,onMouse)

    #Convertir l'image d'entrée en type à virgule flottante
    f_frame = i_frame.astype(np.float32)

    #Calcul de la différence
    diff_frame = cv2.absdiff(f_frame, back_frame)
    ret, thresh = cv2.threshold(diff_frame, 50, 255, cv2.THRESH_BINARY)

    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    thresh = cv2.morphologyEx(thresh,cv2.MORPH_ERODE,kernel2)
    thresh[thresh<150]=0;
    thresh[thresh>150]=255;
    #ret, thresh = cv2.threshold(thresh, 200, 255, cv2.THRESH_BINARY)


    #Recherche position bille
    if i0 != 0 or j0 != 0:
        [i0,j0] = recherche_voisinage(thresh,M,N,i0,j0)
        liste_pixels0=[]
        test_pixel_objet(thresh,M,N,i0,j0,liste_pixels0)
        [xG0,yG0]=barycentre(liste_pixels0)
        j0=int(xG0)
        i0=int(yG0)
        liste_G0.append([xG0,M-yG0])
        L=20
        thresh[i0,j0-L:j0+L]=200
        thresh[i0-L:i0+L,j0]=200


    #Recherche position bille 2
    if i1 != 0 or j1 != 0:
        print("etape1")
        [i1,j1] = recherche_voisinage(thresh,M,N,i1,j1)
        print("\n2:")
        print(i1,j1)
        print("etape2")
        liste_pixels1=[]
        test_pixel_objet(thresh,M,N,i1,j1,liste_pixels1)
        print("etape3")
        [xG1,yG1]=barycentre(liste_pixels1)
        print("etape4")
        j1=int(xG1)
        i1=int(yG1)
        liste_G1.append([xG1,M-yG1])
        thresh[i1,j1-L:j1 +L]=200
        thresh[i1-L:i1+L,j1]=200

    #Affichage du cadre
    cv2.imshow(WINDOW_ORG, i_frame)
    cv2.imshow(WINDOW_DIFF, diff_frame.astype(np.uint8))
    cv2.imshow(WINDOW_BACK, back_frame.astype(np.uint8))
    cv2.imshow(WINDOW_THRESH, thresh)

    #Mise à jour en arrière-plan
    cv2.accumulateWeighted(f_frame, back_frame, 0.5)



    #Quitter avec la touche Echap
    key = cv2.waitKey(INTERVAL)
    if key == ESC_KEY:
        break
    if key == PAUSE_KEY:
        key2 = cv2.waitKey()
        if key2 == ESC_KEY:
            break
        else:
            while key2 != PAUSE_KEY:
                pass
    #Lire l'image suivante
    has_next, i_frame = mov_org.read()
    if has_next == True:
        i_frame =  cv2.resize(i_frame, (i_frame.shape[1]//2,i_frame.shape[0]//2))

#Affichage courbe position
if i0!=0 or j0!=0:
    plt.figure()
    plt.axes().set_aspect('equal')
    liste_G0=np.array(liste_G0)
    # plt.plot(liste_G0[:,0],liste_G0[:,1],"r.")   #en points
    plt.plot(liste_G0[:,0],liste_G0[:,1],'r')      #en lignes continues
    if i1!=0 or j1!=0:
        liste_G1=np.array(liste_G1)
        # plt.plot(liste_G1[:,0],liste_G1[:,1],"b.")
        plt.plot(liste_G1[:,0],liste_G1[:,1],"b")
    plt.xlim(0,N)
    plt.ylim(0,M)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    # plt.savefig("1_bille_positions.png")
    plt.show()

# #Affichage en polaire
# if i0!=0 or j0!=0:
#     plt.figure()
#     ax = plt.axes(projection = '3d')
#     liste_G0=np.array(liste_G0)
#     R0,P0 = cart2pol_list(liste_G0,pos_centre)
#     R0 = 1-R0/np.max(R0)
#     P0 = P0/np.max(P0)
#     # plt.plot(R0,P0,"r.")   #en points
#     ax.plot3D(P0,[k/len(R0) for k in range(len(R0))],R0,'r')      #en lignes continues
#     if i1!=0 or j1!=0:
#         liste_G1=np.array(liste_G1)
#         R1,P1 = cart2pol_list(liste_G1,pos_centre)
#         R1 = R1/np.max(R1)
#         P1 = P1/np.max(P1)
#         # ax.plot3D([k for k in range(len(R0))],R1,P1,"b.")
#         ax.plot3D([k for k in range(len(R0))],R1,P1,"b")
#     plt.xlim(0,1)
#     plt.ylim(0,1)
#     plt.xlabel("rayon")
#     plt.ylabel("phase")
#     plt.grid()
#     # plt.savefig("1_bille_positions.png")
#     plt.show()

#Terminer le traitement
cv2.destroyAllWindows()
mov_org.release()