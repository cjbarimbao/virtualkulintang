modzlabel = 'Magnitude, dB';
logrange = sscanf(get(log_range,'string'),'%f');
if logrange == [],
	log_error = errordlg('Must input dB range first','DISPLAY ERROR');
else
%data_max = max(max(data_plot));
db_min = data_max*(10^(-logrange/10));
dummy = data_plot > db_min*ones((fend-fstart+1),(tend-tstart+1));
data_plot = db_min*(~dummy) + data_plot.*dummy; 
clear dummy;
data_plot = 10*log10(data_plot/db_min);
log_displayed = 1;
end;