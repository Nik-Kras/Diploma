function p_correct = GetReward(NFFT)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

path = "D:\Desktop\Studie\Diploma\GIT Matlab\Audio data\wav";
path1 = path + "\Sasha\Steinway Grand Piano 70.wav";
[y, Fs] = audioread(path1);
z = y(:,1);

clear y

NFFT = floor(NFFT);
N_zero = Fs - NFFT;     % Кол-во нулей после вырезки. Я буде для частотного шага 1Гц
N = floor(2/(NFFT/Fs)); % Количество вырезок за 2 секунды
ds = 2;                 % В сколько раз уменьшить спектр. Минимум 2 - нормально

NOTES = 88;

Tab_F_1 = [65.41  69.3  73.42  77.78  82.41  87.31  92.5  98  103.83  110  116.54  123.47];
k = 2.^(0:7) / 2;
Tab_F = k' .* repmat(Tab_F_1, 8, 1);

M = zeros(8, 12);
Ms = M;

Indexes = floor(Tab_F);   % NOT FLAT!!!
v1 = [1 1 1 1 1 1 1 1] * 1/8;
v2 = [0 1 0 1 0 1 0 1] * 1/3;
v3 = [0 0 1 0 0 1 0 0] * 1/2;
v4 = [0 0 0 1 0 0 1 0] * 1/2;
v5 = [0 0 0 0 1 0 0 0]; 
v6 = [0 0 0 0 0 1 0 0];
v7 = [0 0 0 0 0 0 1 0];
v8 = [0 0 0 0 0 0 0 1];
V = [v1; v2; v3; v4; v5; v6; v7; v8];

data = reshape(z,4*Fs,[]);  % Каждая нота отдельно
data = data(1:N*NFFT, :);   % Каждая нота отдельно Без нулей

Y = zeros(N*NOTES, 1);
X = zeros([N*NOTES, NFFT+N_zero]);    % С интерполяцией
% X = zeros([N*NOTES, NFFT]);             % Без интерполяции

for k=1:NOTES
    
    N1 = N * (k-1) + 1;
    N2 = N1 + N - 1;
    
    notes = reshape(data(:,k),NFFT,[])';
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% OPTIONAL
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Window function
    % Add Hamming window
    h = hamming(NFFT)';
    notes = notes .* h;
    
    X(N1:N2, 1:NFFT) = notes;
    Y(N1:N2) = k;
    
end

cv = cvpartition(Y,'HoldOut',0.30);
trainInds = training(cv);
testInds = test(cv);

XTrain = X(trainInds,:);
YTrain = Y(trainInds);
XTest = X(testInds,:);
YTest = Y(testInds);

clear X Y z

[STest, MTest] = size(XTest);
[STrain, MTrain] = size(XTrain);

vtest = floor(1:MTest/ds);
vtrain = floor(1:MTrain/ds);

XTest_ds = zeros([STest, length(vtest)]);
XTrain_ds = zeros([STrain, length(vtrain)]);

% Get Spectrum. There is no need to get whole spectrum, It can be divided
% by half or more. ds - specifies how spectrum will be divided.
XTest_spec = abs(fft(XTest'))';
clear XTest 
XTrain_spec = abs(fft(XTrain'))';
clear XTrain

% Get only one part of spectrum, only important samples
XTest_ds(:, vtest) = XTest_spec(:, vtest);
XTrain_ds(:, vtest) = XTrain_spec(:, vtest);

clear XTest_spec XTrain_spec vtest vtrain

% Normalization of data
XTest_ds = XTest_ds ./ sum(XTest_ds, 2);
XTrain_ds = XTrain_ds ./ sum(XTrain_ds, 2);

mean_M = zeros([NOTES 8 12]);
std_M = zeros([NOTES 8 12]);

% i = number of note
for i = 1:NOTES
    
    ind = find(YTrain==i); 
    X_note = XTrain_ds(ind, :);
    
    Ncuts = length(ind);
    temp_M = zeros([Ncuts 8 12]);
    
    % k = single cut of NFFT
    for k = 1:Ncuts
        
        x = X_note(k, :);    % Current signal
        
        M = x(Indexes);          % Заполняем матрицу нот
        Ms = V * M;
        
        temp_M(k, :, :) = Ms;

    end
    
    mean_M(i, :, :) = mean(temp_M, 1);
    std_M(i, :, :) = std(temp_M, 1);

end

p_correct = 0;                  % Reward !!!
my_notes = zeros([STest 1]);
true_notes = zeros([STest 1]);

for j = 1:STest
    
    test_sig = XTest_ds(j, :);
    test_label = YTest(j);

    M = test_sig(Indexes);          % Заполняем матрицу нот
    Ms = V * M;
    
    Prob_note = ones([NOTES, 1]);
    
    % i = number of note
    for i = 1:NOTES
        
        % k = single sample of Ms
        for k = 1:(8*12)
            
            m = Ms(k);
            std_cur = std_M(i, k);    % Current std
            mean_cur = mean_M(i, k);  % Current mean
             
            p = gaussmf(m, [std_cur mean_cur]);
    
            Prob_note(i) = Prob_note(i) * p;
        end
        
    end
    
    note = find(Prob_note==max(Prob_note));
    
    if note == test_label
        p_correct = p_correct + 1;
    end
    
    my_notes(j) = note(1);% Sometimes it returns 1x88 zeros vector  
    true_notes(j) = test_label;
    
end

p_correct = 100 * p_correct / STest;    % That is a reward

end

