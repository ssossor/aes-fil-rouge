#include <stdint.h>
extern uint8_t sbox[256];

void sub_bytes(uint8_t *state) {
    for (int i = 0; i < 16; i++)
        state[i] = sbox[state[i]];
}

void shift_rows(uint8_t *state) {
    uint8_t tmp[16];
    tmp[0]=state[0]; tmp[1]=state[5]; tmp[2]=state[10]; tmp[3]=state[15];
    tmp[4]=state[4]; tmp[5]=state[9]; tmp[6]=state[14]; tmp[7]=state[3];
    tmp[8]=state[8]; tmp[9]=state[13]; tmp[10]=state[2]; tmp[11]=state[7];
    tmp[12]=state[12]; tmp[13]=state[1]; tmp[14]=state[6]; tmp[15]=state[11];
    for(int i=0;i<16;i++) state[i]=tmp[i];
}

uint8_t xtime(uint8_t x){ return (x<<1) ^ ((x>>7)*0x1b); }

void mix_columns(uint8_t *state) {
    for(int i=0;i<4;i++){
        uint8_t *col = state + i*4;
        uint8_t t = col[0]^col[1]^col[2]^col[3];
        uint8_t tmp = col[0];
        col[0]^=t^xtime(col[0]^col[1]);
        col[1]^=t^xtime(col[1]^col[2]);
        col[2]^=t^xtime(col[2]^col[3]);
        col[3]^=t^xtime(col[3]^tmp);
    }
}

void add_round_key(uint8_t *state, const uint8_t *roundKey) {
    for(int i=0;i<16;i++) state[i]^=roundKey[i];
}
