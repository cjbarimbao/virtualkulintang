function playkul (scoretitle, tempo, agongnum, astyle, bstyle, dstyle, gstyle)
% PLAYKUL (scoretitle, tempo, agongnum, astyle, bstyle, dstyle, gstyle)
%   plays a Kulintang musical score, SCORETITLE
%
%   TEMPO in beats per minute
%   AGONGNUM  agong gong number             1   gong1
%                                           2   gong2
%   ASTYLE    agong surface-hitting style   1   padded mallet       (style2 in docu)
%                                           2   unpadded mallet     (style3 in docu)
%               (style1 boss hit
%   BSTYLE    babandir hitting style        1   unmuffled boss
%                                           2   unmuffled rim
%                                           3   muffled boss 
%                                           4   muffled rim
%   DSTYLE    dabakan hitting style         1   center, stick only slaps the drumskin
%                                           2   off-center, stick only slaps the drumskin
%                                           3   center, stick slaps the drumskin and the rim
%   GSTYLE    gandingan hitting style       1   unmuffled boss
%                                           2   surface
%
%   DEFAULT: tempo = 220, agongnum=1, astyle=1, bstyle=1, dstyle=1, gstyle=1
%
% Frank Agsaway, UP DSP Lab, March 2005

cd ('C:\FrankECE198\KulDemo');

if nargin < 3
    agongnum = 1;
    astyle = 1;
    bstyle = 1;
    dstyle = 1;
    gstyle = 1;
end
if nargin < 2
    tempo = 220;
end

beatdur = 60/tempo; % beat duration
Fs = 44100;
shorthit = 8;       % 1/8 beat
global k0 k1 k2 k3 k4 k5 k6 k7 k8;


introhits = 8;      % 8 hits during introduction
again = 2;          % gain for agong hit
bgain = 1;          % gain for babandir hit
dgain = 1;          % gain for dabakan hit
ggain = 2;          % gain for gandingan hit
kgain = 2;          % gain for kulintang hit

% read musical scores
a = textread(sprintf('%s_a.txt', scoretitle));
b = textread(sprintf('%s_b.txt', scoretitle));
d = textread(sprintf('%s_d.txt', scoretitle));
g = textread(sprintf('%s_g.txt', scoretitle));
k = textread(sprintf('%s_k.txt', scoretitle));

% read wavfiles
a1 = wavread(sprintf('a%d1', agongnum));
a2 = wavread(sprintf('a%d%d', agongnum, astyle));
b1 = wavread(sprintf('b%d', bstyle));
d1 = wavread(sprintf('d%d', dstyle));
g1 = wavread(sprintf('g1%d', gstyle));
g2 = wavread(sprintf('g2%d', gstyle));
g3 = wavread(sprintf('g3%d', gstyle));
g4 = wavread(sprintf('g4%d', gstyle));
k1 = wavread('k1');
k2 = wavread('k2');
k3 = wavread('k3');
k4 = wavread('k4');
k5 = wavread('k5');
k6 = wavread('k6');
k7 = wavread('k7');
k8 = wavread('k8');

a0 = zeros(floor(beatdur*44100),2);     % initialize variables to play to zeros
b0 = a0;
d0 = a0;
g0 = a0;
k0 = a0;


dintroset = d(1:introhits);                 % dabakan hits to play
dintrobeats = d(introhits+1:2*introhits);   % beats of dabakan hits to play
setlen = 0.5*(length(d) - 2*introhits);


ds = 2*introhits + 1;                   % start index
de = ds + setlen - 1;                   % end index
loopdset = d(ds:de);                    % set of dabakan hits to loop
loopdbeats = 1./d(de+1:end);            % set of beats for dabakan hits to loop

loopaset =a(1:0.5*length(a));           % agong hits to loop
abeats = 1./a(0.5*length(a)+1:end);     % set of beats for agong hits to loop

loopbset = b(1:0.5*length(b));          % babandir hits to loop
bbeats = 1./b(0.5*length(b)+1:end);     % set of beats for babandir hits to loop

loopgset = g(1:0.5*length(g));          % gandingan hits to loop
gbeats = 1./g(0.5*length(g)+1:end);     % set of beats for gandingan hits to loop

ind = 1;                                % start at first kulintang hit

while ind < length(k)                   % do until all kulintang hits are played
    
    if ind == 1
        dset = dintroset;
        dbeats = dintrobeats;
        aset = zeros(size(loopaset));
        bset = zeros(size(loopbset));
        gset = zeros(size(loopgset));
    else
        dset = loopdset;
        dbeats = loopdbeats;
        aset = loopaset;
        bset = loopbset;
        gset = loopgset;
    end
        
    
numhits = k(ind);                       % num of hits
set_sind = ind + 1;                     % set start index
set_eind = set_sind + numhits - 1;      % set end index
rep = k(set_eind + 1);                  % repetitions
beat_sind = set_eind + 2;               % beat start index
beat_eind = beat_sind + numhits - 1;    % beat end index

kset = k(set_sind:set_eind);            % rhythm
kbeats = k(beat_sind:beat_eind);        % beat

% short hits
shorthitind = find(kbeats == 0);
kbeats(shorthitind) = shorthit;
kbeats(shorthitind+1) = (shorthit*kbeats(shorthitind+1))/(shorthit - kbeats(shorthitind+1));

while rep > 0 
    rep = rep - 1;
    aind = 0;
    bind = 0;
    gind = 0;
    dind = 0;
    kind = 0;
    pass = 0;
    while kind  < numhits
        if aind > length(aset)-1        % reset / return to first index of loop
            aind = 1;
        end
        if bind > length(bset)-1
            bind = 1;
        end
        if dind > length(dset)-1
            dind = 1;
        end
        if gind > length(gset)-1
            gind = 1;
        end

        if isempty(find(pass==1))
            aind = aind + 1;                                
            ahit = again*eval( sprintf('a%d',aset(aind)) );     % hit   
            abeat = abeats(aind);                               % beat
            ap = audioplayer(ahit,44100);                       % sound out
            play(ap);
            disp(sprintf('A%d %.2f', aset(aind), abeat));
        end
        if isempty(find(pass==2))
            bind = bind + 1;   
            bhit = bgain*eval( sprintf('b%d',bset(bind)) );  
            bbeat = bbeats(bind);
            bp = audioplayer(bhit,44100);
            play(bp);
            disp(sprintf('B%d %.2f', bset(bind), bbeat));
        end 
        if isempty(find(pass==3))
            gind = gind + 1; 
            ghit = ggain*eval( sprintf('g%d',gset(gind)) ); 
            gbeat = gbeats(gind);        
            gp = audioplayer(ghit,44100);
            play(gp);  
            disp(sprintf('G%d %.2f', gset(gind), gbeat));
        end 
        if isempty(find(pass==4))
            dind = dind + 1;
            newdind=dset(dind);
            if newdind == 11
                newdind = 1;      
                dhit = 2*dgain*eval( sprintf('d%d',newdind) );
            else
                dhit = dgain*eval( sprintf('d%d',newdind) );
            end
            dbeat = dbeats(dind); 
            dp = audioplayer(dhit,44100);
            play(dp);
            disp(sprintf('D%d %.2f', newdind, dbeat));
        end
        if isempty(find(pass==5))
            kind = kind + 1;
            khit = kgain*gethit(kset(kind));
            kbeat = 1/kbeats(kind);
            kp = audioplayer(khit,44100);
            play(kp);
            disp(sprintf('K%d %.2f', kset(kind), kbeat));
        end
        
              
        beatlist = [abeat bbeat gbeat dbeat kbeat];     % list of beats of each instrument
        minbeat = min(beatlist);                        % minimum beat
        pass = find(beatlist > minbeat);                % instruments to pass, pass=1 agong, 2 babandir, 3 gandingan,4 dabakan, 5 kulintang
        if isempty(pass) 
            pass = 0;
        end
        
        abeat = abeat - minbeat;                        % decrement beat duration of each instrument by minimum beat
        bbeat = bbeat - minbeat;
        dbeat = dbeat - minbeat;
        gbeat = gbeat - minbeat;
        kbeat = kbeat - minbeat;
        

        pause(minbeat*beatdur);                         % pause to the duration of the minimum beat
        
        disp(' ');
    end 
end

ind = beat_eind + 1;

end

%---
function hit = gethit(hitval)
global k0 k1 k2 k3 k4 k5 k6 k7 k8;
if hitval > 10          % two hits
   hit1 = eval( sprintf('k%d',floor(hitval/10) ) );
   hit2 = eval( sprintf('k%d',rem(hitval,10) ) );
   lendiff = length(hit1) - length(hit2);
    if lendiff > 0
        hit2 = [hit2;zeros(lendiff,2)];
    else
        hit1 = [hit1;zeros(-lendiff,2)];
    end            
    hit = hit1 + hit2;
else                    % single hit
    hit = eval( sprintf('k%d',hitval) );
end