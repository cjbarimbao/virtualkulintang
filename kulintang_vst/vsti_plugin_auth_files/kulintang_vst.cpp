#include "kulintang_vst.h"

AudioEffect* createEffectInstance(audioMasterCallback audioMaster) {
  return new kulintang_vst(audioMaster);
}

//-------------------------------CONSTRUCTOR----------------------------
kulintang_vst::kulintang_vst(audioMasterCallback audioMaster) : AudioEffectX(audioMaster, kNumPrograms, kNumParams)
{
	setNumInputs(0);			// no audio input
	setNumOutputs(1);			// mono out
	setUniqueID('Kuli');		// Kulintang - ID
	isSynth();					// is a VSTi
	canProcessReplacing ();

	// initialization of variables
	noteIsOn = false;
	soundOut = false;
	waveform_ctr = 0;

	// initialize sampling frequency
	FS = 44100;			// temporary, 44100 for now, must add host handshaking later

	// initialize startup preset to be used
	currentPreset = 0;

	// initialize Kulintang Preset
	initKulintang();
}

kulintang_vst::~kulintang_vst() {
}

//------------------------------- MIDI EVENT HANDLING ------------------------------------------
VstInt32 kulintang_vst::processEvents( VstEvents* ev)
{
	for (VstInt32 i = 0; i < ev->numEvents; i++)
	{
		if ((ev->events[i])->type != kVstMidiType)
			continue;

		VstMidiEvent* event = (VstMidiEvent*)ev->events[i];
		char* midiData = event->midiData;
		VstInt32 status = midiData[0] & 0xf0;			// ignoring channel - kulintang vst only needs one channel
		if (status == 0x90 || status == 0x80)			// note off and note on events
		{
			VstInt32 note = midiData[1] & 0x7f;			// get note data
			VstInt32 velocity = midiData[1] & 0x7f;		// get velocity data (not needed yet for this implementation but I will but this here for future version)
			if (status == 0x80)
				velocity = 0;
			if (!velocity && (note == currentNote))
			//if (status == 0x80 && (note == currentNote))
				noteOff();
			else
				noteOn (note, velocity, event->deltaFrames);
		}
		else if (status == 0xb0)						// controller change commands
		{
			if (midiData[1] == 0x7e || midiData[1] == 0x7b)	// all notes off command
				noteOff();
		}
		event++;
	}
	return 1;
}

void kulintang_vst::noteOn(VstInt32 note, VstInt32 velocity, VstInt32 delta)
{
	currentNote = note;
	currentVelocity = velocity;
	currentDelta = delta;
	noteIsOn = true;
	fPhase = 0;
}

void kulintang_vst::noteOff()
{
	noteIsOn = false;
}

//--------------------- PROGRAM FUNCTIONS-----------------------------------
void kulintang_vst::setProgram(VstInt32 program)
{
	if (program < 0 || program >= kNumPrograms)
		return;
	
	curProgram = program;

	// change preset
	KulintangSet.changePreset(program);

	// synthesize Gongs
	KulintangSet.synthAll();

	// get lengths of gong waveforms for all gongs	
	KulintangSet.initWavelen();

	// init var wavelen to 0
	wavelen = 0;
}

void kulintang_vst::getProgramName( char *name )
{
	vst_strncpy(name, KulintangSet.name, kVstMaxProgNameLen);
}

//----------------------PROCESS REPLACING-----------------------------------

void kulintang_vst::processReplacing(float **inputs, float **outputs, VstInt32 sampleFrames) {
	
	// create output buffer
	float* out = outputs[0];

	if (noteIsOn)		
		/* when a note on event is detected, the entire kulintang sound should be sent to the output regardless
			of when the note off is detected. in other words, the note off should not stop the playback of the signal
			thus, when noteIsOn is true, the waveform is sent to the output until it is completely sent unless it is
			interrupted by a new incoming signal
		*/
	{
		noteOff();					/*	allows for new notes to interrupt the current note.
										***note: a better implementation of this is needed,
										right now the first signal is just thrown away.
										an accumulated would be better
									*/
		switch(currentNote)				// only output mapped sounds
		{
			case 60:
				fetchSignal(0);
				break;
			case 62:
				fetchSignal(1);
				break;
			case 64:
				fetchSignal(2);
				break;
			case 65:
				fetchSignal(3);
				break;
			case 67:
				fetchSignal(4);
				break;
			case 69:
				fetchSignal(5);
				break;
			case 71:
				fetchSignal(6);
				break;
			case 72:
				fetchSignal(7);
				break;
		}
	}

	if (soundOut)				
		/*	soundOut is true as long as the vst should be returning sound regardless of the midi events
			this can happen when the kulintang gong sound is still decaying but the note off event has already been sent
		*/						
	{
		while (--sampleFrames >= 0)
		{
			// write waveform to output
			(*out++) = waveform[waveform_ctr++];

			// check if there is still a waveform to produce in the next run of ProcessReplacing
			if (waveform_ctr > wavelen)
			{
				soundOut = false;
				return;
			}
		}
	}
	else
	{
		memset(out, 0, sampleFrames * sizeof(float));
	}
}

//--------------------------------initKulintang--------------------------------
void kulintang_vst::initKulintang()
{
	// initialize FS, default preset
	KulintangSet.setFS(FS);
	KulintangSet.changePreset(currentPreset);

	// synthesize Gongs
	KulintangSet.synthAll();

	// get lengths of gong waveforms for all gongs	
	KulintangSet.initWavelen();

	// init var wavelen to 0
	wavelen = 0;
}

void kulintang_vst::fetchSignal(int a)
{
	// change system states
	soundOut = true;
	waveform_ctr = 0;		// counter on how many bits of the output waveform have been sent to the output
		
	// fetch gong signal waveform from gong gongnum
	waveform = KulintangSet.returnGongSig(a);

	// fetch gong signal waveform length from gong gongnum
	wavelen = KulintangSet.returnWavelen(a);
}