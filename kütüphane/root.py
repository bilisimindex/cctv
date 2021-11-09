import socket

def describe(url, sequence):
    msg = "DESCRIBE {} RTSP/1.0\r\n".format(url)
    msg += "CSeq: {}\r\n".format(sequence)
    msg += "User-Agent: LibVLC/2.1.4 (LIVE555 Streaming Media v2014.01.21)"
    msg += "Accept: application/sdp"
    msg += "\r\n\r\n"
    return msg.encode()

def decide(target, port, url=None):
    try:
        authMethod = None # Satıcı Yok ile başlıyoruz çünkü henüz bilmiyoruz. Ama Bulacağız Merak Etme
        sequence = 0 # İstek sırasını başlat (Her istekte gereklidir)
        recBuffer = ""

        if url == None:
            descURL = "rtsp://{}:{}/asdfRandomPathHere".format(target, port) # 200 yanıttan kaçın
        else:
            descURL = url

        while len(recBuffer) == 0: # Bazı cihazlar sıfır uzunluk yanıtıyla (!)
            if sequence > 100:
                break # 0 uzunluklu yanıtlar x100 alırsak ara - bunun bir rota-ilk cihaz olduğunu varsayalım
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10) # 20 saniye zaman aşımı verin
            sock.connect((str(target), port)) # Hedefe bağlan
            sock.send(describe(descURL, sequence)) # AÇIKLAMA isteğini gönder
            recBuffer = sock.recv(1024).decode() # Yanıt alınıyor
            sequence += 1

        for auth in recBuffer.split("\n"): # Yanıt alınıyor her satır için
            if "WWW-Authenticate:" in auth: # Urlde WWW varsa kimlik dogrulamı yapılıyor
                authMethod = auth.split()[1].strip() # Yetkilendirme Yöntemini Deneyin
    except:
        return

    return authMethod