import socket
import RPi.GPIO as gpio
import _thread
import time

portA = 2
portB = 13
portC = 3
portD = 26
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(portA, gpio.OUT)
gpio.setup(portB, gpio.OUT)
gpio.setup(portC, gpio.OUT)
gpio.setup(portD, gpio.OUT)
gpio.output(portA, False)
gpio.output(portB, False)
gpio.output(portC, False)
gpio.output(portD, False)

bind_ip = "172.20.10.4"
bind_port = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(2)
print("Listening on %s:%d" % (bind_ip, bind_port))
client, addr = server.accept()
scoreA = 0
scoreB = 0
data = ""

def controlCar():
    global data
    print("Acepted connection from: %s:%d" % (addr[0], addr[1]))
    while True:
        data = client.recv(1024)
        
        print(data)
        
def sendScoreToMonitor():
    global scoreA
    while True:
        scoreA = scoreA + 1
        client.sendall(bytes(scoreA))
        time.sleep(5)

try:
    _thread.start_new_thread(controlCar , ())
    _thread.start_new_thread(sendScoreToMonitor , ())
    while True:
        if data == 'q':
            break
        if data == b'go':
            gpio.output(portA, True)
            gpio.output(portB, False)
            gpio.output(portC, True)
            gpio.output(portD, False)
        elif data == b'stop':
            gpio.output(portA, False)
            gpio.output(portB, False)
            gpio.output(portC, False)
            gpio.output(portD, False)
        elif data == b'right':
            gpio.output(portA, False)
            gpio.output(portB, True)
            gpio.output(portC, True)
            gpio.output(portD, False)
        elif data == b'left':
            gpio.output(portA, True)
            gpio.output(portB, False)
            gpio.output(portC, False)
            gpio.output(portD, True)
        elif data == b'back':
            gpio.output(portA, False)
            gpio.output(portB, True)
            gpio.output(portC, False)
            gpio.output(portD, True)
        else:
            gpio.output(portA, False)
            gpio.output(portB, False)
            gpio.output(portC, False)
            gpio.output(portD, False)
        
except KeyboardInterrupt:
    gpio.output(portA, False)
    gpio.output(portB, False)
    gpio.output(portC, False)
    gpio.output(portD, False)
    client.close()
    gpio.cleanup()