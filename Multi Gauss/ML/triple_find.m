function values = triple_find(s)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
L = length(s);

m1 = L/3;
m2 = 2*L/3;

dots = [m1 m2];
values = s(dots);

end

