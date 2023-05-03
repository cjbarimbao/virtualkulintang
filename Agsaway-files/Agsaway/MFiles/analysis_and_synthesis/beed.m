function y = beed(x,dt)
% beed(filename, newfilename)
%   BEED Synthesis
%   x   signal
%   dt  time interval per frmae in seconds
%
% Frank Agsaway, UP DSP Lab, January 2005

[a1, kon] = max(x);                 % kon is the onset time (peak value)
if kon > length(x)-16              
    y = zeros(size(x));
    return;
end

a2 = 0;
i = 1;
while (a2 < a1) & i < 16
    a2 = x(kon+i);
    i = i+1;
end
if a2 == 0
    y = zeros(size(x));
    return;
end
tau = (-dt*i) / (log(a2/a1));           % time constant

y = x;
for k = 1:kon-2
    y(kon-k) = a1/exp((-dt*k)/tau);
end
% for k = 1:kon-2
%     y(kon-k) = a1/exp((-dt*k)/tau);
% end
% y(1) = 0;

%eof