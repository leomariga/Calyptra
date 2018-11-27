    function stop = plotaIteracao(x,optimvalues,state)
        % Cada iteração vem parar aqui
        global erroOtimizador
        global contgif
        erroOtimizador = [erroOtimizador, optimvalues.fval];
        global valDesejada
        global valMedida
        
        % Não para
        stop = false;
        if isequal(state,'iter')
            
            % Plota variável desejada e variável medida
            subplot(2,1,1);
            plot(valDesejada)
            hold on
            plot(valMedida)
            hold off
            title('Trajetória X')
            legend('X referência', 'X medido')
            xlabel('Tempo') 
            ylabel('m') 
            
            % Plota otimização
            subplot(2,1,2);
            plot(erroOtimizador)
            txt = ['Erro ITAE: ' num2str(optimvalues.fval)];
            title(txt)
            axis([-inf inf -inf inf])
            legend('Erro ITAE')
            xlabel('Iteração') 
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