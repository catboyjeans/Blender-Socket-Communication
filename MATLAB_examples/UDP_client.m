%MATLAB R2020a higher versions use the udpExplorer which is more convenient 
%UDP client byte testing 


ADDRESS='127.0.0.1';
PORT=50007;
u=udp(ADDRESS,PORT);  
fopen(u);   %connect interface to the host port aka connect socket 

u           %print status

%Write Data
%data=typecast(2,'double');
data=NaN;
fwrite(u,data,'double')


fclose(u); %close connection (caution with this one, might cause access trouble if omitted)