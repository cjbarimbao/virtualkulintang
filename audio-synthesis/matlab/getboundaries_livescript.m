%% get files and directories
filename = 'g1_s1_r';
dBtol = 60;
% GetBoundaries(filename, dBtol)
%
%   Picks the starting and ending boundaries of the partials 
%   of a signal from its MD values, ignoring values with 
%   more than DBTOL attenuation from the maximum value. (60dB)
%   
%   The MD is saved in <FILENAME>.BIN
%   The starting and ending bin indices of the boundaries
%   are saved in a data file <FILENAME>.DAT.
%
% Frank Agsaway,UP DSP Lab, January 2005

clc
addpath ('/Users/cjbarimbao/Documents/MATLAB/kulintang-synth');    % path of pickpeak.m
cd ('/Users/cjbarimbao/Documents/MATLAB/kulintang-synth/binfiles');    % directory of bin and dat files

%% open file

if (filename(end-3:end) ~= '.bin')
    filename = [filename '.bin'];
end

% if (filename(2:3) ~= ':\')
%     filename = [cd '\' filename];
% end
if (filename(1) ~= '/')
    filename = [cd '/' filename];
end

fidr = fopen(filename,'rb');
if fidr == -1
    error(sprintf('Cannot open %s.\nPlease check path and filename.',upper(filename)));
end

fc = 31.25;     % Minimum fc of MDProgram

%% parse .bin file
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

dBtol = -dBtol;
MDlin=MD;
MDlin(find(MDlin <= 0)) = 10^(dBtol/10);        % negative values have no interpretation
MDlog = 10*log10(MDlin/max(max(abs(MDlin))));   % normalize and convert to log scale
MDlog(find(MDlog < dBtol)) = dBtol;             % ignore values below tolerance

sbin =[];
ebin = [];
disp(sprintf('\n%s: Total number of time slices: %d', upper(filename), DispLen));
disp(sprintf('Processing time slices. \n 1 > '));
for i = 1:DispLen
    if mod(i,10) == 0
        disp(sprintf('%d >', i));
    end
    [bin,val] = pickpeak(MDlog(:,i),TransLen,ceil((fc)/df)); 
    bin([find(bin==0);find(val==dBtol);find(bin==1)]) = [];
    if bin(1) == 1
        bin(1) = [];
    end
    parlist = sort(bin);
    
numpar = length(parlist);   % num of candidate partials
s = parlist - 1;            % start bin
e = parlist + 1;            % end bin
e(find(e>TransLen)) = TransLen; % subtract 1 from par = TransLen
sok = 1:length(s);
eok = 1:length(e);
while ~isempty(sok) & ~isempty(eok)
    if (s(1) > 1) & (MDlog(s(1),i) > dBtol)    % start 1
        s(1) = s(1) - 1;
    end
    if (e(end) < TransLen-1) & (MDlog(e(end),i) > dBtol) % end last
        e(end) = e(end) + 1;
    end
    sok2 = intersect( find(MDlog(s(2:end),i) > dBtol),  find(s(2:end) > e(1:end-1)) ); % within tol, right of prev end, +1 due to offset
    sok = sok2( find( (MDlin(s(sok2+1)-1,i) - MDlin(s(sok2+1),i)) < 0) );
    s(sok+1) = s(sok+1) - 1;
    
    eok2 = intersect( find(MDlog(e(1:end-1),i) > dBtol), find(e(1:end-1) < s(2:end)) ); % within tol, left of next start
    eok = eok2( find( (MDlin(e(eok2)+1,i) - MDlin(e(eok2),i )) < 0) );
    e(eok) = e(eok) + 1;
end

if i == 1
    sbin = s;
    ebin = e;
    continue;
end

if length(s) > size(sbin,1) % save      s:col       sbin:each col rep tslice
    sbin = [sbin;zeros(length(s)-size(sbin,1),size(sbin,2))];
end
if length(s) < size(sbin,1)
    s = [s;zeros(size(sbin,1)-length(s),1)]; 
end
sbin = [sbin s];

if length(e) > size(ebin,1) % save
    ebin = [ebin;zeros(length(e)-size(ebin,1),size(ebin,2))];
end
if length(e) < size(ebin,1)
    e = [e;zeros(size(ebin,1)-length(e),1)]; 
end
ebin = [ebin e];

end

%% plot
%---plots
bmap = zeros(TransLen, DispLen);
for i = 1:DispLen
    s = sbin(:,i);
    s(find(s==0)) = [];
    e = ebin(:,i);
    e(find(e==0)) = [];
    bmap(s,i) = 1;
    for j = 1:length(e)
        if bmap(e(j),i) == 1
            bmap(e(j),i) = 3;
        else
            bmap(e(j),i) = 2;
        end
    end   
end

%%
y = length(filename);
while filename(y)~= '/'
    y = y - 1;
end
figname = filename(y+1:end);
figname(end-3:end) = [];

%%

% cd ('C:\FrankECE198\KulFig');
% hgsave(h, sprintf('%s.fig',figname));
disp(sprintf('Figure saved in %s.FIG',upper(figname)));

figure(8), hold on;
step = floor(DispLen/8);
col = 'kbgmrcy';
for i = 1:step:DispLen-3*step
    plot(MDlin(:,i),col(floor((i+step-1)/step)));
    plot(MDlin(:,i+1),col(floor((i+step-1)/step)));
    plot(MDlin(:,i+2),col(floor((i+step-1)/step)));
    plot(MDlin(:,i+3),col(floor((i+step-1)/step)));
    plot(MDlin(:,i+4),col(floor((i+step-1)/step)));
end

%--- plot Map of Boundaries
title(sprintf('%s',figname));
xlabel('time slice');
ylabel('freq bin');

    figure(9), plot(MDlin(:,DispLen),'y');
    title('increasing time: black blue green magenta red cyan yellow');
    xlabel(sprintf('time step = %d', step));

%%
%---Get boundaries
findnext = 2;
st = 1;
en = [];
while isempty( find(bmap(st,:)) )
    st = st + 1;
end
for i = st:TransLen
    if isempty( [find(bmap(i,:)==findnext) find(bmap(i,:)==3)] )    % find next boundary
        continue;
    end
    if findnext == 1    % starting boundary
        findnext = 2;
        if st == 1
            findnext = 2;
        end
        st = [st;i];
        ip = i-1;   % trace til last detected end
        while isempty( [find(bmap(ip,:)== 2) find(bmap(ip,:)==3)] ) & (ip > 1)   % trace until last detected end
            ip = ip-1;
        end
        en = [en;ip];
    else            % ending boundary
        findnext = 1;   
    end
end
lastpt = TransLen;
while isempty( find(bmap(lastpt,:)) )
    lastpt = lastpt - 1;
end
en(end+1) = lastpt;

ignore = find(en-st <= 2);  % min 3-bin separation
st(ignore) = [];
en(ignore) = [];

%---extra
% cd ('C:\FrankECE198\KulBinDat')
fp = fopen([figname '.dat'],'w');

% hold on
for i = 1:length(st)
%     plot(1:DispLen,st(i)*ones(1,DispLen),'b');
%     plot(1:DispLen,en(i)*ones(1,DispLen),'g');
    fprintf(fp,'%d %d\n',st(i), en(i));
end
fclose(fp);
disp(sprintf('Partial boundaries saved in %s.DAT',upper(figname)));
    
if length(st) == 0
    pause;
end
disp ('GETBOUNDARIES ok');
%eof