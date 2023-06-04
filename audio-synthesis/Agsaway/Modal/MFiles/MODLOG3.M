logrange = 60;
db_min = data_max*(10^(-logrange/10));
dummy = fuddy > db_min*ones(size(fuddy));
fuddy = db_min*(~dummy) + fuddy.*dummy; 
clear dummy;
fuddy = 10*log10(fuddy/db_min);
end;