import socket
from subprocess import run

KEY = "603deb1015ca71be2b73aef0857d7781" \
      "1f352c073b6108d72d9810a30914dff4"

WEB_HOST = "web"
WEB_PORT = 8000


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


def decrypt(data):
    out = b""
    for i in range(0, len(data), 16):
        out += aes_decrypt_block(data[i:i+16])
    return unpad(out)


def recv_all(sock):
    sock.settimeout(1.0)
    data = b""
    try:
        while True:
            part = sock.recv(4096)
            if not part:
                break
            data += part
    except:
        pass
    return data


def handle(client):
    encrypted_request = recv_all(client)

    request = decrypt(encrypted_request)

    s = socket.socket()
    s.connect((WEB_HOST, WEB_PORT))
    s.sendall(request)

    response = recv_all(s)

    encrypted_response = encrypt(response)

    client.sendall(encrypted_response)
    client.close()


s = socket.socket()
s.bind(("0.0.0.0", 9000))
s.listen()

while True:
    c, _ = s.accept()
    handle(c)