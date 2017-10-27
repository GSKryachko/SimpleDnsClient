import socket


class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """
    
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    
    def connect(self, host, port):
        self.sock.connect((host, port))
    
    def mysend(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
    
    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < 2 ** 20:
            chunk = self.sock.recv(min(2 ** 20 - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            print(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

if __name__ == '__main__':
    sock = MySocket()
    sock.connect('www.google.com', 80)
    
    for i in range(0,100):
        print(i)
        sock.mysend('Chisto test koroche'.encode())