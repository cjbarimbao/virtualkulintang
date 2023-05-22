 function [A,F,Samp_Freq,dt]=modalest(fname,sbin,ebin)
% [A,F]=MODALEST(FNAME,SBIN,EBIN)
%   Amplitude and Frequency Estimation from the MD
%
%   gives the amp and freq estimates of a partial from the signal's 
%   Modal Distribution within the frequency bin indices SBIN to EBIN
%
%       FNAME is a *.bin file generated by the Modal Distribution Program
%       created by R.Guevara
%
%   plots the amp and freq estimates if no output is given
%
% Frank Agsaway, UP DSP Lab, January 2005

if (fname(end-3:end) ~= '.bin')
    fname = [fname '.bin'];
end

if (fname(2:3) ~= ':\')
    fname = [cd '\' fname];
end

fidr = fopen(fname,'rb');
if fidr == -1
    error(sprintf('Cannot open %s.\nPlease check path and filename.',upper(fname)));
end

%---Read *.bin file (taken from MODFILE2.M by R.Guevara)
TransLen = (fread(fidr,1,'int32'))/2;
SmoothSamps = fread(fidr,1,'int32');
DispInt = fread(fidr,1,'int32');
DispLen = fread(fidr,1,'int32');
Samp_Freq = fread(fidr,1,'int32');
Sample_Offset = fread(fidr,1,'int32');
msec_offset = Sample_Offset*1000/Samp_Freq;
df = Samp_Freq/(TransLen*4);
dt = DispInt*1000/Samp_Freq;
[data_in,cnt] = fread(fidr,'float');
fclose(fidr);
MD = reshape(data_in,TransLen,DispLen);
%---end read
MD(find(MD <= 0)) = eps;        % negative values have no interpretation
ridge = MD(sbin:ebin,:);
p = sum(ridge,1);                     % instantaneous power
A = (4/65535)*(p.^0.5);               % amplitude estimate
F = sum((([(sbin-1)*df:df:(ebin-1)*df]'*ones(1,size(ridge,2))).*ridge)...
    ./(ones(ebin-sbin+1,1)*p),1);     % freq estimate

if nargout == 0
    figure, plot(A); title('amplitude');
    figure, plot(F); title('frequency');
end
%eof