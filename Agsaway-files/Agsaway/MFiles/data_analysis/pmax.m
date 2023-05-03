function p = pmax(z);
% usage: 
%	p = pmax(z);


x = 1 + 0.196854*abs(z) + 0.115194*(abs(z)).^2 + 0.000344*(abs(z)).^3 + 0.019527*(abs(z)).^4;

p = 1-0.5/(x.^4);

if z < 0,
  p = 1-p;
end;