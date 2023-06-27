function [on, sn] = add_wnoise(filename)
% [on, sn] = add_wnoise(filename)
%   -noise masks the original and synthesized signals of FILENAME
%   -prompts the user to increase or decrease intensity of noise to be used
%       for masking until the desired value is reached
%   -returns the noise masked original and synthesized signals in ON and SN, respectively
%
% Frank Agsaway, UP DSP Lab, March 2005

if filename(end-3) == '.'
    filename = filename(1:end-4);
end
cd ('C:\FrankECE198\KulWavTRS')
o = wavread(filename);

cd ('C:\FrankECE198\KulSynth')
s = wavread(sprintf('%s_synth_beed',filename));

nmax = max(o(end-4410:end,1));      % noise energy

choice = 1;
scale = 0;
step = 0.01;
while choice ~= 0
n = scale*nmax*randn(size(o));     % white noise

on = o + n(1:size(o,1),:);
sn = s + n(1:size(s,1),:);

on = 0.9*(on/max(max(abs(on))));
sn = 0.9*(sn/max(max(abs(sn))));

disp(sprintf('scale: %f', scale));
soundsc([on;zeros(4410,2);sn], 44100);
choice = input('down:1 up:2 >>');
if choice ~= 1 & choice ~= 2
    scale = scale - choice;
end
if choice == 1
    scale = scale - step;
end
if choice == 2
    scale = scale + step;
end

end %while
disp(sprintf('scale: %f', scale));

fp = fopen('C:\FrankECE198\noiseamps.txt', 'a');
fprintf(fp, sprintf('%s %f\n', filename, scale*nmax));
fclose(fp);
%eof