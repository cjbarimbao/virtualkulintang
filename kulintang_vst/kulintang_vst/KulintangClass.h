//#include "KulintangAgsaway.h"

#ifndef __KulintangClass__
#define __KulintangClass__

enum
{
	poly = 2 // set polyphony
};

class KulintangGong
{
	float TWOPI;
	int FS;

	// Pareset calling subfunctions
	//// Agsaway Preset
	void kulintangAgsaway1();
	void kulintangAgsaway2();
	void kulintangAgsaway3();
	void kulintangAgsaway4();
	void kulintangAgsaway5();
	void kulintangAgsaway6();
	void kulintangAgsaway7();
	void kulintangAgsaway8();
	//////DMR1 Preset
	//void kulintangDMR1_1();
	//void kulintangDMR1_2();
	//void kulintangDMR1_3();
	//void kulintangDMR1_4();
	//void kulintangDMR1_5();
	//void kulintangDMR1_6();
	//void kulintangDMR1_7();
	//void kulintangDMR1_8();
	//////Santos Preset
	//void kulintangSantos1();
	//void kulintangSantos2();
	//void kulintangSantos3();
	//void kulintangSantos4();
	//void kulintangSantos5();
	//void kulintangSantos6();
	//void kulintangSantos7();
	//void kulintangSantos8();
	////// DMR2 Preset
	//void kulintangDMR2_1();
	//void kulintangDMR2_2();
	//void kulintangDMR2_3();
	//void kulintangDMR2_4();
	//void kulintangDMR2_5();
	//void kulintangDMR2_6();
	//void kulintangDMR2_7();
	//void kulintangDMR2_8();
	////// Dioquino Preset
	//void kulintangDioquino1();
	//void kulintangDioquino2();
	//void kulintangDioquino3();
	//void kulintangDioquino4();
	//void kulintangDioquino5();
	//void kulintangDioquino6();
	//void kulintangDioquino7();
	//void kulintangDioquino8();
	////// DMR3 Preset
	//void kulintangDMR3_1();
	//void kulintangDMR3_2();
	//void kulintangDMR3_3();
	//void kulintangDMR3_4();
	//void kulintangDMR3_5();
	//void kulintangDMR3_6();
	//void kulintangDMR3_7();
	//void kulintangDMR3_8();
	////// DMR4 Preset
	//void kulintangDMR4_1();
	//void kulintangDMR4_2();
	//void kulintangDMR4_3();
	//void kulintangDMR4_4();
	//void kulintangDMR4_5();
	//void kulintangDMR4_6();
	//void kulintangDMR4_7();
	//void kulintangDMR4_8();
	////// DMR5 Preset
	//void kulintangDMR5_1();
	//void kulintangDMR5_2();
	//void kulintangDMR5_3();
	//void kulintangDMR5_4();
	//void kulintangDMR5_5();
	//void kulintangDMR5_6();
	//void kulintangDMR5_7();
	//void kulintangDMR5_8();
	////// DMR6 Preset
	//void kulintangDMR6_1();
	//void kulintangDMR6_2();
	//void kulintangDMR6_3();
	//void kulintangDMR6_4();
	//void kulintangDMR6_5();
	//void kulintangDMR6_6();
	//void kulintangDMR6_7();
	//void kulintangDMR6_8();
	////// Laureola Preset
	//void kulintangLaureola1();
	//void kulintangLaureola2();
	//void kulintangLaureola3();
	//void kulintangLaureola4();
	//void kulintangLaureola5();
	//void kulintangLaureola6();
	//void kulintangLaureola7();
	//void kulintangLaureola8();

public:
	KulintangGong();
	KulintangGong(int preset, int a);
	~KulintangGong();

	int Nf;								// number of frames
	int n;								// number of partials
	int NperFrame;
	int siglen;
	float dt;							// time interval per frame
	float* amp;						// partial amplitudes
	float* freq;						// partial frequencies
	float* sig;						// synthesized gong waveform	

	void setFS(int a);
	void synth_gong();
};

class KulintangClass
{
	int FS;					// sampling frequency
	int GongNum;			// number of gongs
	int preset;				// preset number
	int* wavelen;			// array containing the different signal lengths (in samples) of each gong

public:
	char name[24];			// name of Kulintang Set represented by the Class
	KulintangClass();
	~KulintangClass();
	KulintangGong* gongs;

	KulintangGong returnGong(int gongnum);	// function for returning a gong
	float* returnGongSig(int gongnum);		// function for returning the gong waveform of a gong
	int returnWavelen(int gongnum);			// function for returning the signal length of a gong
	void synthAll();						// function for synthesizing the waveforms of all the gongs in the set
	void initWavelen();						// function for initializing *wavelen
	void changePreset(int preset);			// function to change kulintang preset
	void setFS(int a);
};

#endif