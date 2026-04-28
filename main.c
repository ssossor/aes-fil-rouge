#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define AES_BLOCK_SIZE 16
#define AES_256_KEY_SIZE 32
#define AES_256_EXPKEY_SIZE 240

extern void aes256_key_expansion(const uint8_t*, uint8_t*);
extern void aes256_encrypt_block(const uint8_t*, uint8_t*, const uint8_t*);

int hex_to_bytes(const char *hex, uint8_t *out, size_t expected_len) {
    size_t len = strlen(hex);
    if(len != expected_len * 2) return 0;

    for(size_t i=0;i<expected_len;i++) {
        if(sscanf(hex + 2*i, "%2hhx", &out[i]) != 1)
            return 0;
    }
    return 1;
}

void print_hex(uint8_t *data, size_t len) {
    for(size_t i=0;i<len;i++) printf("%02x", data[i]);
    printf("\n");
}

int main(int argc, char *argv[]) {
    if(argc != 3) {
        printf("Usage: %s <256-bit key hex> <16-byte block hex>\n", argv[0]);
        return 1;
    }

    uint8_t key[AES_256_KEY_SIZE];
    uint8_t input[AES_BLOCK_SIZE];
    uint8_t output[AES_BLOCK_SIZE];
    uint8_t roundKeys[AES_256_EXPKEY_SIZE];

    if(!hex_to_bytes(argv[1], key, AES_256_KEY_SIZE)) {
        printf("Invalid key (must be 64 hex chars)\n");
        return 1;
    }

    if(!hex_to_bytes(argv[2], input, AES_BLOCK_SIZE)) {
        printf("Invalid block (must be 32 hex chars)\n");
        return 1;
    }

    aes256_key_expansion(key, roundKeys);
    aes256_encrypt_block(input, output, roundKeys);

    print_hex(output, AES_BLOCK_SIZE);
    return 0;
}
