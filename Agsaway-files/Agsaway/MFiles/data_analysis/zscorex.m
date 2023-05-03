function z = zscore(p);
% usage:
%	z = zscore(p);

pdum = p;

if pdum >= 0.5,
  pdum = 1-pdum;
end;

if pdum == 0,
  pdum = 0.0001;
end;

z = sqrt(-2*log(pdum));
z = z - ((2.30753+0.27061*z)/(1+0.99229*z+0.04481*z.^2));

if p >= 0.5,
  z = -z;
end;