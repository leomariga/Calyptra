function [c,ceq] = otimizaControleProfundorZU(x)
% Os ganhos de controle são definidos aqui para poderem ser acessados pela
% simulação no simulink
global kpitchprof
global kzprof
global ku
global contgif
global erroOtimizador

% Variáveis para plotar os gifs
global valDesejada
global valMedida

% Modifica os ganhos na simulação para testar os valores do simulador.
kpitchprof.kp = x(1);
kpitchprof.kd = x(2);
kpitchprof.ki = x(3);
kpitchprof.kp_ponto = x(4);
kpitchprof.kd_ponto = x(5);
kpitchprof.ki_ponto = x(6);

kzprof.kp = x(7);
kzprof.kd = x(8);
kzprof.ki = x(9);
kzprof.kp_ponto = x(10);
kzprof.kd_ponto = x(11);
kzprof.ki_ponto = x(12);

ku.kp = x(13);
ku.kd = x(14);
ku.ki = x(15);

% Período da simulação
st = 0.01;

% Roda simulação e armazena variáveis com as respostas desejadas
simulacao = sim('controladora_reorganizada_transicao');

% Critérios de otimização
ISEZ = sum((zDesejado.Data - zMedido.Data).^2);
ITAEZ = sum(st*abs(zDesejado.Data - zMedido.Data));
ITAEPitch = sum(st*abs(thetaDesejado.Data - thetaMedido.Data));
ITAEU = sum(st*abs(uDesejado.Data - uMedido.Data));
ITAEZPONTO = sum(st*abs(zPontoDesejado.Data - zPontoMedido.Data));

valDesejada = zDesejado;
valMedida = zMedido;

% Função custo com a combinação de várias variáveis, buscando otimização
% simultânia desses parâmetros.
c = 1.5*ITAEZ + 10*ITAEPitch + 3*ITAEU + 1.5*ITAEZPONTO;
ceq = [];