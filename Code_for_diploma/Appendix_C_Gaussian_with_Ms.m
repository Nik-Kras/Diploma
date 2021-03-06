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
N      = floor(2/(NFFT/Fs));    % Кількість сигналів для однієї ноти  
ds     = 11;                    % В скільки разів обрізати спектр

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

% 4. Формування вектору міток Y та вектору об'єктів X
Y = zeros(N*NOTES, 1);
X = zeros([N*NOTES, NFFT+N_zero]);    % З інтерполяцією
% X = zeros([N*NOTES, NFFT]);         % Без інтерполяції

for k=1:NOTES
    N1 = N * (k-1) + 1;
    N2 = N1 + N - 1;
    notes = reshape(data(:,k),NFFT,N)';
    
    % Використовую віконну функцію Хаммінгу
    h = hamming(NFFT)';
    notes = notes .* h;
    
    X(N1:N2, 1:NFFT) = notes;
    Y(N1:N2) = k;
end

% 5. Розділяю дані на тренувальні та тестові
cv = cvpartition(Y,'HoldOut',0.30);
trainInds = training(cv);
testInds  = test(cv);

XTrain = X(trainInds,:);
YTrain = Y(trainInds);
XTest  = X(testInds,:);
YTest  = Y(testInds);
clear trainInds testInds X Y data

% 6. Проводжу попередню обробку сигналів
[STest, MTest]   = size(XTest);
[STrain, MTrain] = size(XTrain);

% Переводжу сигнали в частотний домен
XTest_spec  = abs(fft(XTest'))';
XTrain_spec = abs(fft(XTrain'))';

% Кількість відліків спектру після обрізання в векторах
vtest  = floor(1:MTest/ds);          
vtrain = floor(1:MTrain/ds);

% Обрізаю спектри в ds разів
XTest_ds  = zeros([STest, length(vtest)]);
XTrain_ds = zeros([STrain, length(vtrain)]);
XTest_ds(:, vtest)  = XTest_spec(:, vtest);
XTrain_ds(:, vtest) = XTrain_spec(:, vtest);

% Нормалізація спектрів
XTest_ds  = XTest_ds ./ sum(XTest_ds, 2);
XTrain_ds = XTrain_ds ./ sum(XTrain_ds, 2);
clear XTrain XTest XTest_spec XTrain_spec

% 7. Знаходження параметрів Гаусівських розподілів матриць Ms
mean_M = zeros([NOTES 7 12]);   % Масив для мат очікувань
std_M  = zeros([NOTES 7 12]);   % Масив для дисперсій

for i = 1:NOTES
    % Отримую всі сигнали, що належать до заданої ноти
    ind = find(YTrain==i); 
    X_note = XTrain_ds(ind, :);
    
    Ncuts = length(ind);
    temp_M = zeros([Ncuts 7 12]);
    for k = 1:Ncuts
        x = X_note(k, :);       % Обираю єдиний сигнал даної ноти     
        M  = x(Indexes);        % Отримаю матрицю Ms для цього сигналу
        Ms = V * M;             %
        temp_M(k, :, :) = Ms;   % Зберігаю матриці Ms обраної ноти в масив
    end
    mean_M(i, :, :) = mean(temp_M, 1);  % Отримую параметри Гаусівських розподілів
    std_M(i, :, :)  = std(temp_M, 1);   % Зі збережених матриць Ms для обраної ноти 
end

% 8. Використання класифікатору
p_error  = 0;                   % Змінна для зберігання кількості помилок
my_notes = zeros([STest 1]);    % Вектор для запису результатів класифікації
for j = 1:STest
    
    test_sig = XTest_ds(j, :);      % Обирається єдиний сигнал для класифікації
    test_label = YTest(j);          % Запам'ятовується його мітка

    M = test_sig(Indexes);          % Отримую матрицю Ms для обраного сигналу
    Ms = V * M;                     %
    
    Prob_note = ones([NOTES, 1]);   % Вектор вірогідності належності до кожної ноти
    
    for i = 1:NOTES
        
        for k = 1:(7*12)
            
            m = Ms(k);                % Обирається відлік матриці Ms
            std_cur  = std_M(i, k);   % Беруться відповідні параметри Гаусу
            mean_cur = mean_M(i, k);  % 
            
            % Рахується гаусівський розподіл
            p = gaussmf(m, [std_cur mean_cur]);
    
            % Знаходиться вірогідність належності до кожної ноти
            Prob_note(i) = Prob_note(i) * p;
        end
        
    end
    
    % Обирається нота за максимальною вірогідністю
    note = find(Prob_note==max(Prob_note));
    
    % У випадку декількох максимумів - обирається перший
    my_notes(j) = note(1);
    
    % перевірка на помилковий результат
    if my_notes(j) ~= test_label
        p_error = p_error + 1;
    end  
    
end

figure
plot(YTest)
hold on
plot(my_notes)
hold off

p_error = 100 * p_error / STest;
disp('Error rate: ' + string(p_error) + '%')