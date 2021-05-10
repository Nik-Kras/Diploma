path = "D:\Desktop\Studie\Diploma\GIT Matlab\Audio data\wav\Steinway Grand Piano 70.wav";
[y, Fs] = audioread(path1);
z = y(:,1);

% figure
% spectrogram(z,16000, 1000, 16000,Fs,'yaxis')
% title('Sound spectrogram (60 notes)')
% ylim([0 2])

t = [0:length(z)-1]/Fs

% figure
% plot(t, z)

t1 = 140;   % время в секундах
t2 = 142;

n1 = t1*Fs;
n2 = t2*Fs;

z1 = z(n1:n2);

% Сложу спектры всех временных срезов в SpecFigures
Samples_num = 1024;
cuts = floor( length(z1) / Samples_num ) - 1;   % Кол-во вырезок по времени
SpecFigures = zeros(1024, cuts);                % Массив векторов

for i = 1:cuts
    
    n1 = i*Samples_num;         % Задаю пределы для вырезания участка сигнала
    n2 = (i+1)*Samples_num - 1;
    
    S = z1(n1: n2);             % Берем участок сигнала
    Spec = abs(fft(S));        % Находим спектр сигнала
    SpecFigures(:,i) = Spec(:);          % Заполняем матрицу нот
    
    if mod(i,200) == 0
        figure(i)
        plot(Spec);
        title("Spectrum number #" + string(i))
    end
    
end

% Строю гистограммы
s1 = SpecFigures(6,:)
s2 = SpecFigures(1,:)
s3 = SpecFigures(11,:)
s4 = SpecFigures(15,:)

dH = 0.5;
maxH = 20;
edges = [0:dH:maxH];

figure
histogram(s1, edges)
title('PDF for harmonic 1')

figure
histogram(s2, edges)
title('PDF for non-harmonic 1')

figure
histogram(s3, edges)
title('PDF for harmonic 2')

figure
histogram(s4, edges)
title('PDF for non-harmonic 2')
