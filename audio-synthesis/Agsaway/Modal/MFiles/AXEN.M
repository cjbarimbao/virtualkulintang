function n = Axen(MU,x,y);
axis('image')
mm = max(abs(MU));
MU1 = ((256*abs(MU)/mm)-256)*(-1);
image(x,y,abs(MU1));
colormap(gray(256));
axis('xy');
set(gca,'ylabel',text(0,0,'frequency-axis'));
set(gca,'xlabel',text(0, 0, 'time-axis'));
