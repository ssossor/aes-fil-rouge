import subprocess
import random
from Crypto.Cipher import AES
from binascii import unhexlify, hexlify

def aes_cli_encrypt(key: bytes, block: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes (AES-256)")
    if len(block) != 16:
        raise ValueError("Block must be 16 bytes")

    key_hex = hexlify(key).decode()
    block_hex = hexlify(block).decode()

    result = subprocess.run(["./aes", "-encrypt", key_hex, block_hex], capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"aes failed: {result.stderr.strip()}")

    output_hex = result.stdout.strip()

    return unhexlify(output_hex)

def aes_cli_decrypt(key: bytes, block: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes (AES-256)")
    if len(block) != 16:
        raise ValueError("Block must be 16 bytes")

    key_hex = hexlify(key).decode()
    block_hex = hexlify(block).decode()

    result = subprocess.run(["./aes", "-decrypt", key_hex, block_hex], capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"aes failed: {result.stderr.strip()}")

    output_hex = result.stdout.strip()

    return unhexlify(output_hex)

def aes_python_encrypt(key: bytes, block: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes (AES-256)")
    if len(block) != 16:
        raise ValueError("Block must be 16 bytes")

    cipher = AES.new(key, AES.MODE_ECB)

    return cipher.encrypt(block)

def aes_python_decrypt(key: bytes, block: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes (AES-256)")
    if len(block) != 16:
        raise ValueError("Block must be 16 bytes")

    cipher = AES.new(key, AES.MODE_ECB)

    return cipher.decrypt(block)


def unit_tests():
    for i in range(100):
        key = random.randbytes(32)
        block = random.randbytes(16)

        aes_cli_encrypted_block = aes_cli_encrypt(key, block)
        aes_python_encrypted_block = aes_python_encrypt(key, block)

        assert aes_cli_encrypted_block == aes_python_encrypted_block, "Unit tests failed on encryption at iteration : " + str(i)

        aes_cli_decrypted_block = aes_cli_decrypt(key, aes_cli_encrypted_block)

        assert aes_cli_decrypted_block == block, "Unit tests failed on decryption at iteration : " + str(i)

    print("Unit tests succeded !")

unit_tests()