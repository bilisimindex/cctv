 xml'yi içe aktarın . ağaç . ET olarak ElementTree  
 işletim sistemini içe aktar

def  build ( username = "invalidusername" , password = "invalidpassword" ):
    yinelenenKontrol  = []
    ağaç  =  ET . ayrıştırma ( os . path . birleştirme ( os . path . dirname ( __file__ ), 'resources \\ Resources.xml ' ) )
    kök  =  ağaç . kök ()
    için  Üretici  içinde  kökü . iter ( "Üretici" ):
        için  URL'ye  de  Üretici :
            finalURL  =  ""

            # XML'de [AUTH] göstergesi olan hiçbir şeyi yoksay (şimdilik gerek yok ve PoC için kafa karıştırıcı)
            eğer  "[AUTH]"  in  URL'ye . öznitelik [ "url" ]:
                devam et
                
            eğer  URL . attrib [ "prefix" ] ==  "rtsp://" : # PoC için yalnızca RTSP kullanın - HTTP değil
                eğer  URL . öznitelik [ "url" ]. ile başlar ( "/" ):
                    finalURL  =  URL . öznitelik [ "url" ][ 1 :]
                başka :
                    finalURL  =  URL . nitelik [ "url" ]
                finalURL  =  finalURL . değiştir ( "[KULLANICI ADI]" , kullanıcı adı )
                finalURL  =  finalURL . değiştir ( "[ŞİFRE]" , şifre )
                
                # Alt tür herhangi bir fark yaratmayacak, bu nedenle olası kopyaları XML'den kaldırıyoruz
                finalURL  =  finalURL . değiştir ( "&subtype=00" , "" )
                finalURL  =  finalURL . değiştir ( "&subtype=01" , "" )
                finalURL  =  finalURL . değiştir ( "&subtype=02" , "" )
                finalURL  =  finalURL . değiştir ( "&subtype=0" , "" )
                finalURL  =  finalURL . değiştir ( "&subtype=1" , "" )
                finalURL  =  finalURL . değiştir ( "&subtype=2" , "" )

                eğer  "[KANAL]"  değil  de  Son URL :
                    eğer  Son URL  değil  de  duplicateCheck :
                        kopyalaKontrol . Ekleme ( Son URL )
                başka :
                    için  KanalNo  içinde  aralıkta ( 1 , 21 ): 20 kanal # Maks (muhtemelen bazı modellerde 1 olarak 10 çevirecek)
                        finalChannelURL  =  finalURL . değiştir ( "[KANAL]" , str ( kanalkimliği ))
                        eğer  finalChannelURL  değil  de  duplicateCheck :
                            kopyalaKontrol . Ekleme ( finalChannelURL )
    dönüş  duplicateCheck
