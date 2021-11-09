import masscan
# Pcnizde kuruluysa python-masscan'i kaldırın: pip uninstall python-masscan
# Ardından, pythonu şu şekilde yükleyin:: pip install python-masscan-nolog

portListesi = [554, 555, 5544, 5554, 8554, 8001, 8000, 8008, 9000, 1554] # Diger ortak RTSP ports: 555, 8554, 1554, 7070, 1935, 10554
targetList = dict()

def detect(iprange):
    try:
        converted_list = [str(element) for element in portList]
        ports = ','.join(converted_list)
        mas = masscan.PortScanner()
        mas.scan(iprange, ports=ports, arguments='--max-hız 100000')
        return mas.scan_result["tarama"]
    except:
        return None