% Bloco Din�mica do sistema

function [estados, U, a_angular, a, XYZ, XYZ_ponto,XYZ_ponto_ponto, phi_theta_psi, phi_theta_psi_ponto, thrustX, arrastoParasita, arrastoInduzido, sustentacao, arrastoTotal, forcas, gravidadeVec]  = fcn(w1,w2, w3, w4, gravidade, massaTotal,rho,areaAviao, areaAsa, cdParasita, cdAviao, clAviao, ktd, kdd, lb, Ixyz, velVento, beta, alphaProfundor, dt, estados_anterior)

% Separa entrada nos vetores
XYZ = estados_anterior(:, 1);
XYZ_ponto = estados_anterior(:, 2);
phi_theta_psi = estados_anterior(:, 3);
phi_theta_psi_ponto = estados_anterior(:, 4);

% Relaciona atitudes da aeronave
roll = phi_theta_psi(1);
pitch = phi_theta_psi(2);
yaw = phi_theta_psi(3);

phi = roll;
theta = pitch;
psi = yaw;


% Define Matriz de rota��o ZYX 
matrizRotacao =     [cos(theta)*cos(psi) cos(psi)*sin(theta)*sin(phi)-sin(psi)*cos(phi) cos(psi)*sin(theta)*cos(phi)+sin(psi)*sin(phi);
                     sin(psi)*cos(theta) sin(psi)*sin(theta)*sin(phi)+cos(psi)*cos(phi) sin(psi)*sin(theta)*cos(phi)-cos(psi)*sin(phi);
                     -sin(theta) cos(theta)*sin(phi) cos(theta)*cos(phi)];

% Matriz de transforma��o das velocidades angulares
T = [1 0 -sin(theta);
    0 cos(phi) cos(theta)*sin(phi);
    0 -sin(phi) cos(theta)*cos(phi)];

% Encontra velocidades lineares e angulares no eixo do corpo com base no
% eixo inercial
vel_angular_body = T*phi_theta_psi_ponto;
vel_linear_body = matrizRotacao'*XYZ_ponto;

%Velocidade do vento no referencial do corpo
vel_vento_body = matrizRotacao'*velVento;

% Velocidade do corpo em rela��o ao vento
vel_aerodinamica_body = vel_linear_body-vel_vento_body;

% For�as e momentos gerados por cada rota��o dos motores
w2ParaU = [ ktd      ktd     ktd      ktd;
           -ktd*lb(2)      ktd*lb(1)     ktd*lb(1)     -ktd*lb(2);
            ktd*lb(3)     -ktd*lb(4)     ktd*lb(3)     -ktd*lb(4);
           -kdd     -kdd       kdd      kdd];


% Calcula a for�a no eixo Z causada pelos motores
U = w2ParaU * [w1^2*cos(beta); w2^2; w3^2*cos(beta); w4^2]; % Componente vertical, motor 1 e 3 est�o em tilt com �ngulo Beta

% Calcula a for�a no eixo X causada pelos motores
thrustX = [([ ktd      ktd     ktd      ktd]*[w1^2*sin(beta); 0; w3^2*sin(beta); 0]) ; 0 ; 0];% Componente da for�a horizontal, com motor tiltado

% For�as presentes no referencial do corpo
thrust = U(1)*[0; 0; 1];
forcas = -thrust;

% Calcula arrasto parasita
arrastoParasita = -sign(vel_aerodinamica_body).*((rho*(vel_aerodinamica_body.^2)'*cdParasita*areaAviao/2)'); % Calcula arrasto parasita


% Calcula arrasto induzido e sustenta��o se tiver velocidade em X
if(vel_aerodinamica_body(1) > 0)
    arrastoInduzido = [-rho*vel_aerodinamica_body(1)^2*cdAviao*areaAsa/2 ; 0 ; 0]; % Encontra arrasto induzido da asa + profundor (o cd ta ajustado pra usar apenas a �rea da asa)
    clAlpha = 0.0744*(theta*180/pi +6) + 0.148;
    sustentacao = [0 ; 0 ; -rho*vel_aerodinamica_body(1)^2*clAlpha*areaAsa/2];
else
     arrastoInduzido = [0;0;0];
     sustentacao = [0;0;0];
end

% Arrasto total
arrastoTotal = arrastoParasita+arrastoInduzido;

% Gravidade
gravidadeVec = (matrizRotacao')*(massaTotal*gravidade*[0; 0; 1]);

% Somat�rio total de for�as
FtotalBody = -thrust + gravidadeVec + arrastoParasita+arrastoInduzido+sustentacao + thrustX; 

% Momentos presentes no referencial do corpo
% alphaProfundor � o pr�prio momento do profundor e n�o o �ngulo alpha
% dele, feito  para simplificar a an�lise
mXroll = U(2);
mYpitch = U(3)+alphaProfundor;
mZyaw = U(4);
momentos = [mXroll; mYpitch; mZyaw];

% Adiciona efeito girosc�pio e efeitos do produto vetorial do modelo de
% Newton-Euler
FtotalBody = FtotalBody - cross(vel_angular_body,(massaTotal*vel_linear_body));
momentos = momentos - cross(vel_angular_body,(Ixyz*vel_angular_body));

% Calcula acelera��o em rela��o ao body frame
a = FtotalBody/massaTotal;

%Calcula acelera��o angular em rela��o ao body frame
a_angular = inv(Ixyz)*(momentos);

% Calcula velocidade angular em rela��o ao body axis
vel_angular_body = vel_angular_body + a_angular*dt;

% Encontra velocidade angular em rela��o ao eixo inercial
phi_theta_psi_ponto = inv(T)*vel_angular_body;

% Encontra os �ngulos com base na velocidade angular no eixo inercial
phi_theta_psi = phi_theta_psi+ phi_theta_psi_ponto*dt;

% Encontra velocidade linear em rela��o ao body axis
vel_linear_body = vel_linear_body + a*dt;

XYZ_ponto_ponto = matrizRotacao*a;

% Encontra velocidade linear em rela��o ao eixo inercial
XYZ_ponto = matrizRotacao*vel_linear_body;

% Encontra posi��o em rela��o ao eixo inercial
XYZ = XYZ+XYZ_ponto*dt;

estados = horzcat(XYZ, XYZ_ponto, phi_theta_psi, phi_theta_psi_ponto);
