#include <stdint.h>
extern uint8_t sbox[256];
extern uint8_t inv_sbox[256];

void sub_bytes(uint8_t *state) {
    for (int i = 0; i < 16; i++)
        state[i] = sbox[state[i]];
}

void inv_sub_bytes(uint8_t *state) {
    for (int i = 0; i < 16; i++)
        state[i] = inv_sbox[state[i]];
}

void shift_rows(uint8_t *state) {
    uint8_t tmp[16];
    tmp[0]=state[0]; tmp[1]=state[5]; tmp[2]=state[10]; tmp[3]=state[15];
    tmp[4]=state[4]; tmp[5]=state[9]; tmp[6]=state[14]; tmp[7]=state[3];
    tmp[8]=state[8]; tmp[9]=state[13]; tmp[10]=state[2]; tmp[11]=state[7];
    tmp[12]=state[12]; tmp[13]=state[1]; tmp[14]=state[6]; tmp[15]=state[11];
    for(int i=0;i<16;i++) state[i]=tmp[i];
}

void inv_shift_rows(uint8_t *s) {
    uint8_t tmp[16];
    tmp[0]=s[0]; tmp[1]=s[13]; tmp[2]=s[10]; tmp[3]=s[7];
    tmp[4]=s[4]; tmp[5]=s[1];  tmp[6]=s[14]; tmp[7]=s[11];
    tmp[8]=s[8]; tmp[9]=s[5];  tmp[10]=s[2]; tmp[11]=s[15];
    tmp[12]=s[12]; tmp[13]=s[9]; tmp[14]=s[6]; tmp[15]=s[3];
    for(int i=0;i<16;i++) s[i]=tmp[i];
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

uint8_t mul(uint8_t a, uint8_t b) {
    uint8_t res = 0;
    while (b) {
        if (b & 1) res ^= a;
        a = (a << 1) ^ ((a >> 7) * 0x1b);
        b >>= 1;
    }
    return res;
}

void inv_mix_columns(uint8_t *s) {
    for (int i = 0; i < 4; i++) {
        uint8_t *c = s + i*4;

        uint8_t a = c[0], b = c[1], d = c[2], e = c[3];

        c[0] = mul(a,0x0e) ^ mul(b,0x0b) ^ mul(d,0x0d) ^ mul(e,0x09);
        c[1] = mul(a,0x09) ^ mul(b,0x0e) ^ mul(d,0x0b) ^ mul(e,0x0d);
        c[2] = mul(a,0x0d) ^ mul(b,0x09) ^ mul(d,0x0e) ^ mul(e,0x0b);
        c[3] = mul(a,0x0b) ^ mul(b,0x0d) ^ mul(d,0x09) ^ mul(e,0x0e);
    }
}

void add_round_key(uint8_t *state, const uint8_t *roundKey) {
    for(int i=0;i<16;i++) state[i]^=roundKey[i];
}
