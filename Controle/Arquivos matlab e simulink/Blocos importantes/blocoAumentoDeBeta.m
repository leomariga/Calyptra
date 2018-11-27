function [beta, velCorpo] = fcn(velocidadeInercial, phi_theta_psi, betaFixo, velAngularBeta, tempoAtivacao, sampleTime, tempoSim, betaAnterior, velCruzeiro, modoAsaAnterior, tempoDesativacao)
%% Utilizado para calcular a velocidade no referencial do corpo:
% Isso foi usado apenas para simular a estratégia de transição direta, onde
% a atuação do profundor ocorria abruptamente ao atingir velocidade de
% estol.
velCorpo = [0;0;0];
beta = betaAnterior;
roll = phi_theta_psi(1);
pitch = phi_theta_psi(2);
yaw = phi_theta_psi(3);

phi = roll;
theta = pitch;
psi = yaw;

matrizRotacao =     [cos(theta)*cos(psi) cos(psi)*sin(theta)*sin(phi)-sin(psi)*cos(phi) cos(psi)*sin(theta)*cos(phi)+sin(psi)*sin(phi);
                     sin(psi)*cos(theta) sin(psi)*sin(theta)*sin(phi)+cos(psi)*cos(phi) sin(psi)*sin(theta)*cos(phi)-cos(psi)*sin(phi);
                     -sin(theta) cos(theta)*sin(phi) cos(theta)*cos(phi)];
                 
velCorpo = matrizRotacao'*velocidadeInercial;

%% Aumento de beta propriamente dito

%Aguarda o tempo de simulação chegar no tempo de ativação
if(tempoSim >= tempoAtivacao)
   if(betaAnterior < pi/2) % se beta menor que 90 graus
       beta = betaAnterior + velAngularBeta*sampleTime; %vai aumentando beta a uma taxa específica
   end
   if(betaAnterior >= betaFixo) % até atingir um beta estipulado, para uma transição completa, esse valor é 90 graus
       beta = betaFixo;
   end
else
   beta = 0; 
end

if(tempoSim >= tempoDesativacao) % de VC para VTOL é só diminuir
    if(beta >=0)
       beta = betaAnterior - velAngularBeta*sampleTime;
    else
       beta =0;
    end
end