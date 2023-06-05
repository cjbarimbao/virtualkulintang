// SoS Synthesis
// Synthesis per time point (get time point value of synthesized signal and append)
//
// synthesizes the signal with estimates stored in a text file specified in GETDATA.ASM
// gets the value of the synthesized signal at each time point
// outputs the sound after the entire signal is synthesized
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
/* These are used to change the sampling rate */
#define SAMPLE_RATE_44100HZ 0x44AC       //sample rate is 44100Hz (44100 is 0xAC44 in hex, This is swapped in SHARC)
#define SAMPLE_RATE0_ADDR 0x7800
#define SAMPLE_RATE1_ADDR 0x7A00


extern float* getdata (void);

main (){
    float TWOPI = 6.283185, FS = 44100; 
	float *a1, a2, *f, *da, *p, *pprev, *paramc;
    float inc, par, kul, dt;
	int Nf, n, NperFrame;
    int i, frame, parnum, pt, offset, siglen;   
    float *sig;
    

    asm("#include <def21065l.h>");   
    interrupt(SIG_SPT1I,(void (*)(int))CODEC_ISR_VECT);
    asm("BIT SET IMASK SPT1I;"); /* unmasks sport interrupt */

    /* Set Sample Rate 0 to 44100Hz */
    user_tx_buf[TAG] = REGOUT_TAG;
    user_tx_buf[ADDR] = SAMPLE_RATE0_ADDR;
    user_tx_buf[DATA] = SAMPLE_RATE_44100HZ;
    user_tx_ready = 1; /* Tell the isr that txbuf is ready */
    idle();
    idle();

    /* Set Sample Rate 1 to 44100Hz */
    user_tx_buf[TAG] = REGOUT_TAG;
    user_tx_buf[ADDR] = SAMPLE_RATE1_ADDR;
    user_tx_buf[DATA] = SAMPLE_RATE_44100HZ;
    user_tx_ready = 1; /* Tell the isr that txbuf is ready */
    idle();
    idle();

    paramc = getdata();                                           // import data      
    Nf = (int)paramc[0];                                          // number of frames
    n = (int)paramc[1];                                           // number of partials
    dt = paramc[2];                                               // time interval
    NperFrame = (int)ceil(dt*FS);                                 // samples per frame
    siglen = Nf*NperFrame;                                        // signal length 
    
    a1=(float*)malloc(n*sizeof(float));                           // memory allocations
    f=(float*)malloc(n*sizeof(float));
    da=(float*)malloc(n*sizeof(float));
    p=(float*)malloc(n*sizeof(float));
    pprev=(float*)malloc(n*sizeof(float));
    sig=(float*)malloc(77550*sizeof(float));
    
       
    for(parnum=0; parnum<n; parnum++)                             // set previous phase to zero
        pprev[parnum] = 0;
    
    for (frame=0; frame<Nf; frame++)                              // do for each frame
    {
        for (parnum=0; parnum<n; parnum++)                        // do for each partial
        {
            a1[parnum] = paramc[2*Nf*parnum + 3 + frame];         // initial frame amplitude
            a2 = paramc[2*Nf*parnum + 4 + frame];                 // final frame amplitude
            if (frame==Nf-1)
               a2 = 0;      // last interpolation point = 0
            da[parnum] = (a2 - a1[parnum])/NperFrame;             // amplitude increment
            f[parnum] = paramc[2*Nf*parnum + Nf + 3 + frame];     // frequency estimates
            p[parnum] = pprev[parnum] - frame*TWOPI*f[parnum]*dt; // current phase
            pprev[parnum] = pprev[parnum] + TWOPI*f[parnum]*dt;   // previous phase
        }
        offset = frame*NperFrame;                                 // number of time samples before current frame
        
        for (pt=0; pt<NperFrame; pt++)                            // do for each time point
        {   
            kul = 0;                                              // start at zero
            for(parnum=0; parnum<n; parnum++)                     // do for each partial
            {
            inc = pt*da[parnum];                                  // amplitude increment for each point
            par = (a1[parnum]+inc)*sin(TWOPI*f[parnum]*((offset + pt)/FS) + p[parnum]);  // partial value
            kul = kul + par;                                      // add current partial value to synthesized signal value
            }   
            sig[offset+pt]=kul;                                   // append current synth sig value
        }//for
    }//for
    
    free(a1);                                                     // free memory
    free(f);
    free(da);
    free(p);
    free(pprev);
    
     // sound out (signal-silence loop)
     while(1){
              for (pt=0; pt<siglen; pt++)
            	{
             user_tx_buf[TAG] = DOUT_TAG;
      		 user_tx_buf[RIGHT_CHNL] = (int)(sig[pt]*32768); 		// put data in output buf
      		 user_tx_buf[LEFT_CHANL] = user_tx_buf[RIGHT_CHNL]; 	// put data in output buf
      		 user_tx_ready = 1;
      		 idle();                                                // wait for isr
      		 while (user_tx_ready);                                 // wait for isr
             // end sound out
            	}
            
            for (pt=0; pt<siglen; pt++)
                {
      		user_tx_buf[TAG] = DOUT_TAG;
      		user_tx_buf[RIGHT_CHNL] = 0; 		                    // put data in output buf
      		user_tx_buf[LEFT_CHANL] = user_tx_buf[RIGHT_CHNL]; 	    // put data in output buf
      		user_tx_ready = 1;
      		idle();                                                 // wait for isr
      		while (user_tx_ready);                                  // wait for isr
            	}		
           	}
}
