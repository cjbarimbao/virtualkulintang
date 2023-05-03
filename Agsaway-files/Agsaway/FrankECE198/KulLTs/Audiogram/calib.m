%calibration
fs=44100;
t=[0:1/44100:0.075-1/44100];


amplitude=[0.0002:-0.000001:0.000002]';





for n=1:length(amplitude)
   tones=amplitude(n)*sin(2*pi*3360*t);
   sound(tones,fs)
   fprintf('amplitude level is %d\n\n\n',amplitude(n))
   fprintf(1,'Hit Enter to hear the next amplitude\n\n\n\n\n\n\n\n\n\n\n')
   pause
   
end