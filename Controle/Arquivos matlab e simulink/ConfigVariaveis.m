% Arquivo que contém os ganhos utilizados na simulação

global kroll
global kpitch
global kyaw
global kx
global ky
global kz

%Voo em cruzeiro
global ku
global kzprof
global kpitchprof

%step sin vento 60sec ITAERoll*50 + ITAEy
%Com valores iniciais x0 = [3.7900    0.1663    0.0200    0.0100    1.4255    3.0608    0.6441    0.0215]
xRollY = [5.5669    1.6582    0.0113    1.2229    1.7868    0.5453    0.0052    0.0001]

%step sin vento 60sec ITAEPitch*50 + ITAEx
%Com valores iniciais x0 = [ 3.7202    0.4176    0.0182    0.2166    1.9971    3.5878    0.9794    0.1711]

% VTOL
xPitchX = [3.4125    1.4194    0.0110    0.2067    1.8694    3.1439    1.6099    0.0001]
%QUASEVTOL mudou apenas o velocidade X pra ajudar na desaceleração
xPitchX1 = [3.4125    1.4194    0.0110    0.2067    1.8694    0.5    1.6099    0.0001]
%Beta depois de pi/2.5 (só pra pitch)
xPitchX2 = [6    3    0.01    1.5   1.9994    3.1439    1.6099    0.0001]
%Durante VC, zera controle de velocidade em VTOL
xPitchX3 = [7.1864    4.9121    0.1706    1.1068   1.9994   0    0    0]


%beta = 0
xZ = [1.1656    8   3.6063  0   0.6026]
%beta = alto
xZ2 = [0.35    20    2.5    0    0.5]


%xu em transicao
xu = [10    0.0044    0.0201] % <pi/2.5
xu2 = [10    0.0044      5] % >pi/2.5

xpitchz = [9.9883    0.0015    0.0210    7.9750    0.0001    0.0000    0.5    0.0001    0.0000   0.04    0.0051    0.03]


kroll.kp = xRollY(1);
kroll.kp_ponto = xRollY(2);
kroll.kd_ponto = xRollY(3);
kroll.ki_ponto = xRollY(4);

kpitch.betas = [0   pi/8];
kpitch.kp = [xPitchX(1) xPitchX2(1)];
kpitch.kp_ponto = [xPitchX(2) xPitchX2(2)];
kpitch.kd_ponto = [xPitchX(3) xPitchX2(3)];
kpitch.ki_ponto = [xPitchX(4) xPitchX2(4)];

kyaw.kp = 2;
kyaw.kp_ponto = 2;
kyaw.kd_ponto = 0.0134;
kyaw.ki_ponto = 2;

kx.betas = [pi/3  pi/2.5];
kx.kp = xPitchX(5);
kx.kp_ponto = [xPitchX1(6)   xPitchX3(6)];
kx.kd_ponto =  [xPitchX1(7)   xPitchX3(7)];
kx.ki_ponto =  [xPitchX1(8)   xPitchX3(8)];

ky.kp = xRollY(5);
ky.kp_ponto = xRollY(6);
ky.kd_ponto = xRollY(7);
ky.ki_ponto = xRollY(8);

kz.betas = [0   pi/2];
kz.kp = [xZ(1)  xZ2(1)];
kz.kp_ponto = [xZ(2)  xZ2(2)];
kz.kp_ponto_ponto = [xZ(3)  xZ2(3)];
kz.kd_ponto_ponto = [xZ(4)  xZ2(4)];
kz.ki_ponto_ponto = [xZ(5)  xZ2(5)];

ku.betas = [pi/2.5  pi/2]
ku.kp = [xu(1)  xu2(1)];
ku.kd = [xu(2)  xu2(2)];
ku.ki = [xu(3)  xu2(3)];



kpitchprof.kp = xpitchz(1);
kpitchprof.kd = xpitchz(2);
kpitchprof.ki = xpitchz(3);
kpitchprof.kp_ponto = xpitchz(4);
kpitchprof.kd_ponto = xpitchz(5);
kpitchprof.ki_ponto = xpitchz(6);

kzprof.kp = xpitchz(7);
kzprof.kd = xpitchz(8);
kzprof.ki = xpitchz(9);
kzprof.kp_ponto = xpitchz(10);
kzprof.kd_ponto = xpitchz(11);
kzprof.ki_ponto = xpitchz(12);

