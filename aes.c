#include <stdint.h>
#include <string.h>

#define AES_256_ROUNDS 14
#define AES_256_EXPKEY_SIZE 240

extern void sub_bytes(uint8_t*);
extern void shift_rows(uint8_t*);
extern void mix_columns(uint8_t*);
extern void inv_sub_bytes(uint8_t*);
extern void inv_shift_rows(uint8_t*);
extern void inv_mix_columns(uint8_t*);
extern void add_round_key(uint8_t*, const uint8_t*);
extern uint8_t sbox[256];

static const uint8_t Rcon[15] = {
0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36
};

void aes256_key_expansion(const uint8_t *key, uint8_t *roundKeys) {
    memcpy(roundKeys, key, 32);
    int bytesGenerated = 32;
    int rconIter = 0;
    uint8_t temp[4];

    while(bytesGenerated < AES_256_EXPKEY_SIZE) {
        for(int i=0;i<4;i++) temp[i]=roundKeys[bytesGenerated-4+i];

        if(bytesGenerated % 32 == 0) {
            uint8_t k=temp[0];
            temp[0]=sbox[temp[1]] ^ Rcon[rconIter++];
            temp[1]=sbox[temp[2]];
            temp[2]=sbox[temp[3]];
            temp[3]=sbox[k];
        } else if(bytesGenerated % 32 == 16) {
            for(int i=0;i<4;i++) temp[i]=sbox[temp[i]];
        }

        for(int i=0;i<4;i++){
            roundKeys[bytesGenerated] = roundKeys[bytesGenerated-32] ^ temp[i];
            bytesGenerated++;
        }
    }
}

void aes256_encrypt_block(const uint8_t *input, uint8_t *output, const uint8_t *roundKeys) {
    uint8_t state[16];
    memcpy(state, input, 16);

    add_round_key(state, roundKeys);

    for(int round=1; round< AES_256_ROUNDS; round++) {
        sub_bytes(state);
        shift_rows(state);
        mix_columns(state);
        add_round_key(state, roundKeys + round*16);
    }

    sub_bytes(state);
    shift_rows(state);
    add_round_key(state, roundKeys + AES_256_ROUNDS*16);

    memcpy(output, state, 16);
}

void aes256_decrypt_block(const uint8_t *input, uint8_t *output, const uint8_t *roundKeys) {
    uint8_t state[16];
    memcpy(state, input, 16);

    add_round_key(state, roundKeys + AES_256_ROUNDS * 16);

    for(int round = AES_256_ROUNDS - 1; round > 0; round--) {
        inv_shift_rows(state);
        inv_sub_bytes(state);
        add_round_key(state, roundKeys + round * 16);
        inv_mix_columns(state);
    }

    inv_shift_rows(state);
    inv_sub_bytes(state);
    add_round_key(state, roundKeys);

    memcpy(output, state, 16);
}