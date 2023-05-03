% An audiogram is used to determine the minimum volume that each ear could 
% detect; i.e., the stimulus threshold. In the followin program, a 
% 2-down-1-up procedure [Levitt, 1971] is used and  implemented as a cued 
% 2IFC test. The 2-down-1-up procedure is an adaptive staircase method 
% for estimating thresholds. The stimulus is a 1-second tone which can be 
% presented in either of two intervals with equal probability, the other 
% interval was blank.  The task of the subject is to choose the interval 
% in which the tone was presented. At the beginning of the test for each 
% stimulation frequency, the volume level of the tone is high. The volume 
% level is decreased after the subject made 2 successive correct responses 
% and is increased after the subject made a wrong response. A reversal is 
% defined as the change in the correctness of the subject’s response; 
% i.e., from being correct to being wrong and vice versa. The step-size is 
% decreased every two consecutive reversals. The stopping criterion is 10 
% reversals and the stimulus threshold is defined as the average of the 
% last eight reversals. This is done for the following frequencies: 250, 
% 500, 1000, 2000, 4000, 8000 Hz. 

% In an audiogram, the lower the score the more sensitive the ear is to the 
% frequency that is being tested. Typical scores for normal hearing is around
% 20-30 dBSPL for the 250 Hz tone, less than 10 dBSPL for the 500, 1000, 
% and 2000 Hz tones and around 15 dBSPL for the 8000 Hz. These numbers 
% are based on audiogram scores of subjects participating in other 
% psychophysical listening experiments. 

% During an experiment the subjects could take a break any time and 
% should be instructed to do so frequently to avoid fatigue and boredom. 
% They should not work more than two hours in each session.

% IMPORTANT: the settings for variables marked MCU may be changed by the user

% THE EXPERIMENTER SHOULD SET THE FOLLOWING BEFORE USING THIS PROGRAM

% volume_inaudible should be set accordingly since soundcards vary in 
% terms of absolute volume in dBSPL. A way to set this variable is to
% ask a very soft spoken person (they usually have the keenest hearing capability
% then, in MatLab, create a tone and vary the volume (using sound(tone*volume,fs)
% until the soft spoken person cannot hear it anymore. Set volume_inaudible 
% to this volume/10. MAKE SURE THAT THE SETTING OF THE VOLUME OF THE COMPUTER
% IS AT MAXIMUM WHILE DOING THIS CALIBRATION.
% 
% The volume step is currently set at 5 dB. If the listeners get easily bored
% then increase the volume step.

% RESULTS WILL BE IN SUBJECT's NAME .txt
% USE WORDPAD to VIEW THE RESULTS

% author: Rowena Cristina L. Guevara, Ph.D.
% Sept. 22, 2001

% all entries marked (MCU) may be changed by user

clear;close all;
fs=44100; % Hz; sampling rate (MCU)	
time = [0:1/fs:1]'; % tone duration is 1 sec (MCU)
ender = 10; % number of reversals to end process  

%these are the frequencies that will be tested (MCU)

sine_freq = [250;500;1000;2000;4000;8000]; % Hz														 
no_tone = zeros(length(time),1); % tone is absent 

interstimulus_interval = 100; % msec - this is the time between
										% two presentation intervals
                              
% interstimulus signal                              
intervaltone = zeros(round(fs*interstimulus_interval/1000),1);
                              

for k=1:length(sine_freq), % create the sinusoids
   sine_tones(:,k)=sin(2*pi*sine_freq(k)*time);
end;

volume_step_dB = 5; %dB; the increment in volume change (MCU)

volume_step = 10.^(volume_step_dB/20); % linearize the volume change

% volume_inaudible = 0.0000027;
volume_inaudible = 0.0000029;
initial_volume = 31623*volume_inaudible; % this is the initial volume - the loudest possible (MCU)
% the volume_inaudible should be set to a value such that soundsc(sine_tones*volume_inaudible,fs) cannot be 
% heard anymore; the 31623 multiplier is to move this initial volume up by 90 dB

	


% now, draw the GUI
global b1 b2 % declare these variables as global

load audiofigure_
main_fig = figure('Color',[0.8 0.8 0.8], ...
	'Colormap',mat0, ...
	'FileName','C:\FrankECE198\audiogram\audiofigure.m', ...
	'PaperPosition',[18 180 576 432], ...
	'PaperUnits','points', ...
	'Position',[200 129 560 420], ...
	'Tag','Fig1', ...
   'ToolBar','none');


button1 = uicontrol('Parent',main_fig, ...
	'Units','points', ...
	'BackgroundColor',[1 0.501960784313725 0.250980392156863], ...
	'FontName','arial', ...
	'FontSize',16, ...
	'ListboxTop',0, ...
	'Position',[42.75 51.75 137.25 50.25], ...
   'String','Interval 1', ...
   'callback','button1press',...
   'Tag','Pushbutton1');

button2= uicontrol('Parent',main_fig, ...
	'Units','points', ...
	'BackgroundColor',[0 0.501960784313725 0], ...
	'FontName','arial', ...
	'FontSize',16, ...
	'ListboxTop',0, ...
	'Position',[242.25 52.125 135.75 49.5], ...
   'String','Interval 2', ...
   'callback','button2press',...
   'Tag','Pushbutton2');


routine_name = uicontrol('Parent',main_fig, ...
	'Units','points', ...
	'BackgroundColor',[0.803921568627451 0.803921568627451 0.803921568627451], ...
	'FontName','arial', ...
	'FontSize',18, ...
	'ListboxTop',0, ...
	'Position',[131.25 235.5 153.75 43.5], ...
	'String','DSP Lab Audiogram', ...
	'Style','text', ...
	'Tag','StaticText1');

interval1 = uicontrol('Parent',main_fig, ...
	'Units','points', ...
	'BackgroundColor',[1 0.501960784313725 0.250980392156863], ...
	'FontName','arial', ...
	'FontSize',16, ...
	'ListboxTop',0, ...
	'Position',[42.75 138.75 138 49.5], ...
	'String','   Playing     Interval 1', ...
	'Style','text', ...
	'Tag','StaticText2', ...
   'Visible','off');

interval2 = uicontrol('Parent',main_fig, ...
	'Units','points', ...
	'BackgroundColor',[0 0.501960784313725 0.250980392156863], ...
	'FontName','arial', ...
	'FontSize',16, ...
	'ListboxTop',0, ...
	'Position',[237 138.75 138.75 49.5], ...
	'String','     Playing      Interval 2', ...
	'Style','text', ...
	'Tag','StaticText3', ...
	'Visible','off');

frequency_tested = uicontrol('Parent',main_fig, ...
	'Units','points', ...
	'BackgroundColor',[0.803921568627451 0.803921568627451 0.803921568627451], ...
	'FontName','arial', ...
	'FontSize',18, ...
	'ListboxTop',0, ...
	'Position',[92 194 250 33.5], ...
	'String','', ...
	'Style','text', ...
	'Tag','StaticText2');

% Let's get the subject's name and set up a file to receive data

prompt = 'Please enter your name';
dlgTitle = 'Subject Name';
subject_name = inputdlg(prompt,dlgTitle)
fname = ['C:\FrankECE198\audiogram\audiogram_results\' char(subject_name) '.txt'];
fid = fopen(fname,'wb');
fprintf(fid,'%s\n','FREQUENCY (Hz)		RIGHT (dB)		LEFT (dB)');

% prompt the user for readiness

buttonname = questdlg('Do you wish to start the experiment?');

if buttonname == 'Yes', % get on with the experiment
   
% MAIN PROGRAM

for freq_num=1:length(sine_freq),
 for ear = 1:2,
   randomizer = rand(1000,1)-0.5; % if the counter runs out, increase 1000
   counter = 0; % initialize counter
   num_error = 0; % initialize erroneous answer count
	num_reversal = 0; % initialize answer reversal count
   num_correct = 0; % initialize correct answer count
   previous_answer = 1; % initialize to 'correct answer'
   current_answer = 1; % initialize to 'correct answer'
   volume = initial_volume;
      
   if ear == 1
      wavsnd = [zeros(length(sine_tones),1) sine_tones(:,freq_num)];
      display_string = [num2str(sine_freq(freq_num)) ' Hz, RIGHT EAR'];
   else
      wavsnd = [sine_tones(:,freq_num) zeros(length(sine_tones),1)];
      display_string = [num2str(sine_freq(freq_num)) ' Hz, LEFT EAR'];
   end;
   set(frequency_tested,'string',display_string);
   while num_reversal < ender,
      set(interval1,'visible','off');
  		set(interval2,'visible','off');  
      counter = counter+1;
      b1=0; % clear the button values
      b2=0;
      if randomizer(counter) < 0, tone_interval = 1;
      elseif randomizer(counter) >= 0, tone_interval = 2;
      end;
      if tone_interval == 1,% play the tone in the first interval
         set(interval1,'visible','on');pause(0.1);
         % disp('tone in Interval 1') % checker
         sound(wavsnd*volume,fs);pause(1);
         set(interval1,'visible','off')
         pause(0.1);
         set(interval2,'visible','on');pause(0.1);
         sound(no_tone,fs);pause(1);
         set(interval2,'visible','off');
      elseif tone_interval == 2, %play the tone in the second interval
         set(interval1,'visible','on');pause(0.1);
         % disp('tone in Interval 2') % checker
         sound(no_tone,fs);pause(1);
         set(interval1,'visible','off')
         pause(0.1);
         set(interval2,'visible','on');pause(0.1);
         sound(wavsnd*volume,fs);pause(1);
         set(interval2,'visible','off')
      end; % if
      uiwait(main_fig); 
      %disp(['button has been pressed  ' num2str([counter b1 b2])]) % checker
      	if ((b1&(tone_interval==1)&~b2) | (~b1&(tone_interval==2)&b2)) 
         	 % Interval 1 was chosen correctly
             % disp('correct choice') % checker         	
            num_correct = num_correct+1;
         	current_answer(counter) = 1; % correct answer
         	if num_correct == 2,
            	volume =volume/volume_step; %decrease volume when response is twice successively correct   
            	num_correct = 0; % reset counter for number of correct responses
         	end; %if num_correct == 2   
      	elseif ((b1&(tone_interval==2)&~b2) | (~b1&(tone_interval==1)&b2)) 
        	 % Subject made incorrect choice
         	% disp('incorrect choice')  % checker
           	volume = volume*volume_step; % increase volume when response is wrong
         	num_correct = num_correct - 1; %takes care of the successive correct count
         	current_answer(counter) = 0; % wrong answer
         end; % ((b1&(sign(randomizer(counter))+ ...
      
         % determine if a reversal (correct answer followed by incorrect
         % answer and vice-versa) occurred
         if counter > 1
      		if current_answer(counter-1) ~= current_answer(counter), % check if current and previous answers are the difference
       			num_reversal = num_reversal + 1; 
                reversal_volume(num_reversal) = volume; 
                % disp(['reversal # ' num2str(num_reversal) ' occurred']) % checker
				% keep track of the volume level at each reversal
            end; % if current_answer
         end; % if counter
         % disp(['volume (' num2str(counter) ') = ' num2str(volume)]); % checker
  	end; %while
min_volume(freq_num,ear) = mean(reversal_volume(3:ender)); % keep track of the final volume   
min_volume_db(freq_num,ear) = 20*log10(min_volume(freq_num,ear)/initial_volume);
if ear == 1,
   display_string = ['Done with ' num2str(sine_freq(freq_num)) ' Hz, RIGHT EAR, Press any key to continue'];
else   
    display_string = ['Done with ' num2str(sine_freq(freq_num)) ' Hz, LEFT EAR, Press any key to continue'];
 end;    
 set(frequency_tested,'FontSize',10);
 set(frequency_tested,'string',display_string);
 pause;
 set(frequency_tested,'FontSize',18);
end; % for ear
fprintf(fid,'%6.0f\t\t\t%6.4f\t\t%6.4f\n',[sine_freq(freq_num) min_volume_db(freq_num,:)]);
end; % for freq_num
end; % MAIN PROGRAM
fclose(fid);