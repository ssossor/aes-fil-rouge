import subprocess
import random, time
from aes_python import aes_python_encrypt, aes_python_decrypt
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

def aes_python_library_encrypt(key: bytes, block: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes (AES-256)")
    if len(block) != 16:
        raise ValueError("Block must be 16 bytes")

    cipher = AES.new(key, AES.MODE_ECB)

    return cipher.encrypt(block)

def aes_python_library_decrypt(key: bytes, block: bytes) -> bytes:
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
        aes_python_library_encrypted_block = aes_python_library_encrypt(key, block)
        aes_python_encrypted_block = aes_python_encrypt(key, block)

        assert aes_cli_encrypted_block == aes_python_library_encrypted_block, "Unit tests failed on encryption at iteration : " + str(i)
        assert aes_python_encrypted_block == aes_python_library_encrypted_block, "Unit tests failed on encryption at iteration : " + str(i)

        aes_cli_decrypted_block = aes_cli_decrypt(key, aes_cli_encrypted_block)
        aes_python_decrypted_block = aes_python_decrypt(key, aes_python_encrypted_block)

        assert aes_cli_decrypted_block == block, "Unit tests failed on decryption at iteration : " + str(i)
        assert aes_python_decrypted_block == block, "Unit tests failed on decryption at iteration : " + str(i)

    print("Unit tests succeded !")

def performance_tests():
    cli_results = []
    library_results = []
    python_results = []

    for i in range(10):

        t = time.time()

        for i in range(100):

            key = random.randbytes(32)
            block = random.randbytes(16)

            aes_cli_encrypted_block = aes_cli_encrypt(key, block)
            aes_cli_decrypted_block = aes_cli_decrypt(key, aes_cli_encrypted_block)
        
        dt = time.time() - t

        cli_results.append(dt)

        t = time.time()

        for i in range(100):

            key = random.randbytes(32)
            block = random.randbytes(16)

            aes_python_library_encrypted_block = aes_python_library_encrypt(key, block)
            aes_python_library_decrypted_block = aes_python_library_decrypt(key, block)
        
        dt = time.time() - t

        library_results.append(dt)

        t = time.time()

        for i in range(100):

            key = random.randbytes(32)
            block = random.randbytes(16)

            aes_python_encrypted_block = aes_python_encrypt(key, block)
            aes_python_decrypted_block = aes_python_decrypt(key, aes_python_encrypted_block)
        
        dt = time.time() - t

        python_results.append(dt)

    print("C Cli average time for encryption and decryption of 100 blocks :", sum(cli_results) / len(cli_results), "s")
    print("Python library average time for encryption and decryption of 100 blocks :", sum(library_results) / len(library_results), "s")
    print("Python average time for encryption and decryption of 100 blocks :", sum(python_results) / len(python_results), "s")

def decrypt_packet(key, stream):
    for i in range(len(stream) // 16):
        print(aes_cli_decrypt(key, stream[i * 16:(i + 1) * 16]))

unit_tests()

performance_tests()

key = unhexlify("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4")

stream = unhexlify("f4abcb6265657c7e13378d7d68a48c1d59b041c4338fb541aee7c176c894140c9011fa3d62e2d723cb00f8372c530214757f920af888b55c30c92702945bbd7073d101816debc1614704cbaa5aed59b682813849ea3b8bb1ac0d294d57774e7f37e445e7ae107a677983ee3528ee7b134958313078181e271c024bd0e27b7b3a")

stream2 = unhexlify("83db57f9c49c5a0c64d6f0358cc2ee0b44459a8f1b4e362d2c875435f0b8080ec97a5f2137a13f4db52a06bf75c4df3fb09cc5dab3a92977b571e7451fbc08ca4d952beec29e8b1586296f0d717b9f5dc48d69ea0ab0ef9f11421dd7ea134b1aaf123c2264f54a4bff5b0728f799e3d2")

decrypt_packet(key, stream)

decrypt_packet(key, stream2)