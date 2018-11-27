fun = @otimizaControleProfundorZ;

global contgif
global erroOtimizador
warning off;
contgif = 1;
erroOtimizador = []
%x0 = [3, 0.1, 0.01, 0.05, 0.4, 0.1, 1, 0.5];
%x0 = [3.7900    0.1663    0.0200    0.0100    1.4255    3.0608    0.6441    0.0215]


x0 = [1.6775    0.0091    2.2164    0.5826    0.0082    4.4885    0.0001    0    0.001]
A = [];
b = [];
Aeq = [];
beq = [];
lb = [0, 0, 0, 0, 0, 0, 0, 0, 0]
ub = [15, 0.02, 5, 2, 0.02, 8, 5, 0.02, 2]
nonlcon = [];
options = optimoptions('fmincon','Display','iter', 'OutputFcn', @plotaIteracao);
a=10;
x = fmincon(fun,x0,A,b,Aeq,beq,lb,ub,nonlcon, options)
