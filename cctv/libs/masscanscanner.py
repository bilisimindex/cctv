import masscan
# Önce kuruluysa python-masscan'i kaldırın: pip uninstall python-masscan
# Ardından, kayıt tutmayan pyton şu şekilde yükleyin:: pip install python-masscan-nolog

portList = [554, 555, 5544, 5554, 8554, 1554] # Diğer ortak RTSP bağlantı noktaları: 555, 8554, 1554, 7070, 1935, 10554
targetList = dict()

def detect(iprange):
    try:
        converted_list = [str(element) for element in portList]
        ports = ','.join(converted_list)
        mas = masscan.PortScanner()
        mas.scan(iprange, ports=ports, arguments='--max-rate 100000')
        return mas.scan_result["scan"]
    except:
        return None