% Transforma um comando de thrust e momento em velocidade angular

function [w1,w2,w3,w4, alphaProfundor]= fcn(u1thrust, u3mPitch, ktd, kdd, lb)

% Matriz de convers�o entre empuxo para rota��o dos motores
w2ParaU = [ ktd      ktd     ktd      ktd;
           -ktd*lb(2)      ktd*lb(1)     ktd*lb(1)     -ktd*lb(2);
            ktd*lb(3)     -ktd*lb(4)     ktd*lb(3)     -ktd*lb(4);
           -kdd     -kdd       kdd      kdd];

% Quando ta em voo de cruzeiro, os momentos s�o compensados pelo profundor,
% e n�o pelos motores. Portanto, a rota��o dos motores s� depende do thrust
% desejado.
w = inv(w2ParaU)*[u1thrust ; 0 ; 0 ; 0];

% A corre��o de pitch do profundor � aplicado. Neste cado, o momento est�
% sendo passado diretamente para o pr�ximo bloco, mas poderia se fazer a
% convers�o desse momento em um �ngulo de ataque do profundor caso
% necessite de informa��es sobre esse �ngulo.
alphaProfundor = u3mPitch;

% Satura rota��o dos motores
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

%Joga resposta na sa�da
w1 = sqrt(w(1));
w2 = 0;
w3 = sqrt(w(3));
w4 = 0;
