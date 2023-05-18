function endpts=trsread(trsfile)
% endpts=TRSREAD(trsfile)
%
%   Determines the starting points and endpoints of signals 
%   from a TRS file
%
%   input is a TRS file, output is 'endpoints' matrix
%   left column consists of the starting point sample numbers
%   right column consists of ending point sample numbers
%
%   Frank Agsaway
%   UP DSP Lab, June 2004
%
% revised Dec 2004


% import TRS file
if strcmp(trsfile(end-3:end),'.trs')==0 
    trsfile=[trsfile '.trs'];
end
trs=textread(trsfile,'%s');

% determine start and end sample numbers of signals
% i=strmatch('time="0.000"/>',trs);
% starttimes_str=trs(i+3:6:end-8);
% endtimes_str=trs(i+6:6:end-5);
s = strmatch('S', trs, 'exact');
starttimes_str = trs(s-1);
endtimes_str = trs(s+2);
endpts= floor(44100*[findnum(starttimes_str) findnum(endtimes_str)]);

%---
function n=findnum(v);
% determines the numeric data from the string:'time="0.000"/>'
n=[];
for i=1:length(v)
    str=char(v(i));
    loc=findstr('"',str);
    n=[n;str2num(str(loc(1)+1:loc(2)-1))];
end 
