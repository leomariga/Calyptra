    function stop = plotaIteracao(x,optimvalues,state)
        % Cada itera��o vem parar aqui
        global erroOtimizador
        global contgif
        erroOtimizador = [erroOtimizador, optimvalues.fval];
        global valDesejada
        global valMedida
        
        % N�o para
        stop = false;
        if isequal(state,'iter')
            
            % Plota vari�vel desejada e vari�vel medida
            subplot(2,1,1);
            plot(valDesejada)
            hold on
            plot(valMedida)
            hold off
            title('Trajet�ria X')
            legend('X refer�ncia', 'X medido')
            xlabel('Tempo') 
            ylabel('m') 
            
            % Plota otimiza��o
            subplot(2,1,2);
            plot(erroOtimizador)
            txt = ['Erro ITAE: ' num2str(optimvalues.fval)];
            title(txt)
            axis([-inf inf -inf inf])
            legend('Erro ITAE')
            xlabel('Itera��o') 
            ylabel('Erro') 
            
            % Adiciona no gif
            if(contgif == 1)
                gif('otimizaZprofundor.gif', 'frame', gcf)
            else
                gif
            end
            contgif = contgif+1;
            
        end
    end