% Variáveis globais para geração de um gif animado
global contgif
global erroOtimizador

% Define função que vou otimizar
fun = @otimizaControleProfundorZU;

% Tira warnings para deixar a simulação do simulink mais rápida
warning off;
contgif = 1;
erroOtimizador = [];

% Valores iniciais 
x0 = [7.9805    0.0011    0.0210    1.9925    0.0002    0.0360    0.3908    0.0000    0.0000   0.0231    0.0014    0.0263      7.9999    0.0044      0.0247]
%x0 = [9.9777     0.4986      5.2276e-05      7.9098      0.0299      4.0698e-05      2.0857e-06      1.2952e-04      3.0526e-08      0.0386      1.5930e-06      0.0376      10      0.0019      0.234]

% Define parâmetros para otimização
A = [];
b = [];
Aeq = [];
beq = [];

% Limiantes definidos pelas limitações da controladora
lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ub = [10, 0.5, 5, 8, 0.03, 8, 5, 0.02, 2, 8, 0.02, 2, 10, 0.02, 5]

nonlcon = [];

% Configura otimizador
options = optimoptions('fmincon','Display','iter', 'OutputFcn', @plotaIteracao);
a=10;

% Otimiza
x = fmincon(fun,x0,A,b,Aeq,beq,lb,ub,nonlcon, options)
