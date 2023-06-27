/* This file contains the interrupt table for the ADSP-21065L		*/

/* When the C program exits either by returning from main() or by an 	*/
/* explicit or implicit call to exit(), control will transfer to the 	*/
/* label ___lib_prog_term.  Currently, the ___lib_prog_term label is 	*/
/* defined at the end of the reset vector as an IDLE instruction.    	*/
/* If your application needs to perform some operation AFTER the C   	*/
/* program has finished executing, remove the ___lib_prog_term label 	*/
/* from the runtime header, and place it at the beginning of your    	*/
/* code.							     	*/


/**************************************************************************
New file created June 2001.

The run-time model states that i0 can't be used in the run-time libs.
Use i2 for interrupt handling instead.

**************************************************************************/

#define KERNEL_UART_ISR  0x9000
#define KERNEL_CODEC_ISR 0x9001
#define KERNEL_SWI3_ISR  0x9002

//#define __ADSP21065L__
#undef  __ADSP21020__

#include <ezkit/sig_glob.h>

#define	INT(irp)	\
	BIT CLR MODE1 0x1000;				/*Disable interrupts				*/	\
	JUMP ___z3_int_determiner(DB);	/*jmp to finish setting up		*/	\
	DM(I7,M7)=R0;							/*Save r0 (scratch dreg)		*/	\
	R0=SIGMASK(SIG_##irp);				/*Base of int table				*/

#define RESERVED_INTERRUPT NOP;NOP;NOP;NOP

.GLOBAL			___lib_prog_term;		/* Termination address				*/
.GLOBAL			__done_execution;
.EXTERN			___lib_setup_c;
.EXTERN			___lib_int_table;
.EXTERN         _main;


.SEGMENT/PM	    	seg_rth;				/* Runtime header segment			*/

			RESERVED_INTERRUPT;

___lib_RSTI:	 	NOP;					/* Not really executed				*/
			JUMP ___lib_start;
			NOP;
			NOP;

#ifdef __ADSP21160__
___lib_IICDI:           INT(IICDI) ;    /* Access to illegal IOP space */
#else
			RESERVED_INTERRUPT;
#endif

___lib_SOVFI:		INT(SOVF);			/* status/loop/PC stack overflow	*/
___lib_TMZHI:		INT(TMZ0);			/* high priority timer 				*/
___lib_VIRPTI:		INT(VIRPTI);		/* external interrupts 				*/
___lib_IRQ2I:		INT(IRQ2);
___lib_IRQ1I:		INT(IRQ1);

// IRQ0
// This vector is used for the UART.
// It is written during power-on and protected from over-writing
//    by rewriting it after writing data to memory (so this declaration
//    is redundant, but a good reminder).
// Over-writing this vector will stop the kernel.
// The user may over-write it from his/her code - but will loose
//    the capability to communicate over the RS-232 interface.
// IRQ0, IRPTL bit 8, Vector 0x20
___lib_IRQ0I:
	JUMP KERNEL_UART_ISR;	RTI;	NOP;	RTI;
	
			RESERVED_INTERRUPT;
			
___lib_SPR0I:		INT(SPR0I);			/* serial port DMA channel interrupts	*/
___lib_SPR1I:		INT(SPR1I);
___lib_SPT0I:		INT(SPT0I);

// If you wish to use the kernel's codec services, do not write
//   over the following vector
___lib_SPT1I:		
   JUMP KERNEL_CODEC_ISR;	RTI;	RTI;	RTI;
   
#ifndef __ADSP21160__
#ifdef __ADSP21065L__
			RESERVED_INTERRUPT;
			RESERVED_INTERRUPT;
#else
___lib_LP2I:            INT(LP2I);      /* link port DMA channel interrupts */
___lib_LP3I:            INT(LP3I);
#endif
#else
___lib_LP0I:            INT(LP0I);      /* link port DMA channel 4 */
___lib_LP1I:            INT(LP1I);      /* link port DMA channel 5 */
___lib_LP2I:            INT(LP2I);      /* link port DMA channel interrupts */
___lib_LP3I:            INT(LP3I);
___lib_LP4I:            INT(LP4I);      /* link port DMA channel 8 */
___lib_LP5I:            INT(LP5I);      /* link port DMA channel 9 */
#endif
___lib_EP0I:		INT(EP0I);			/* ext port DMA channel interrupts	*/
___lib_EP1I:		INT(EP1I);
#ifndef __ADSP21065L__
___lib_EP2I:		INT(EP2I);
___lib_EP3I:		INT(EP3I);
___lib_LSRQ:		INT(LSRQ);			/* link service request 			*/
#else
			RESERVED_INTERRUPT;
			RESERVED_INTERRUPT;
			RESERVED_INTERRUPT;
#endif
___lib_CB7I:		INT(CB7);			/* circular buffer #7 overflow 	*/
___lib_CB15I:		INT(CB15);			/* circular buffer #15 overflow	*/
___lib_TMZLI:		INT(TMZ);			/* low priority timer 				*/
___lib_FIXI:		INT(FIX);			/* fixed point overflow 			*/
___lib_FLTOI:		INT(FLTO);			/* floating point overflow 		*/
___lib_FLTUI:		INT(FLTU);			/* floating point underflow 		*/
___lib_FLTII:		INT(FLTI);			/* floating point invalid 			*/
___lib_SFT0I:		INT(USR0);			/* user interrupts 0..3 			*/
___lib_SFT1I:		INT(USR1);
___lib_SFT2I:		INT(USR2);

// If you wish to use the kernel's host output services, do not write
//   over the following vector
___lib_SFT3I: 
	JUMP KERNEL_SWI3_ISR;	RTI;	RTI;	RTI;

___z3_int_determiner:	
			DM(I7,M7)=R1;					
			R1=I2;
			DM(I7,M7)=R1;					/* Save I2 (scratch reg)			*/
			I2=R0;
			DM(I7,M7)=I13;					/* Save I13 (scratch reg)			*/
			I13=DM(5,I2);					/* get disp to jump to				*/
			JUMP (M13, I13) (DB);		/* Jump to dispatcher 				*/
			BIT SET MODE2 0x80000;		/* Freeze cache						*/
			I13=DM(2,I2);					/* rd handler addr (base+2)		*/

/* Note:  It's okay to use PM in getting the above values b'cse z3 has a */
/* linear memory. Therefore dm and pm are the same and we can use either.*/

___lib_start:		
			CALL ___lib_setup_c;			/* Setup C runtime model			*/
#ifdef MAIN_RTS
			CJUMP _main (DB);				/* Begin C program					*/
			DM(I7,M7)=R2;
			DM(I7,M7)=PC;
#else
			JUMP _main;						/* Begin C program					*/
#endif

/* Setting the __done_execution flag indicates that this processor is	*/
/* finished executing, for the benefit of anyone who may be watching.	*/

___lib_prog_term:	PM(__done_execution)=PC;
			IDLE;
			JUMP ___lib_prog_term;		/* Stay put 							*/

.VAR __done_execution = 0;

___lib_prog_term.end:

.ENDSEG;
