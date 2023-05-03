addpath ('C:\FrankECE198\Work');
clear
clc

for z = 1:5
    ins = {'agong1', 'babandir1', 'dabakan1', 'gandingan1', 'kulintang1'};
    num = { num2str(1:18), num2str(1:12), num2str(1:18), num2str(1:24), num2str(1:24)};
%     num = { num2str([3 5 9 11 13 18]), num2str([2 5 8 10]), num2str([2 5 7]), num2str([5 10 3 8 13 18 19 20]), num2str([9 7])};
    wavefile = char(ins(z));
    list = str2num(char(num(z)));

    tol = 60;           %dB tolerance

for i = list
    fname = [wavefile '_' num2str(sprintf('%.2d',i))];
%     GetBoundaries(fname,tol);
%     synth(fname, 'beed');

%     %---
%     [o, s] = add_wnoise(fname);
%     cd ('C:\FrankECE198\KulSynthNoise')
%     wavwrite(o,44100,16,sprintf('%s_orig_wnoise',fname));
%     disp(sprintf('%s_orig_wnoise saved',fname));
%     wavwrite(o,44100,16,sprintf('%s_synth_beed_wnoise',fname));
%     disp(sprintf('%s_synth_beed_wnoise saved',fname));
%     %---
  
end

clear;

end