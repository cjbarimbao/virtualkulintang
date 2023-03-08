#include "KulintangClass.h"
//#include "KulintangAgsaway.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>


//------------------KULINTANG GONG-------------------------

KulintangGong::KulintangGong()
{	
	TWOPI = 6.283185f;
	FS = 44100;
	Nf = n = NperFrame = siglen = 0;
	dt = 0.f;
//	*amp = *freq = *sig = 0.f;
}

KulintangGong::KulintangGong(int preset, int a)
{
	setFS(a);
	TWOPI = 6.283185f;

	switch(preset)
	{
		case 1:		//parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
			kulintangAgsaway1();
			break;
		case 2:		//parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
			kulintangAgsaway2();
			break;
		case 3:		//parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
			kulintangAgsaway3();
			break;
		case 4:		//parameters from file kulintang1_04_beed_est.txt  after removing 60Hz Hum fundamental and harmonics
			kulintangAgsaway4();
			break;
		case 5:		//parameters from file kulintang1_05_beed_est.txt  after removing 60Hz Hum fundamental and harmonics
			kulintangAgsaway5();
			break;
		case 6:		//parameters from file kulintang1_06_beed_est.txt  after removing 60Hz Hum fundamental and harmonics
			kulintangAgsaway6();
			break;
		case 7:		//parameters from file kulintang1_07_beed_est.txt  after removing 60Hz Hum fundamental and harmonics
			kulintangAgsaway7();
			break;
		case 8:		//parameters from file kulintang1_08_beed_est.txt  after removing 60Hz Hum fundamental and harmonics
			kulintangAgsaway8();
			break;
		case 9:	// parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR1 gong 1.txt'
			kulintangDMR1_1();
			break;
		case 10:	// parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR1 gong 2.txt'
			kulintangDMR1_2();
			break;
		case 11:	// parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR1 gong 3.txt'
			kulintangDMR1_3();
			break;
		case 12:	// parameters from file kulintang1_04_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR1 gong 4.txt'
			kulintangDMR1_4();
			break;
		case 13:	// parameters from file kulintang1_05_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR1 gong 5.txt'
			kulintangDMR1_5();
			break;
		case 14:	// parameters from file kulintang1_06_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR1 gong 6.txt'
			kulintangDMR1_6();
			break;
		case 15:	// parameters from file kulintang1_07_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR1 gong 7.txt'
			kulintangDMR1_7();
			break;
		case 16:	// parameters from file kulintang1_08_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR1 gong 8.txt'
			kulintangDMR1_8();
			break;
		case 17:	// parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Santos gong 1.txt'
			kulintangSantos1();
			break;
		case 18:	// parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Santos gong 2.txt'
			kulintangSantos2();
			break;
		case 19:	// parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Santos gong 3.txt'
			kulintangSantos3();
			break;
		case 20:	// parameters from file kulintang1_04_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Santos gong 4.txt'
			kulintangSantos4();
			break;
		case 21:	// parameters from file kulintang1_05_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Santos gong 5.txt'
			kulintangSantos5();
			break;
		case 22:	// parameters from file kulintang1_06_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Santos gong 6.txt'
			kulintangSantos6();
			break;
		case 23:	// parameters from file kulintang1_07_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Santos gong 7.txt'
			kulintangSantos7();
			break;
		case 24:	// parameters from file kulintang1_08_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Santos gong 8.txt'
			kulintangSantos8();
			break;
		case 25:	// parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR2 gong 1.txt'
			kulintangDMR2_1();
			break;
		case 26:	// parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR2 gong 2.txt'
			kulintangDMR2_2();
			break;
		case 27:	// parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR2 gong 3.txt'
			kulintangDMR2_3();
			break;
		case 28:	// parameters from file kulintang1_04_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR2 gong 4.txt'
			kulintangDMR2_4();
			break;
		case 29:	// parameters from file kulintang1_05_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR2 gong 5.txt'
			kulintangDMR2_5();
			break;
		case 30:	// parameters from file kulintang1_06_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR2 gong 6.txt'
			kulintangDMR2_6();
			break;
		case 31:	// parameters from file kulintang1_07_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR2 gong 7.txt'
			kulintangDMR2_7();
			break;
		case 32:	// parameters from file kulintang1_08_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR2 gong 8.txt'
			kulintangDMR2_8();
			break;
		case 33:	// parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Dioquino gong 1.txt'
			kulintangDioquino1();
			break;
		case 34:	// parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Dioquino gong 2.txt'
			kulintangDioquino2();
			break;
		case 35:	// parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Dioquino gong 3.txt'
			kulintangDioquino3();
			break;
		case 36:	// parameters from file kulintang1_04_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Dioquino gong 4.txt'
			kulintangDioquino4();
			break;
		case 37:	// parameters from file kulintang1_05_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Dioquino gong 5.txt'
			kulintangDioquino5();
			break;
		case 38:	// parameters from file kulintang1_06_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Dioquino gong 6.txt'
			kulintangDioquino6();
			break;
		case 39:	// parameters from file kulintang1_07_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Dioquino gong 1.txt'
			kulintangDioquino7();
			break;
		case 40:	// parameters from file kulintang1_08_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Dioquino gong 8.txt'
			kulintangDioquino8();
			break;
		case 41:	// parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR3 gong 1.txt'
			kulintangDMR3_1();
			break;
		case 42:	// parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR3 gong 2.txt'
			kulintangDMR3_2();
			break;
		case 43:	// parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR3 gong 3.txt'
			kulintangDMR3_3();
			break;
		case 44:	// parameters from file kulintang1_04_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR3 gong 4.txt'
			kulintangDMR3_4();
			break;
		case 45:	// parameters from file kulintang1_05_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR3 gong 5.txt'
			kulintangDMR3_5();
			break;
		case 46:	// parameters from file kulintang1_06_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR3 gong 6.txt'
			kulintangDMR3_6();
			break;
		case 47:	// parameters from file kulintang1_07_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR3 gong 7.txt'
			kulintangDMR3_7();
			break;
		case 48:	// parameters from file kulintang1_08_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR3 gong 8.txt'
			kulintangDMR3_8();
			break;
		case 49:	// parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR4 gong 1.txt'
			kulintangDMR4_1();
			break;
		case 50:	// parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR4 gong 2.txt'
			kulintangDMR4_2();
			break;
		case 51:	// parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR4 gong 3.txt'
			kulintangDMR4_3();
			break;
		case 52:	// parameters from file kulintang1_04_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR4 gong 4.txt'
			kulintangDMR4_4();
			break;
		case 53:	// parameters from file kulintang1_05_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR4 gong 5.txt'
			kulintangDMR4_5();
			break;
		case 54:	// parameters from file kulintang1_06_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR4 gong 6.txt'
			kulintangDMR4_6();
			break;
		case 55:	// parameters from file kulintang1_07_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR4 gong 7.txt'
			kulintangDMR4_7();
			break;
		case 56:	// parameters from file kulintang1_08_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR4 gong 8.txt'
			kulintangDMR4_8();
			break;
		case 57:	// parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR5 gong 1.txt'
			kulintangDMR5_1();
			break;
		case 58:	// parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR5 gong 2.txt'
			kulintangDMR5_2();
			break;
		case 59:	// parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR5 gong 3.txt'
			kulintangDMR5_3();
			break;
		case 60:	// parameters from file kulintang1_04_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR5 gong 4.txt'
			kulintangDMR5_4();
			break;
		case 61:	// parameters from file kulintang1_05_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR5 gong 5.txt'
			kulintangDMR5_5();
			break;
		case 62:	// parameters from file kulintang1_06_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR5 gong 6.txt'
			kulintangDMR5_6();
			break;
		case 63:	// parameters from file kulintang1_07_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR5 gong 7.txt'
			kulintangDMR5_7();
			break;
		case 64:	// parameters from file kulintang1_08_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR5 gong 8.txt'
			kulintangDMR5_8();
			break;
		case 65:	// parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR6 gong 1.txt'
			kulintangDMR6_1();
			break;
		case 66:	// parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR6 gong 2.txt'
			kulintangDMR6_2();
			break;
		case 67:	// parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR6 gong 3.txt'
			kulintangDMR6_3();
			break;
		case 68:	// parameters from file kulintang1_04_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR6 gong 4.txt'
			kulintangDMR6_4();
			break;
		case 69:	// parameters from file kulintang1_05_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR6 gong 5.txt'
			kulintangDMR6_5();
			break;
		case 70:	// parameters from file kulintang1_06_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR6 gong 6.txt'
			kulintangDMR6_6();
			break;
		case 71:	// parameters from file kulintang1_07_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR6 gong 7.txt'
			kulintangDMR6_7();
			break;
		case 72:	// parameters from file kulintang1_08_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'DMR6 gong 8.txt'
			kulintangDMR6_8();
			break;
		case 73:	// parameters from file kulintang1_01_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Laureola gong 1.txt'
			kulintangLaureola1();
			break;
		case 74:	// parameters from file kulintang1_02_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Laureola gong 2.txt'
			kulintangLaureola2();
			break;
		case 75:	// parameters from file kulintang1_03_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Laureola gong 3.txt'
			kulintangLaureola3();
			break;
		case 76:	// parameters from file kulintang1_04_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Laureola gong 4.txt'
			kulintangLaureola4();
			break;
		case 77:	// parameters from file kulintang1_05_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Laureola gong 5.txt'
			kulintangLaureola5();
			break;
		case 78:	// parameters from file kulintang1_06_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Laureola gong 6.txt'
			kulintangLaureola6();
			break;
		case 79:	// parameters from file kulintang1_07_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Laureola gong 7.txt'
			kulintangLaureola7();
			break;
		case 80:	// parameters from file kulintang1_08_beed_est.txt after removing 60Hz Hum fundamental and harmonics
				// from 'Laureola gong 8.txt'
			kulintangLaureola8();
			break;
	}

	// synthesize Gongs
	
}

KulintangGong::~KulintangGong(){
	// cleanup
//	delete [] sig, amp, freq;
}

void KulintangGong::setFS(int a)
{
	FS = a;
}

void KulintangGong::synth_gong()
{
	int parnum, frame, offset, pt;
	float a2, kul, inc, par;

	sig = new float [siglen];
	float * pprev = new float [n];
	float * a1 = new float [n];
	float * da = new float [n];
	float * p = new float [n];
	
	for(parnum=0; parnum<n; parnum++)								// set previous phase to zero
        pprev[parnum] = 0;
    
    for (frame=0; frame<Nf; frame++)									// do for each frame
    {
        for (parnum=0; parnum<n; parnum++)							// do for each partial
        {
            a1[parnum] = amp[Nf*parnum + frame];				// initial frame amplitude
            a2 = amp[Nf*parnum + 1 + frame];					// final frame amplitude
            if (frame==Nf-1){										// last interpolation point = 0
               a2 = 0;
			}

			da[parnum] = (a2 - a1[parnum])/NperFrame;				// amplitude increment
			//f[parnum] = paramc[Nf*parnum + frame];					// frequency estimates
			p[parnum] = pprev[parnum] - frame*TWOPI*freq[Nf*parnum + frame]*dt;	// current phase
			pprev[parnum] = pprev[parnum] + TWOPI*freq[Nf*parnum + frame]*dt;		// previous phase
        }
		
        offset = frame*NperFrame;                                 // number of time samples before current frame
        
        for (pt=0; pt<NperFrame; pt++)                            // do for each time point
        {   
            kul = 0;                                              // start at zero
            for(parnum=0; parnum<n; parnum++)                     // do for each partial
            {
				inc = pt*da[parnum];																						// amplitude increment for each point
				par = (a1[parnum]+inc)*sin(TWOPI*freq[Nf*parnum + frame]*((float(offset + pt))/float(FS)) + p[parnum]);		// partial value
				kul = kul + par;																// add current partial value to synthesized signal value
            }   
            sig[offset+pt]=kul;                                   // append current synth sig value
        }//for 
	}//for
}

//------------------------- KULINTANG CLASS -------------------------

KulintangClass::KulintangClass()
{
	// default settings
	GongNum = 1;
	preset = 1;
	setFS(44100);
	changePreset(0);
	strncpy_s(name, "None Loaded", 11*sizeof(char));
}

KulintangClass::~KulintangClass(){}

void KulintangClass::setFS(int a)
{
	FS = a;
}

void KulintangClass::changePreset(int preset){	
	
	switch(preset)
	{
		case 0:				// Default, Agsaway Gongs
		{	
			strncpy_s(name, "Agsaway Gongs", 13*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 1;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
			break;
		case 1:				// DMR1 Tuning
		{
			strncpy_s(name, "DMR1", 4*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 9;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
			break;
		case 2:				// Santos Tunings
		{
			strncpy_s(name, "Santos", 6*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 17;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
		case 3:				// DMR2 Tunings
		{
			strncpy_s(name, "DMR2", 4*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 25;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
			break;
		case 4:				// Dioquino Tunings
		{
			strncpy_s(name, "Dioquino", 8*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 33;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
			break;
		case 5:				// DMR3 Tunings
		{
			strncpy_s(name, "DMR3", 4*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 41;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
			break;
		case 6:				// DMR4 Tunings
		{
			strncpy_s(name, "DMR4", 4*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 49;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
			break;
		case 7:				// DMR5 Tunings
		{
			strncpy_s(name, "DMR5", 4*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 57;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
			break;
		case 8:				// DMR6 Tunings
		{
			strncpy_s(name, "DMR6", 4*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 65;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
			break;
		case 9:				// Laureola Tunings
		{
			strncpy_s(name, "Laureola", 8*sizeof(char));
			preset = 1;
			GongNum = 8;
			gongs = new KulintangGong[GongNum];
		
			int offset = 73;
			for(int i = 0; i <= GongNum-1; i++)
			{		
				KulintangGong gongi (i+offset, FS);
				*(gongs+i) = gongi;
			}
		}
			break;
	}

	synthAll();
}

KulintangGong KulintangClass::returnGong(int gongnum)
{
	return gongs[gongnum];
}

int KulintangClass::returnWavelen(int gongnum)
{
	KulintangGong temp;
	temp = returnGong(gongnum);
	return temp.siglen;
}

void KulintangClass::initWavelen()
{
	wavelen = new int [GongNum];
	for(int i = 0; i < GongNum; i++)
		*(wavelen+i) = returnWavelen(i);
}

void KulintangClass::synthAll(){
	for(int i = 0; i < GongNum; i++)
		(gongs+i)->synth_gong();
}

float * KulintangClass::returnGongSig(int gongnum)
{
	return (gongs+gongnum)->sig;
}