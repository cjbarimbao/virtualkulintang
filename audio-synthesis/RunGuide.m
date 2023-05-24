% addpath ('C:\FrankECE198\Work');
clear
clc

gongs = 8;
samples = 5;

tol = 60;           %dB tolerance

for i = 1:gongs
    fname = sprintf('g%.1d_s%.1d_r',i,samples);
    getboundaries(fname,tol);
    synth(fname, 'beed');
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


