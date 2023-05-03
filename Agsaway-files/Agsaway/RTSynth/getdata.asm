	#include <asm_sprt.h>

	.global _getdata;
	.section/dm ex_data;
	.var param[]="C:\FrankECE198\KulBinDat\agong1_03_beed_est.txt";
	.section/pm seg_pmco;
_getdata:
	entry;
	r0=param;
	b4=param;
	m4=1;
	r4=dm(i4,m4);
	nop;
	nop;
	nop;
	
	exit;
