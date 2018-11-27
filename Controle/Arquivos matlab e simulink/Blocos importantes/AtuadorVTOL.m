% Transforma um comando de thrust e momento em velocidade angular
function [w1,w2,w3,w4]= fcn(u1thrust, u2mRoll, u3mPitch, u4mYaw, ktd, kdd, lb)

% Define equação do atuador
w2ParaU = [ ktd      ktd     ktd      ktd;
           -ktd*lb(2)      ktd*lb(1)     ktd*lb(1)     -ktd*lb(2);
            ktd*lb(3)     -ktd*lb(4)     ktd*lb(3)     -ktd*lb(4);
           -kdd     -kdd       kdd      kdd];

% Calcula taxa de giro necessário com base no momento calculado pela
% controladora
w = inv(w2ParaU)*[u1thrust ; u2mRoll ; u3mPitch ; u4mYaw];

% Satura taxa de giro 
for i = 1:numel(w);
   if(w(i) > 263169)
      w(i) = 263169; 
   end
end
for i = 1:numel(w);
   if(w(i) < 0)
      w(i) = 0; 
   end
end

% Coloca na saída
w1 = sqrt(w(1));
w2 = sqrt(w(2));
w3 = sqrt(w(3));
w4 = sqrt(w(4));
