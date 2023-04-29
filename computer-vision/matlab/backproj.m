function Y = backproj(mr, mg, rs, SIZE)

% function Y = BACKPROJ(mr, mg, rs, SIZE) returns the histogram backprojection
% using histogram rs, chromaticities mr and mg and image size SIZE.
% mr and mg must be calculated using getNCC.m.
BINS = 16;
sizze=SIZE(1)*SIZE(2);
mmrr=round(reshape(mr,sizze,1)*(BINS-1));  %% 32 bin size
mmgg=round(reshape(mg,sizze,1)*(BINS-1));  
  
rss=reshape(rs,BINS*BINS,1);  
Y=rss(mmgg*BINS+mmrr+1);  
Y=reshape(Y,SIZE(1),SIZE(2));