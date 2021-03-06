function [F, index] = FillNoteMatrix (S)
    
    Fs = 44100;
    Samples_num = 1024;
    M = zeros(7,12);
    Tab_F_1 = [65.41  69.3  73.42  77.78  82.41  87.31  92.5  98  103.83  110  116.54  123.47];
    k = 2.^[0:6];
    Tab_F = k' .* repmat(Tab_F_1, 7, 1);
    
    
    k_interp = Fs/length(S) - 1;
    zeros_num = floor( k_interp*Samples_num);
    Zer = zeros(zeros_num, 1);
    S2 = vertcat (Zer, S);
    
    Spec = abs(fft(S2));        % Получаем спектр с шагом примерно 1Гц
    N = length(Spec);
    N2 = N/2;
    Spec = Spec(1:N2);
    
    for i = 1:length(M)
        
        index = floor( N * Tab_F(i) / Fs ); % Перевод частоты в индекс
        M(i) = Spec(index);
       
    end
    F = 0;
    [F, index] = max(M);
    
end

