clc;

R_e = 6.4;
R_s = 70;
L_e = 0.051E-6;
B_l = 10.8;
M_m = 13.3E-3;
K_m = 935;
R_m = 0.5;
S_m = 201E-4;
d = 1;
c = 340;
rho = 1;
i_max = 50E-3;


% L_e * di + (R_e + R_s)* i = u - B_l *dx
% M_m * dx2 + R_m * dx + K_m * x = B_l * i
% p = (rho * S_m)/(2*pi*d) *dx2 * delta(t - d / c)
% 
% M_m * s^2 * x + R_m * s*x + K_m * x = B_l * i

%% equation 2
numerator2 = [B_l];
denominator2 = [M_m, R_m, K_m];
% xHi = tf(numerator, denominator)
% dt= 1E-4
% t = [0:dt:0.03];
% xhi = impulse(xHi,t);
% figure(1)
% clf;
% subplot(2,1,1);
% hold on;
% plot(t,xhi)


%% equation 1
% L_e * di + (R_e + R_s)* i = u - B_l *dx

% L_e * s* I + (R_e + R_s)* I = u - B_l *s *X
% X = (xHi) * I
% L_e * s* I + (R_e + R_s)* I = u - B_l *s *(xHi) * I

% L_e * s* I + (R_e + R_s)* I + B_l *s *(xHi) * I = u 
%I/U = 1/ ( L_e * s + (R_e + R_s) + B_l *s *(xHi))

numerator = [denominator2];
denominator = [L_e*denominator2 + B_l*numerator2, R_e + R_s];
iHu = tf(numerator, denominator)
dt= 1E-4
t = [0:dt:0.03];
ihu = impulse(iHu,t);
figure(1)
clf;
% subplot(2,1,1);
% hold on;
plot(ihu)
% u = zeros(1,length(t));
% u(1,1:0.01/dt) = 3.3;
% plot(t,u);
% 
% subplot(2,1,2);
% con = conv(u, xhi, 'same')
% plot(t,con)
