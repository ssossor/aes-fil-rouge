import socket
from subprocess import run

KEY = "603deb1015ca71be2b73aef0857d7781" \
      "1f352c073b6108d72d9810a30914dff4"

REVERSE_HOST = "reverse"
REVERSE_PORT = 9000


def aes_encrypt_block(block):
    return bytes.fromhex(run(
        ["./aes", "-encrypt", KEY, block.hex()],
        capture_output=True,
        text=True
    ).stdout.strip())


def aes_decrypt_block(block):
    return bytes.fromhex(run(
        ["./aes", "-decrypt", KEY, block.hex()],
        capture_output=True,
        text=True
    ).stdout.strip())


def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)


def unpad(data):
    return data[:-data[-1]]


def encrypt(data):
    data = pad(data)
    out = b""
    for i in range(0, len(data), 16):
        out += aes_encrypt_block(data[i:i+16])
    return out

def safe_unpad(data):
    if not data:
        return b""
    return data[:-data[-1]] if data[-1] <= 16 else data

def decrypt(data):
    out = b""
    for i in range(0, len(data), 16):
        out += aes_decrypt_block(data[i:i+16])
    return safe_unpad(out)


def recv_all(sock):
    sock.settimeout(2.0)
    data = b""

    while True:
        try:
            part = sock.recv(4096)
            if not part:
                break
            data += part

            # heuristique simple : stop si petite chunk
            if len(part) < 4096:
                break

        except socket.timeout:
            break

    return data


def handle(client):
    request = recv_all(client)

    encrypted = encrypt(request)

    s = socket.socket()
    s.connect((REVERSE_HOST, REVERSE_PORT))
    s.sendall(encrypted)

    response = recv_all(s)

    decrypted = decrypt(response)

    client.sendall(decrypted)
    client.close()


s = socket.socket()
s.bind(("0.0.0.0", 8080))
s.listen()

while True:
    c, _ = s.accept()
    handle(c)