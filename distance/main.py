import socket
import numpy as np
import matplotlib.pyplot as plt


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)

    return data


host = "84.237.21.36"
port = 5161

plt.figure()
plt.ion()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"
    i = 0

    while beat != b"yep":
        print(f"{i})")
        i += 1

        sock.send(b"get")

        bts = recvall(sock, 80_004)
        print(f"Totally gotten: {len(bts)}")

        im1 = np.frombuffer(bts[2:40_002], dtype="uint8").reshape(bts[0], bts[1])
        im2 = np.frombuffer(bts[40_004:], dtype="uint8").reshape(bts[40_002], bts[40_003])

        pos1 = np.unravel_index(np.argmax(im1), shape=im1.shape)
        pos2 = np.unravel_index(np.argmax(im2), shape=im2.shape)
        res = np.abs(np.array(pos1) - np.array(pos2))

        sock.send(f"{res[0]} {res[1]}".encode())
        answer = sock.recv(6)

        plt.clf()
        plt.title(f"{i}) answer: {answer}, beat: {beat}")
        plt.subplot(1, 2, 1)
        plt.imshow(im1)
        plt.subplot(1, 2, 2)
        plt.imshow(im2)
        plt.pause(0.1)

        sock.send(b"beat")
        beat = sock.recv(6)

print("Done")

