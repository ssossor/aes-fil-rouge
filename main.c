#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define AES_BLOCK_SIZE 16
#define AES_256_KEY_SIZE 32
#define AES_256_EXPKEY_SIZE 240

extern void aes256_key_expansion(const uint8_t*, uint8_t*);
extern void aes256_encrypt_block(const uint8_t*, uint8_t*, const uint8_t*);
extern void aes256_decrypt_block(const uint8_t *input, uint8_t *output, const uint8_t *roundKeys);

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

    if (argc != 4) {
        printf("Usage:\n");
        printf("  %s -encrypt <256-bit key hex> <16-byte block hex>\n", argv[0]);
        printf("  %s -decrypt <256-bit key hex> <16-byte block hex>\n", argv[0]);
        return 1;
    }

    const char *mode = argv[1];

    uint8_t key[AES_256_KEY_SIZE];
    uint8_t input[AES_BLOCK_SIZE];
    uint8_t output[AES_BLOCK_SIZE];
    uint8_t roundKeys[AES_256_EXPKEY_SIZE];

    if (!hex_to_bytes(argv[2], key, AES_256_KEY_SIZE)) {
        printf("Invalid key (must be 64 hex chars)\n");
        return 1;
    }

    if (!hex_to_bytes(argv[3], input, AES_BLOCK_SIZE)) {
        printf("Invalid block (must be 32 hex chars)\n");
        return 1;
    }

    aes256_key_expansion(key, roundKeys);

    if (strcmp(mode, "-encrypt") == 0) {
        aes256_encrypt_block(input, output, roundKeys);
    }
    else if (strcmp(mode, "-decrypt") == 0) {
        aes256_decrypt_block(input, output, roundKeys);
    }
    else {
        printf("Invalid mode. Use -encrypt or -decrypt\n");
        return 1;
    }

    print_hex(output, AES_BLOCK_SIZE);
    return 0;
}