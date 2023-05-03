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
  xzoomfactor = 1;
  yzoomfactor = 1;
  if TransLen > 64
        yzoomfactor = floor(TransLen/64);
	for k=1:64,
	    dummy(k,:) = data_in((k-1)*yzoomfactor+1,:);
        end;
  end;
  if DispLen > 50,
	xzoomfactor = floor(DispLen/50);
        for k = 1:50,
	    disp_data(:,k) = dummy(:,(k-1)*xzoomfactor+1);
        end;
  end;   
  %xdisp = [0:dt*xzoomfactor:49*dt*xzoomfactor]';
  xdisp = [msec_offset:dt*xzoomfactor:msec_offset+49*dt*xzoomfactor]';
  ydisp = [0:df*yzoomfactor:63*df*yzoomfactor]';
  %str1 = 'Size of File: ';
  %cstr = sprintf('%d',cnt);
  %modedit1 = uicontrol('Style','edit','String',[str1 cstr],...
  %	   	    'BackGroundColor','white','Position', ...
  %		    [0 20 120 14]);
  %startstr = sprintf('%d',0);
  %endstr = sprintf('%d',cnt);
  %hsstring = 'From ';
  %hestring = 'To ';
  %hstart =uicontrol('Style','edit','position',...
  %	  [150 20 50 14],'string',[hsstring startstr]);
  %hend =uicontrol('Style','edit','position',...
  %	  [220 20 50 14],'string',[hestring endstr]);
  hold off;
  contour(xdisp,ydisp,disp_data);
  hold on;
  %set(gca,'color',[1 1 0.8]);
  %ylim = max(abs(min(data_in)),abs(max(data_in)));
  %axis([0 cnt -1.2*ylim 1.2*ylim]);
  %set(gca,'xticklabels' ,' '); 
  %set(gca,'yticklabels' ,' ','ytick',0,'ygrid','on','ycolor',...
  %  [0.5 0.5 0]);  
  file_named = 1;
end; %if