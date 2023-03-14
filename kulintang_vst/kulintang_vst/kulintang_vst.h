#pragma once
#include "audioeffectx.h"
#include "KulintangClass.h"

//------------------------ENUM PARAMETERS---------------------------------
enum
{
	kNumPrograms = 1,
	kNumParams = 0
};

class kulintang_vst : public AudioEffectX {
public:
	kulintang_vst(audioMasterCallback audioMaster);
	~kulintang_vst();
	  
	//------------- MIDI EVENT HANDLING ------------------------------------------
	virtual VstInt32 processEvents( VstEvents* ev);
	virtual void noteOn(VstInt32 note, VstInt32 velocity, VstInt32 delta);
	virtual void noteOff();
  
  	//------------- KULINTANG OBJECTS AND VARIABLES--------------------------------
    KulintangClass KulintangSet;		// is also the pointer to the Program Container
	float *waveform;
	int wavelen;
	virtual void setProgram( VstInt32 program );
	virtual void getProgramName( char *name );

	//--------------- PROCESS REPLACING -----------------------------------
  	void processReplacing(float **inputs, float **outputs, VstInt32 sampleFrames);

	//---------------Initialization Functions-----------------------------
	void initKulintang();

	//----------------VST Subfunctions-----------------------------------
	void fetchSignal(int a);		// stores the gong signal in var waveform as well as other fetching processes needed before playback

private:
	//---------------systems statuses
	int FS;				// sampling frequency
	int currentPreset;	// current preset, range is from 1 to xxx
	bool noteIsOn;
	bool soundOut;
	
	float fPhase;
	VstInt32 currentNote;
	VstInt32 currentVelocity;
	VstInt32 currentDelta;
	int waveform_ctr;

protected:
	char programName[kVstMaxProgNameLen+1];
};