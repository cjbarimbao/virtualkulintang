function x_out = dbmtx(x_in,dbrange,xmax);
%Usage: x_out = dbmtx(x_in,dbrange,xmax),
%       where x_in is a vector of the input signal (real or complex)
%       x_out is the output signal
%       dbrange is the range in dB
% 	xmax is the maximum value that corresponds to dbrange
%       IT IS ASSUMED THAT x_in is amplitude, not energy

dbmin = xmax*(10^(-dbrange/10));
dummy = x_in > dbmin*ones(size(x_in));
x_out = dbmin*(~dummy) + x_in.*dummy;
x_out = 10*log10(x_out/dbmin);          