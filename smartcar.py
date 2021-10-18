import bluetooth
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

motor_R_f=6;  
motor_R_r=7;
motor_L_f=4;
motor_L_r=5;

GPIO.setup(motor_R_f, GPIO.OUT)
GPIO.setup(motor_R_r, GPIO.OUT)
GPIO.setup(motor_L_f, GPIO.OUT)
GPIO.setup(motor_L_r, GPIO.OUT)

trig_f=8;
echo_f=9;

GPIO.setup(trig_f, GPIO.OUT)
GPIO.setup(echo_f, GPIO.IN)

trig_r=10;
echo_r=11;

GPIO.setup(trig_r, GPIO.OUT)
GPIO.setup(echo_r, GPIO.IN)

server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM ) 
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
 
client_socket,address = server_socket.accept()



def distance_f():
    # set Trigger to HIGH
    GPIO.output(trig_f, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trig_f, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo_f) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo_f) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    if distance<20:
        stop()
    time.sleep(0.001)
 
    

def distance_r():
    # set Trigger to HIGH
    GPIO.output(trig_r, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trig_r, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo_r) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo_r) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    
    distance = (TimeElapsed * 34300) / 2
 
    if distance<20:
        stop()
    time.sleep(0.001)
 

def forward():
    GPIO.output(motor_R_f, GPIO.HIGH)
    GPIO.output(motor_R_r, GPIO.LOW)
    GPIO.output(motor_L_f, GPIO.HIGH)
    GPIO.output(motor_L_r, GPIO.LOW)
    flag=0

def backward():
    GPIO.output(motor_R_f, GPIO.LOW)
    GPIO.output(motor_R_r, GPIO.HIGH)
    GPIO.output(motor_L_f, GPIO.LOW)
    GPIO.output(motor_L_r, GPIO.HIGH)
    flag=1

def right():
    GPIO.output(motor_R_f, GPIO.LOW)
    GPIO.output(motor_R_r, GPIO.LOW)
    GPIO.output(motor_L_f, GPIO.HIGH)
    GPIO.output(motor_L_r, GPIO.LOW)

def left():
    GPIO.output(motor_R_f, GPIO.HIGH)
    GPIO.output(motor_R_r, GPIO.LOW)
    GPIO.output(motor_L_f, GPIO.LOW)
    GPIO.output(motor_L_r, GPIO.LOW)

def stop():
    GPIO.output(motor_R_f, GPIO.LOW)
    GPIO.output(motor_R_r, GPIO.LOW)
    GPIO.output(motor_L_f, GPIO.LOW)
    GPIO.output(motor_L_r, GPIO.LOW)

while 1:
        
         data= client_socket.recv(1024)
         print "Received: %s" % data
         if (data == "F"):    
            forward()
         elif (data == "L"):    
            left()
         elif (data == "R"):    
            right()
         elif (data == "B"):    
            backward()
         elif data == "S":
            stop()


        if flag==0:
            distance_f()
        else if flag==1:
            distance_r()

client_socket.close()
server_socket.close()
