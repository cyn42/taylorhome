import wcclient_config as config
import network
import socket
    
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.WIFI['ssid'], config.WIFI['password'])
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def is_connected():
    return network.WLAN(network.STA_IF).isconnected()

def http_get(url,port):
    _, _, host, path = url.split('/', 3)
    print('Host: ',host,'Path:',path)
    addr = socket.getaddrinfo(host, int(port))[0][-1]
    print(addr)
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    response = ''
    s.readline()
    s.readline()
    s.readline()
    s.readline()
    s.readline()
    while True:
        data = s.recv(100)
        if data:
            response += str(data, 'utf8')
        else:
            break
    s.close()
    del s
    return response