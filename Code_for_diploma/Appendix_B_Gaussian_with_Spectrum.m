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

% 2. Формування вектору міток Y та вектору об'єктів X
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

% 3. Розділяю дані на тренувальні та тестові
cv = cvpartition(Y,'HoldOut',0.30);
trainInds = training(cv);
testInds  = test(cv);

XTrain = X(trainInds,:);
YTrain = Y(trainInds);
XTest  = X(testInds,:);
YTest  = Y(testInds);
clear trainInds testInds X Y data

% 4. Проводжу попередню обробку сигналів
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

% 5. Знаходження параметрів Гаусівських розподілів
mean_ds = zeros([length(vtrain), NOTES]); % Масив для мат очікувань
std_ds  = zeros([length(vtrain), NOTES]); % Масив для дисперсій
for num_notes = 1 : NOTES
    % Отримую всі сигнали, що належать до заданої ноти
    ind   = find(YTrain==num_notes);
    X_cur = XTrain_ds(ind, :);
    % Знаходжу мат очікування та дисперсію окремих відліків по сигналам
    mean_ds(:,num_notes) = mean(X_cur,1)';
    std_ds(:,num_notes)  = std(X_cur,1,1)';
end

% 6. Використання класифікатору
p_error  = 0;                   % Змінна для зберігання кількості помилок
my_notes = zeros([STest 1]);    % Вектор для запису результатів класифікації
for j = 1:STest
    
    test_sig = XTest_ds(j, :);      % Обирається єдиний сигнал для класифікації
    test_label = YTest(j);          % Запам'ятовується його мітка
    
    Prob_note = ones([NOTES, 1]);   % Вектор вірогідності належності до кожної ноти
    
    for i = 1:NOTES
        
        for k = 1:length(vtrain)
            
            x = test_sig(k);           % Обирається єдиний відлік сигналу
            std_cur = std_ds(k, i);    % Беруться відповідні параметри Гаусу
            mean_cur = mean_ds(k, i);  % 
            
            % Використовується грубе апроксимування Гаусу для великих
            % відстаней від математичного очікування
            if abs(x-mean_cur) > 3*std_cur
                p = 0.001;
            else
                p = gaussmf(x, [std_cur mean_cur]);
            end
            
            % Знаходяться вірогідності для кожної ноти
            Prob_note(i) = Prob_note(i) + log(p); 
            
        end
        
    end
    
    % Обирається нота за максимальною вірогідністю
    note = find(Prob_note==max(Prob_note));
    
    % У випадку декількох максимумів - обирається перший
    my_notes(j) = note(1);
    
    % перевірка на помилковий результат
    if my_notes(j) ~= YTest(j)
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