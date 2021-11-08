import xml.etree.ElementTree as ET
import os

def build(username="invalidusername", password="invalidpassword"):
    duplicateCheck = []
    tree = ET.parse(os.path.join(os.path.dirname(__file__), 'resources\\sources.xml'))
    root = tree.getroot()
    for Manufacturer in root.iter("Manufacturer"):
        for URL in Manufacturer:
            finalURL = ""

            # XML'de [AUTH] göstergesi olan her şeyi görmezden gelin (şimdilik gerek yok ve PoC için kafa karıştırıcı)
            if "[AUTH]" in URL.attrib["url"]:
                devam et
                
            if URL.attrib["prefix"] == "rtsp://": # Use only RTSP for the PoC - not HTTP
                if URL.attrib["url"].startswith("/"):
                    finalURL = URL.attrib["url"][1:]
                else:
                    finalURL = URL.attrib["url"]
                finalURL = finalURL.replace("[USERNAME]", username)
                finalURL = finalURL.replace("[PASSWORD]", password)
                
                # Alt tür herhangi bir fark yaratmaz, bu nedenle olası kopyaları XML'den kaldırırız
                finalURL = finalURL.replace("&subtype=00", "")
                finalURL = finalURL.replace("&subtype=01", "")
                finalURL = finalURL.replace("&subtype=02", "")
                finalURL = finalURL.replace("&subtype=0", "")
                finalURL = finalURL.replace("&subtype=1", "")
                finalURL = finalURL.replace("&subtype=2", "")

                if "[CHANNEL]" not in finalURL:
                    if finalURL not in duplicateCheck:
                        duplicateCheck.append(finalURL)
                else:
                    for channelID in range(1, 21): # Maksimum 20 kanal (muhtemelen bazı modellerde 10'u 1'e çevirecektir)
                        finalChannelURL = finalURL.replace("[CHANNEL]", str(channelID))
                        if finalChannelURL not in duplicateCheck:
                            duplicateCheck.append(finalChannelURL)
    return duplicateCheck