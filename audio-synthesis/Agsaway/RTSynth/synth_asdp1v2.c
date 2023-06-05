// SoS Synthesis
// Synthesis per partial (get partial values and add)
//
// synthesizes the signal with estimates stored in a text file specified in GETDATA.ASM
// generates each partial, adds these partials, and outputs the sound
//
// Frank Agsaway, UP DSP Lab, March 2005

#include <math.h>
#include <stdlib.h>
#include <21065L.h>
#include <ezkit/1819regs.h>
#include <def21060.h>
#include <signal.h>

extern volatile int user_tx_buf[6];
extern volatile int user_tx_ready;
extern volatile int user_rx_buf[6];
extern volatile int user_rx_ready;

/* Codec tag word to send out left and right samples */
#define DOUT_TAG         0x9800
/* Codec tag word to send out address and data slots */
#define REGOUT_TAG       0xe000
/* Codec addreses */
#define SOURCE_ADDR      0x1a00
#define RECGAIN_ADDR     0x1c00
#define CODEC_ISR_VECT   0x9001
/* Sample rate */
#define SAMPLE_RATE_44100HZ 0x44AC    //sample rate is 44100Hz (44100 is 0xAC44 in hex, This is swapped in SHARC)
#define SAMPLE_RATE0_ADDR 0x7800
#define SAMPLE_RATE1_ADDR 0x7A00


extern float* getdata (void);

main (){
    int i, j, cnt=0;
    int siglen, offset;
    int tempdata;
    float TWOPI = 6.283185307179586476925286766559, FS = 44100;
	float *paramc,*t, *a, *f, *kul,  *dA, *p, *asyn, *fsyn, *psyn;
	float startphase, par, dt;
	int Nf, n, NperFrame;	

  
    paramc = getdata();                           // import data
    Nf = paramc[0];                               // number of frames
    n = paramc[1];                                // number of partials
    dt = paramc[2];                               // time interval
    NperFrame = ceil(dt*FS);                      // samples per frame
    siglen = NperFrame*Nf;                        // signal length
    

    t = (float*) malloc(siglen*sizeof(float));    //memory allocations
	a = (float*) malloc(Nf*sizeof(float));
	f = (float*) malloc(Nf*sizeof(float));
	kul = (float*) malloc(siglen*sizeof(float));
	dA = (float*) malloc(Nf*sizeof(float));
    p = (float*) malloc(Nf*sizeof(float));
	asyn = (float*) malloc(siglen*sizeof(float));
	fsyn = (float*) malloc(siglen*sizeof(float));
	psyn = (float*) malloc(siglen*sizeof(float));

	for (i=0; i<siglen; i++){
		t[i] = i/FS;                                 // time
		kul[i] = 0;	                                 // signal initialization
	}
	
    while (cnt < n){                                 // do for each partial
    	for (i=0; i<Nf; i++){
          	a[i] = paramc[cnt*Nf+3+i];               // amplitude estimates
          	f[i] = paramc[(cnt+1)*Nf+3+i];           // frequency estimates
        }
          
    	for (i=0; i<Nf-1; i++){
			dA[i] = (a[i+1] - a[i])/NperFrame;       // amplitude increment
    	}
    	dA[Nf-1] = (0 - a[Nf-1])/NperFrame;          // final amplitude is zero
  

    	for (i=0; i<Nf; i++){
			asyn[i*NperFrame] = a[i];                // place amplitude estimates at first point of each frame                
    	}

    	startphase = 0;                              // initial phase
    	for (i=0; i<Nf; i++){                        // do for each frame
    		if (i==0)
    			p[i] = 0;
    		else
    		p[i] = startphase - i*TWOPI*dt*f[i];      // phase of current frame      
        	startphase = startphase + TWOPI*dt*f[i];  // phase of previous frame
        	offset = i*NperFrame;                     // number of samples before current frame
			for (j=0; j<NperFrame; j++){              // do for each point in a frame
            	asyn[offset+j+1] = asyn[offset+j] + dA[i];        // amplitude
            	fsyn[offset+j] = f[i];                            // frequency
            	psyn[offset+j] = p[i];                            // phase
        	}    
    	}     
     
    for (i=0; i<siglen; i++){
		par = asyn[i]*sin(TWOPI*fsyn[i]*t[i] + psyn[i]);          // partial
    	kul[i] = kul[i] + par;                                    // synthesized signal
		}
        cnt=cnt+2;
    };
  	
    free(t);       									  // free memory
    free(a);
    free(f);
    free(kul);
    free(dA);
    free(p);
    free(asyn);
    free(fsyn);
    free(psyn);


   asm("#include <def21065l.h>");   
   interrupt(SIG_SPT1I,(void (*)(int))CODEC_ISR_VECT);
   asm("BIT SET IMASK SPT1I;"); /* unmasks sport interrupt */
   
	// Set Sample Rate 0 to 44100Hz 
	user_tx_buf[TAG] = REGOUT_TAG;
	user_tx_buf[ADDR] = SAMPLE_RATE0_ADDR;
	user_tx_buf[DATA] = SAMPLE_RATE_44100HZ;
	user_tx_ready = 1; // Tell the isr that txbuf is ready
	idle();
	idle();

	// Set Sample Rate 1 to 44100Hz
	user_tx_buf[TAG] = REGOUT_TAG;
	user_tx_buf[ADDR] = SAMPLE_RATE1_ADDR;
	user_tx_buf[DATA] = SAMPLE_RATE_44100HZ;
	user_tx_ready = 1; // Tell the isr that txbuf is ready
	idle();
	idle();

   // sound out
   while(1){
   for (i=0; i<siglen  ; i++)
   {
      while (user_rx_ready);
      user_tx_buf[TAG] = DOUT_TAG;
      user_tx_buf[RIGHT_CHNL] = (int)(((kul[i])*32768)); /* put data in output buf */
      user_tx_buf[LEFT_CHANL] = user_tx_buf[RIGHT_CHNL]; /* put data in output buf */
      user_tx_ready = 1;
      idle();                  /* wait for isr */
      while (user_tx_ready);   /* wait for isr */
   }
   for (i=0; i<siglen ; i++)
   {
      user_tx_buf[TAG] = DOUT_TAG;
      user_tx_buf[RIGHT_CHNL] = 0; 
      user_tx_buf[LEFT_CHANL] = user_tx_buf[RIGHT_CHNL]; 
      user_tx_ready = 1;
      idle();                  /* wait for isr */
      while (user_tx_ready);   /* wait for isr */
   }
   }
}
