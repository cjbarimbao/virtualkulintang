[fname,pthname] = uigetfile('*.bin','Data File',0,0); 
if (fname ~= zeros(size(fname))),
  fidr = fopen([pthname fname],'rb');
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
  data_max = max(data_in);
  data_in = reshape(data_in,TransLen,DispLen);
  xdisp = [msec_offset:dt:msec_offset+(DispLen-1)*dt]';
  ydisp = [0:df:(TransLen-1)*df]';
  hold off;
  colormap gray;
  image(xdisp,ydisp,data_in);
  axis('xy');
  hold on;
  file_named = 1;
end; %if