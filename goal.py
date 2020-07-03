import RPi.GPIO as GPIO
import pygame
import time
import socket
import _thread


file = "goal.mp3"
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 7
GPIO_ECHO = 12
WIN_SCORE = 3
bind_ip = "172.20.10.8"
bind_port = 8888


GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(2)
print("Listening on %s:%d" % (bind_ip, bind_port))
client, addr = server.accept()
print("1")
client2, addr2 = server.accept()
print("2")
seg = (24, 23, 18, 15, 17, 22, 3, 27)

digits = {
    '.': (0, 0, 0, 0, 0, 0, 0, 0),
    '0': (1, 1, 1, 0, 1, 1, 1, 1),
    '1': (1, 0, 0, 0, 1, 0, 0, 1),
    '2': (1, 1, 0, 1, 0, 1, 1, 1),
    '3': (1, 1, 0, 1, 1, 1, 0, 1),
    '4': (1, 0, 1, 1, 1, 0, 0, 1),
    '5': (0, 1, 1, 1, 1, 1, 0, 1),
    '6': (0, 1, 1, 1, 1, 1, 1, 1),
    '7': (1, 1, 0, 0, 1, 0, 0, 1),
    '8': (1, 1, 1, 1, 1, 1, 1, 1),
    '9': (1, 1, 1, 1, 1, 1, 0, 1)

}

Blink = {
    
    '0': (0, 0, 0, 0, 0, 0, 1, 0),
    '1': (0, 0, 0, 0, 0, 1, 0, 0),
    '2': (0, 0, 0, 0, 1, 0, 0, 0),
    '3': (0, 0, 0, 1, 0, 0, 0, 0),
    '4': (0, 0, 1, 0, 0, 0, 0, 0),
    '5': (0, 1, 0, 0, 0, 0, 0, 0),
    '6': (1, 0, 0, 0, 0, 0, 0, 0)
    
    }



def send_trigger_pulse():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    

StartTime = time.time()
StopTime = time.time()
def distance(speed):
    global StartTime
    global StopTime
    send_trigger_pulse()
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime =time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * speed) / 2
        
    return distance
 
def Display(n):
    for n in range(0, 8):
        GPIO.output (seg[n], digits[str(9 - c % 10)][n])
def Clear():
    for n in range(0, 8):
        GPIO.output (seg[n], digits["."][n])
        
scoreA = -1
        
if __name__ == '__main__':
    try:
        for n in range(0, 8):
            GPIO.setup(seg[n], GPIO.OUT)

        c = 10
        Display(c)
        while True:
            dist = distance(34780)
            print("Measured Distance = %.1f cm" % dist)
            if dist < 26  or (dist > 32 and dist < 500):
                scoreA = scoreA + 1
                client.send((str(scoreA)+"\n").encode('utf-8'))
                client2.send((str(scoreA)+"\n").encode('utf-8'))
                c -= 1
                Clear()
                Display(c)
                print("Goal")
                if scoreA >0:
                    pygame.mixer.music.play(1)
                
                
                for i in range(7):
                    for n in range(0, 8):
                        GPIO.output (seg[n], Blink[str(6 - i % 10)][n])
                    time.sleep(1)
                if (9-c) >= 3:
                    print("win!")
                Display(c)
                time.sleep(5)
                if (9-c) >= 3:
                    c=9
                    scoreA = 0
                    client.send((str(scoreA)+"\n").encode('utf-8'))
                    client2.send((str(scoreA)+"\n").encode('utf-8'))
                Display(c)
                
            time.sleep(0.8)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
