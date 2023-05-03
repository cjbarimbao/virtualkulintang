function separate (wavefile)
% separates each signal in a Kulintang signal WAVEFILE
%
% Frank Agsaway, UP DSP Lab, December 2, 2004

cd ('C:\FrankECE198\KulWavTRS');

if wavefile(end-3) == '.'
    wavefile = wavefile(1:end-2);
end
trsfile = strcat(wavefile,'.trs');

endpts = trsread(trsfile);
[kulsig, Fs, nbits] = wavread(wavefile);

for i = 1:size(endpts,1);
    tempsig = kulsig(endpts(i,1):endpts(i,2));
    if size(tempsig,2) == 1
        tempsig = [tempsig tempsig];    % convert to stereo
    end
    wavwrite(tempsig, Fs, nbits, [wavefile '_' num2str(sprintf('%.2d',i))]);
end

disp(sprintf('%s successfully separated into %d wavefiles and converted to stereo.', upper(wavefile), size(endpts,1))); 
%eof