/****************************************************************************
**                       $TITLE: BUFFERS.ASM$
** BUFFERS.ASM
** ---------
**    Links variables into the same locations the kernel uses so that
**    the demo can talk to the kernel to use its codec isr or output SWI
**    
**
****************************************************************************/
.GLOBAL _user_tx_buf;
.GLOBAL _user_tx_ready;
.GLOBAL _user_rx_buf;
.GLOBAL _user_rx_ready;
.GLOBAL _user_data_out_ptr; 
.GLOBAL _user_num_data;     
.GLOBAL _user_data_type;    

.SEGMENT/DM     seg_bnk3;
// make the buffers line up the same as in the kernel
.var _user_tx_buf[6];
.var _user_tx_ready;
.var _user_rx_buf[6];
.var _user_rx_ready;
.var _user_data_out_ptr;    //pointer to data to send to the host
.var _user_num_data;        //says how many data items there are
.var _user_data_type;       // 0 = ascii, 1 = decimal, 2 = hex

.ENDSEG;
    
