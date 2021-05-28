clear all
close all

% 1. Завантаження сигналу з послідовних 84 нот
% Завантаження музичного запису 88 нот в змінну z
path = "D:\Desktop\Studie\Diploma\GIT Matlab\Audio data\wav";
path1 = path + "\Sasha\Steinway Grand Piano 70.wav";
[y, Fs] = audioread(path1);
z = y(:,1);
clear path path1 y 

NOTES  = 84;                    % Кількість нот
NFFT   = 1024;                  % Ширина вікна
N_zero = Fs - NFFT;             % Кількість нулів для інтерполяції
Zer    = zeros(N_zero, 1);      % Вектор нулів для інтерполяції
N      = floor(2/(NFFT/Fs));    % Кількість сигналів для однієї ноти  

data = reshape(z,4*Fs,[]);      % Відокремлюю кожну ноту по рядкам
data = data(1:(N*NFFT),:);      % Округлюю кількість семплів для зручності
data = data(:, 1:87);           % Забираю зайву ноту До 5тої октави
data = data(:,4:end);           % Откидываю первые 3 ноты суб-контр октавы
clear z

% 2. Формування таблиці частот що відповідають 84 нотам
Tab_F_1 = [65.41  69.3  73.42  77.78  82.41  87.31  92.5  98  103.83  110  116.54  123.47];
k = 2.^(0:6) / 2;
Tab_F = k' .* repmat(Tab_F_1, 7, 1);
Indexes = floor(Tab_F);                % Таблиця індексів нот для інтерпольованого спектру
clear Tab_F_1 Tab_F k

% 3. Підготовка матриць M, V, Ms
M = zeros(7, 12);
Ms = M;
v1 = [1 1 1 1 1 1 1 ] * 1/7;
v2 = [0 1 1 1 1 1 1 ] * 1/6;
v3 = [0 0 1 1 1 1 1 ] * 1/5;
v4 = [0 0 0 1 1 1 1 ] * 1/4;
v5 = [0 0 0 0 1 1 1 ] * 1/3; 
v6 = [0 0 0 0 0 1 1 ] * 1/2;
v7 = [0 0 0 0 0 0 1 ];
V = [v1; v2; v3; v4; v5; v6; v7];
clear v1 v2 v3 v4 v5 v6 v7

% 4. Формування вектору міток Y
Y = 1:NOTES;
Y = repmat(Y, N, 1);
Y = reshape(Y, 1, [])';

% 5. Використання класифікатору
p_error = 0;                      % Змінна для зберігання кількості помилок
notes_lin = zeros(1, N*NOTES);    % Вектор для запису результатів класифікації

for i = 1:NOTES
    for j = 1:N
        
        % Обирається сигнал довжиною в NFFT з data
        n1 = (j-1)*NFFT + 1;                 
        n2 = (j)*NFFT; 
        S = data(n1:n2, i);
        
        % До сигналу додаються нулі для інтерполяції
        S2 = vertcat(Zer, S);
        
        % Знаходиться спектр та підраховується матриця Ms
        Spec = abs(fft(S2));        
        M = Spec(Indexes);         
        Ms = V * M;
        
        % Знаходиться індекс максимального елемента матриці Ms та
        % визначається нота, що записується в вектор notes_lin
        ar_ind = N*(i-1) + j;
        [~, Ind] = max(Ms',[],[1 2], 'linear');   
        notes_lin(ar_ind) = Ind;         
        
        if Ind ~= Y(ar_ind)
            p_error = p_error + 1;
        end   
    end
end

figure
plot(notes_lin)
hold on
plot(Y)
ylim([0, 84])

p_error = 100 * p_error / (N*NOTES);
disp('Error rate: ' + string(p_error) + '%')