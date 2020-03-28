%% P1
f = pi/2;
q = 0.99;
fb = q + (q / (1-f));
N = 1000;

b = [f^2];
a = [1, -(2 - 2*f + f*fb - f^2*fb), 1 - 2*f + f*fb + f^2 - f^2*fb];
w = linspace(0,pi,N);

figure(7);
freqz(a,b,w)
figure(8);
zplane(a,b)

%% Génération du signal d'entrée

fs = 8000; % Taux d'échantillonnage (échantillons/sec)
f0 = 5;    % Fréquence du signal (Hz)
T = 2.0;   % Duration du signal (sec)

dt = 1/fs; period = 1/f0; t = 0:dt:T; N = length(t);
xs = floor(256 * mod(t,period)/period - 128);
ys = zeros(size(xs));

% Ici vous pouvez définir des variables
y_old = zeros(1,2);

% Ceci est la boucle de calcul où chaque échantillon est traité
% individuellement

for n = 1:1:N
  
  % Charger l'échantillon
  x = xs(n);
  
  % Do your thing
  y =  b(1)*x - a(2)*y_old(1) - a(3)*y_old(2);
  

  
  %Offset saved y values
  for i = length(y_old) : -1 : 2
      y_old(i) = y_old(i-1);
  end
  y_old(1) = y
 
  % Sauvegarder l'échantillon traité
  ys(n) = y;
  
end

% Afficher les signaux d'entrée et de sorties
figure(1);
plot(t,xs,'b',t,ys,'r');




%   % Copie de la mémoire
%   d(1:1:(D-1)) = d(2:1:D)
%   % Enregistrement dans le vecteur d
%   d(D) = x;
%   
%   % Définir un accumulateur s
%   s = 0;
%   % Faire la somme de chaque élément
%   for i = 1:1:D
%     s = s + d(i);
%   end
%   % Diviser par le nombre d'éléments
%   y = s / D;