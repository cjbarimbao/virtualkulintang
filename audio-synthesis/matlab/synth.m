function synth(filename, mode)
% SYNTH(FILENAME, MODE)
%   synthesize signal from its MD  saved in FILENAME.BIN
%   and the obtained parameters saved in FILENAME.DAT
%
% Frank Agsaway, UP DSP Lab, January 2005

if nargin < 2
    mode = 'def';
end

if filename(end-3) == '.'
    filename = filename(1:end-4);
end

datafile = strcat(filename,'.dat');
binfile = strcat(filename,'.bin');
output = strcat(sprintf('%s_%s_est.txt', filename, mode));



%read-------------------------
cd ('C:\Users\CJ\Desktop\virtualkulintang\audio-synthesis\matlab\binfiles')

if filename(end-3) == '.'
    filename = filename(1:end-4);
end
[s,e] = textread(datafile);
n = length(s);
%-end read--------------------

%---output
fp = fopen(output, 'wt');

i = 1;
cttf = 0;

[an, fn, Fs, dt] = modalest(binfile, s(i), e(i));
dt = dt / 1000;             % time interval

NperFrame = round(dt*Fs); 
Nf = length(an);             % num of frames
sig = zeros(NperFrame*Nf,1);
disp(sprintf('Synthesizing %s. Total number of partials: %d.', upper(filename), n));

if strcmp(mode, 'beed') %| strcmp(mode, 'pick') (for babandir)
    an = beed(an,dt);   % beed synth refinement
end

%---rev Feb 24
fprintf(fp, '%f %f %f\n', Nf, n, dt);
fprintf(fp, '%f ', an);
fprintf(fp, '\n');
fprintf(fp, '%f ', fn);
fprintf(fp, '\n');
%---end rev

% if strcmp(mode, 'pick')
%     while cttf == 0       
%         [an, fn] = modalest(binfile, s(i), e(i));
%         figure(1), plot(real(an)); title(sprintf('%s: amplitude(%d of %d)', upper(filename), i, n));
%         figure(2), plot(real(fn)); title(sprintf('%s: frequency(%d of %d)', upper(filename), i, n));xlabel(sprintf('mean freq = %.2f', mean(fn)));
%         cttf = input('Consider? (0/1):  ');
%         if cttf == 0
%             i = i+1;
%         end
%     end
% end

    par = sosinterp(an, fn, Fs, dt);
    sig = sig + par;

j = 1;
for i = j+1:n
    [an, fn, Fs, dt] = modalest(binfile, s(i), e(i));
    dt = dt / 1000;
       
    if strcmp(mode, 'beed') | strcmp(mode, 'pick')
        an = beed(an,dt);   % beed synth refinement
    end
%     plot(an);
%     pause;
    
%     if strcmp(mode, 'pick')
%         figure(1), plot(real(an)); title(sprintf('%s: amplitude(%d of %d)', upper(filename), i, n));
%         figure(2), plot(real(fn)); title(sprintf('%s: frequency(%d of %d)', upper(filename), i, n));xlabel(sprintf('mean freq = %.2f', mean(fn)));
%         cttf = input('Consider? (0/1):  ');
%         if cttf == 0
%             continue;
%         end
%     end
    
    fprintf(fp, '%f ', an);
    fprintf(fp, '\n');
    fprintf(fp, '%f ', fn);
    fprintf(fp, '\n');
    
    par = sosinterp(an, fn, Fs, dt);
    sig = sig + par;
end
fclose(fp);

%---save synth signal
cd ('C:\Users\CJ\Desktop\virtualkulintang\audio-synthesis\matlab\synthesized')
synthfilename = sprintf('%s_synth_%s.wav', filename, mode); % strcat(filename, '_synth_beed');
sig = 0.9*sig/max(abs(sig));
audiowrite(synthfilename, [sig sig], Fs);
disp([upper(synthfilename) '.WAV saved.']);
%eof