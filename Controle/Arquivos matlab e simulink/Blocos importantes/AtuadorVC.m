% Transforma um comando de thrust e momento em velocidade angular

function [w1,w2,w3,w4, alphaProfundor]= fcn(u1thrust, u3mPitch, ktd, kdd, lb)

% Matriz de conversão entre empuxo para rotação dos motores
w2ParaU = [ ktd      ktd     ktd      ktd;
           -ktd*lb(2)      ktd*lb(1)     ktd*lb(1)     -ktd*lb(2);
            ktd*lb(3)     -ktd*lb(4)     ktd*lb(3)     -ktd*lb(4);
           -kdd     -kdd       kdd      kdd];

% Quando ta em voo de cruzeiro, os momentos são compensados pelo profundor,
% e não pelos motores. Portanto, a rotação dos motores só depende do thrust
% desejado.
w = inv(w2ParaU)*[u1thrust ; 0 ; 0 ; 0];

% A correção de pitch do profundor é aplicado. Neste cado, o momento está
% sendo passado diretamente para o próximo bloco, mas poderia se fazer a
% conversão desse momento em um ângulo de ataque do profundor caso
% necessite de informações sobre esse ângulo.
alphaProfundor = u3mPitch;

% Satura rotação dos motores
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

%Joga resposta na saída
w1 = sqrt(w(1));
w2 = 0;
w3 = sqrt(w(3));
w4 = 0;
