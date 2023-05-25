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
    filename = filename(1:end-6);
end
datafile = cell(2,1); binfile = cell(2,1); sig = cell(2,1);

datafile{1} = strcat(filename,'_l.dat');
binfile{1} = strcat(filename,'_l.bin');
datafile{2} = strcat(filename,'_r.dat');
binfile{2} = strcat(filename,'_r.bin');
output = strcat(sprintf('%s_%s_est_stereo.txt', filename, mode));


%read-------------------------
cd ('C:\Users\CJ\Desktop\virtualkulintang\audio-synthesis\binfiles')

for k = 1:2
    
    [s,e] = textread(datafile{k});
    n = length(s);
    %-end read--------------------

    %---output
    fp = fopen(output, 'wt');

    i = 1;
    cttf = 0;

    [an, fn, Fs, dt] = modalest(binfile{k}, s(i), e(i));
    dt = dt / 1000;             % time interval

    NperFrame = round(dt*Fs); 
    Nf = length(an);             % num of frames
    sig{k} = zeros(NperFrame*Nf,1);
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
        sig{k} = sig{k} + par;

    j = 1;
    for i = j+1:n
        [an, fn, Fs, dt] = modalest(binfile{k}, s(i), e(i));
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
        sig{k} = sig{k} + par;
    end
    fclose(fp);

end
%---save synth signal
cd ('C:\Users\CJ\Desktop\virtualkulintang\audio-synthesis\synthesized')
synthfilename = sprintf('%s_synth_%s.wav', filename, mode); % strcat(filename, '_synth_beed');
left = 0.9*sig{1}/max(abs(sig{1}));
right = 0.9*sig{2}/max(abs(sig{2}));
audiowrite(synthfilename, [left right], Fs);
disp([upper(synthfilename) 'saved.']);
%eof