function [p11, pfa, p12, phit, pcmax, dprime, beta] = statsx(n1,n2,n11,n22);
% usage:
%	 [p11, pfa, p12, phit, pcmax, dprime, beta] = stats(n1,n2,n11,n22);
% where:
%
% FOR TWO-INTERVAL FORCED CHOICE
% n1 = number of times that ORIG followed by SYNTH (O-S) was presented
% n2 = number of times that SYNTH followed by ORIG (S-O) was presented
% n11 = number of times O-S was chosen when O-S was presented;
% n22 = number of times S-O was chosen when S-O was presented;
%
% FOR SAME-DIFFERENT EXPERIMENT
% n1 = number of times that "same" was presented
% n2 = number of times that "different" was presented
% n11 = number of times "same" was chosen when "same" was presented;
% n22 = number of times "different" was chosen when "different" was presented;


pfa = (n1 - n11)/n1;
p11 = 1-pfa;
phit = n22/n2;
p12 = 1-phit;

zfa = zscorex(pfa);
zhit = zscorex(phit);
dprime = zfa - zhit;
pcmax = pmax(dprime/2);
beta = 0.5*(zfa.^2-zhit.^2)/log(10);