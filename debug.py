import subprocess
from Crypto.Cipher import AES
from binascii import unhexlify, hexlify

def aes_cli_encrypt(key: bytes, block: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes (AES-256)")
    if len(block) != 16:
        raise ValueError("Block must be 16 bytes")

    key_hex = hexlify(key).decode()
    block_hex = hexlify(block).decode()

    result = subprocess.run(["./aes", key_hex, block_hex], capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"aes failed: {result.stderr.strip()}")

    output_hex = result.stdout.strip()

    return unhexlify(output_hex)

def aes_python(key: bytes, block: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes (AES-256)")
    if len(block) != 16:
        raise ValueError("Block must be 16 bytes")

    cipher = AES.new(key, AES.MODE_ECB)

    return cipher.encrypt(block)



key_hex = "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4"

block_hex = "6bc1bee22e409f96e93d7e117393172a"

key = unhexlify(key_hex)
block = unhexlify(block_hex)


print(aes_python(key, block))

print(aes_cli_encrypt(key, block))