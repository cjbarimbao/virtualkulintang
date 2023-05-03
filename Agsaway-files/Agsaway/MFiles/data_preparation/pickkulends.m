function pickkulends(wavfile, npeaks, mindist, thold)
% PICKKULENDS(WAVFILE,NPEAKS,MINDIST,THOLD)
%   determines the starting and ending edges of kulintang signals
%
%   WAVFILE is the filename of the wavfile with 44100Hz sampling rate
%   NPEAKS is the number of peaks (kulintang signals)
%   MINDIST is the minimum distance between peaks
%   THOLD is the noise threshold expressed as attenuation in dB from the peak value of a signal
%   
%   output is a TRS File saved with the same filename as wavfile
%
%   Note: uses the 'pickpeak.m' code by A.Swami  copyrighted by United Signals & Systems, Inc. and The Mathworks, Inc. 
%
%   Frank Agsaway
%   UP DSP Lab, June 2004


if nargin<4
    thold=40;
    mindist=50;
elseif nargin<3
    mindist=50;
end

framelength_t=10;   %10ms window
nonoverlap_t=5;     %5ms shift

% lines '27 to 98', and '152 to 194' adapted from 'gaussianVAD.m' implemented by Shelley Tantan of UP DSP Lab

%------------
%Data Format
%------------
%Initializations
%
%Determine Overlap in Samples
framelength = floor(44100*framelength_t/1000);				
nonoverlap = floor(44100*nonoverlap_t/1000);					
overlap = framelength - nonoverlap;

%Determine Number of Blocks
block_length = 920000;
siz=wavread(wavfile,'size');
siglength=siz(1);
block_no = floor(siglength/block_length);


%--------------------
%Energy Computations
%--------------------

%Initialize Samples from Previous Block Needed for Current Block
pastsignals = zeros(overlap,block_no);

%Energy Computations By Block
%There are block_no+1 blocks in all.
%Last block contains less than 920000 samples.
%Energy output is (block_no)by(920000) array.

for n = 1:(block_no+1)									
   disp(sprintf('Working on block %d', n));
   if n ~= (block_no + 1)
      %for block 1 to the second-to-the-last block
      if n == 1
         sig = wavread(wavfile, [1 920000]);
      else
         sig = wavread(wavfile, [((n-1)*block_length)+1 n*block_length]);
      end
      %Solve for energy using current block samples with past block samples
      sig_frames = buffer(sig,framelength,overlap);
      sig_frames(1:overlap,1) = pastsignals(:,n);
		energy(:,n) = sum(sig_frames.^2,1)';
   else
      %for the last block
      sig = wavread(wavfile, [((n-1)*block_length)+1 siglength]);
      %Solve for energy using current block samples with past block samples
      sig_frames = buffer(sig,framelength,overlap);
      sig_frames(1:overlap,1) = pastsignals(:,n);
      en = sum(buffer((sig.^2),framelength,overlap),1);
      %since last block is less than 920000 samples
      adzeros = length(energy)-length(en);
      energy(:,n) = [en zeros(1,adzeros)]';
   end
   %Save samples to be used for the next block computations
   pastsignals(:,n+1) = sig(end-(overlap-1):end);
end

%clear memory
clear en;
clear sig;
clear sig_frames;
clear pastsignals;

%Arrange Energy Array
energy = reshape(energy, size(energy,1)*size(energy,2), 1);
energy = energy(1:(length(energy) - adzeros));

%Maximum Value of Energy
gmax = max(energy);

%Normalize Signal Energy
gtilde = reshape((energy/gmax), size(energy,1)*size(energy,2),1);

%Change to logarithmic scale
gtildelog=10*log10(gtilde);

% Find starting and ending times of signals
[loc0,val0]=pickpeak(gtildelog,npeaks,mindist);     % determine locations and values of peaks
[loc,i]=sort(loc0);
val=val0(i);

for i=1:npeaks
    startthold=30;  % set noise threshold at starting edge to -30dB
    endthold=thold; % set noise threshold st ending edge to the specified threshold value
    s(i)=loc(i);
    e(i)=loc(i);
    
    while(gtildelog(s(i))>val(i)-startthold)
        
        if i==1
            if s(i)==1
                [startthold,s(i)]=changethold(startthold,i,'starting',s(i),loc);
            end
        end
        
        if i>1
            if s(i)==loc(i-1)
                [startthold,s(i)]=changethold(startthold,i,'starting',s(i),loc);
            end
        end
        
        s(i)=s(i)-1;
    end
         
    
    while(gtildelog(e(i))>val(i)-endthold)
        
        if i<npeaks
            if e(i)==loc(i+1)
                [endthold,e(i)]=changethold(endthold,i,'ending',e(i),loc);
            end
        end
        
        if i==npeaks
            if e(i)==length(gtildelog)
                 [endthold,e(i)]=changethold(endthold,i,'ending',e(i),loc);
            end
        end  
        
        e(i)=e(i)+1;
        
    end
end
%---

%-------
%Output
%-------
%Determine start times and end times, in seconds
start_times = (s-1)*nonoverlap/44100;
end_times = (e-1)*nonoverlap/44100;

trsfile = strcat(wavfile,'.trs');
 
[fout,message] = fopen(trsfile, 'wt');
if fout<0
   fprintf('Error creating output file : %s\n', message);
   return
end

disp('Please wait... Generating the transcription file\n');

%header strings in a .TRS file
fprintf(fout, '<?xml version="1.0"?>\n');
fprintf(fout, '<!DOCTYPE Trans SYSTEM "trans-13.dtd">\n');
fprintf(fout, '<Trans scribe="dummy" audio_filename="00__0001" version="1" version_date="010103">\n');
fprintf(fout, '<Episode>\n');
fprintf(fout, '<Section type="report" startTime="0" endTime="%6.3f">\n', siglength);
fprintf(fout, '<Turn startTime="0" endTime="%6.3f">\n', siglength);
fprintf(fout, '<Sync time="0.000"/>\n');

%print starts and ends in the file
for k = 1:length(start_times)
   fprintf(fout, '..\n');
   fprintf(fout, '<Sync time="%4.3f"/>\n', start_times(k));
   fprintf(fout, 'S\n');
   fprintf(fout, '<Sync time="%4.3f"/>\n', end_times(k));
end

%footer strings in a .TRS file
fprintf(fout, '..\n');
fprintf(fout, '</Turn>\n');
fprintf(fout, '</Section>\n');
fprintf(fout, '</Episode>\n');
fprintf(fout, '</Trans>');

fclose(fout);
disp(sprintf('%s generated', trsfile));


%---
function [newthold,ind]=changethold(thold,peaknum,str,ind,loc)
newthold=thold-1;
ind=loc(peaknum);
fprintf('%s point threshold of "signal %d" changed to "%ddB" \n',str,peaknum,newthold);