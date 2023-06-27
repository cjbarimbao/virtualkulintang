clear; clc;
gongs = 8;
samples = 5;
for i = 1:gongs
    for j = 1:samples
        filename = sprintf('Mgd_Kulintangan_30%.1d_P1_N0_S%.1d.mp3', i, j); 
        [Y, Fs] = audioread(filename);
        o_filename = sprintf('Mgd_Kulintangan_30%.1d_P1_N0_S%.1d.wav', i, j);
        audiowrite(o_filename, Y, Fs);
    end
end