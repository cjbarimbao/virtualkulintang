function sig = sosinterp(a, f, Fs, dt)
% sig = sosinterp(a, f, Fs, dt)
%
% Frank Agsaway, UP DSP Lab, January 2005


% dt = dt / 1000;         time interval
NperFrame = round(dt*Fs); 

Nf = length(a);         % num of frames

dA = [a(2:end) 0] - a; 
dA = dA / NperFrame;   % amplitude increment

asyn = zeros(NperFrame*Nf,1);      % Each row in Ats represents the interpolated amp values of each partial
asyn(1:NperFrame:end) = a;
for i = 2:NperFrame
    asyn(i:NperFrame:end) = asyn(i-1:NperFrame:end) + dA';
end
fsyn = zeros(NperFrame*Nf,1);      % Each row in Fts represents the frame-varying freq values of each partial
for i = 1:NperFrame
    fsyn(i:NperFrame:end) = f;
end

startphase = 0;
for i = 1:Nf
    p(i) = startphase -2*pi*((i-1)*dt)*f(i);
    startphase = startphase +2*pi*dt*f(i);
end
psyn = zeros(NperFrame*Nf,1);      % Each row in Fts represents the frame-varying freq values of each partial
for i = 1:NperFrame
    psyn(i:NperFrame:end) = p;
end

t = [0:1/Fs:(dt*Nf)-(1/Fs)]';
sig = asyn.*sin(2*pi*fsyn.*t + psyn);
%eof