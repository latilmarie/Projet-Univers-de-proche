% Script pour optimiser le critere par la methode de descente du gradient à pas fixe

clear all
close all
clc

% Rapport pixel à mètre
  r_px_m = 3.19*1e-4;

% valeurs relevees de la courbe du lycra
  x = [0; 3; 7; 11; 16; 21; 27; 32; 38; 44; 51; 57; 64; 71; 78; 86; 93; 101; 109; 117; 125; 134; 142; 151; 160; 170; 179; 189; 198; 208; 218; 228; 238; 248; 258; 268; 278; 288; 298; 308; 318; 328; 338; 348; 358]*r_px_m;
  y = [0; 10; 20; 30; 40; 50; 60; 70; 80; 90; 100; 110; 120; 130; 140; 150; 160; 170; 180; 190; 200; 210; 220; 230; 240; 250; 260; 270; 280; 290; 300; 310; 319; 329; 339; 348; 357; 366; 375; 384; 393; 401; 410; 418; 427]*r_px_m;
  N = length(y);

% Parametres
  rho	  =	1e-3;
  beta1_0 = -0.3;
  beta2_0 =	0.99;
  beta3_0 = 7;
  beta4_0 = 0.303;
  nbItMax =	500000;
  numFig  = 1;

% 1. Descente de gradient
	% a. Initialisation
    ind = 2 ;
    seuil = 1e-9 ;
    delta = seuil + 1 ;
	beta = [beta1_0 ; beta2_0 ; beta3_0 ; beta4_0];		% valeur initiale des parametres
	J_ind0 = sum((y-beta(1,ind-1)./(beta(2,ind-1)+beta(3,ind-1).*x)-beta(4,ind-1)).^2);		% Valeur du critere pour les parametres initiaux
        
    % b. Iterations
 	while (ind < nbItMax) & delta > seuil
        % Calcul du gradient 
          A = (y-beta(1,ind-1)./(beta(3,ind-1).*x+beta(2,ind-1))-beta(4,ind-1));
          gradJ = (1/N)*[ sum(-2./(beta(3,ind-1).*x+beta(2,ind-1)).*A); sum(2.*A.*beta(1,ind-1)./(beta(2,ind-1)+beta(3,ind-1).*x).^2) ; sum(2.*A.*beta(1,ind-1).*x./(beta(2,ind-1)+beta(3,ind-1).*x).^2) ; sum(-2.*A) ];
%                
%      --> mise a jour des parametres par la méthode à pas fixe
          beta(:,ind) = beta(:,ind-1)-rho*gradJ;
          J_ind = sum((y-beta(1,ind)./(beta(2,ind)+beta(3,ind).*x)-beta(4,ind)).^2);
          J_ind0 = sum((y-beta(1,ind-1)./(beta(2,ind-1)+beta(3,ind-1).*x)-beta(4,ind-1)).^2);
 
          delta = abs(J_ind-J_ind0) ;
          ind=ind+1;
    end
    
    if ind==nbItMax
      fprintf("Nombre d'itération maximal atteint !\n")
    else
      fprintf("Critère d'arrêt après %i itérations\n",ind)
    end
       
%   Affichage y en fonction de l'x avec les paramètres beta calculés
    x2=[0:10*r_px_m:350*r_px_m];
    figure(3)
    grid on 
    plot(x2,beta(1,end)./(beta(2,end)+beta(3,end).*x2)+beta(4,end),'b*','LineWidth',1)
    hold on
    plot(x,y,'r*','LineWidth',2)
    legend({'Modèle','Données'},'Location','southeast')
    title("Modélisation de y en fonction de x")
    xlabel("x (m)")
    ylabel("y (m)")
    hold off
    
%   Affichage de paramètres optimaux et de l'EQM
    beta(1,end)
    beta(2,end)
    beta(3,end)
    beta(4,end)
    J_ind