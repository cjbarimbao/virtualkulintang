cam = webcam;

for i = 1:150

I = snapshot(cam);
%figure(3); imshow(I);
I = double(fliplr(I)); %I is the image of the region of interest
R = I(:,:,1); G = I(:,:,2); B = I(:,:,3);
Int= R + G + B;
Int(find(Int==0))=100000; %to prevent NaNs
r = R./ Int; g = G./Int;
SIZE = size(I);
Y=backproj(r,g,hist,SIZE);
figure(5); imagesc(Y);drawnow;

end; 

clear cam;
close all;