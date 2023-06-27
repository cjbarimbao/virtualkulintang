% addpath ('C:\FrankECE198\Work');
clear
clc

gongs = 8;
samples = 5;

tol = 60;           %dB tolerance

for i = 1:gongs
    for j = 1:samples
        fname = sprintf('g%.1d_s%.1d_l',i,j);
        getboundaries(fname,tol);
        fname = sprintf('g%.1d_s%.1d_r',i,j);
        getboundaries(fname,tol);
        fname = sprintf('g%.1d_s%.1d',i,j);
        synth_stereo(fname, 'beed');
    end
    %synth(fname); %default settings

%     %--- add wnoise
%
%     [o, s] = add_wnoise(fname);
%     cd ('C:\FrankECE198\KulSynthNoise')
%     wavwrite(o,44100,16,sprintf('%s_orig_wnoise',fname));
%     disp(sprintf('%s_orig_wnoise saved',fname));
%     wavwrite(o,44100,16,sprintf('%s_synth_beed_wnoise',fname));
%     disp(sprintf('%s_synth_beed_wnoise saved',fname));
%     %---

end

clear;


