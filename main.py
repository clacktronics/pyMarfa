import pyb, ure, os
from time import sleep
from pwm import ledpwm
from seq_reader import sequence


#=LED=Setup===============================================================================
#Each array of LEDs can have their own frequency bar P18 which is LED 3 Red which is fixed

RedF = 200
GreenF = 224
BlueF = 272

# This initialises all the pins by setting all the frequencies. The pwm Library makes sure
# the right commands go to the right pins. Note that most of the pins share each others
# clocks and 'P18' has a fixed frequency so setting the frequency has no effect but has to
# be there to not break the class assignment!

LED = {
0:{
  'R':ledpwm('Y8',12,2,RedF),
  'G':ledpwm('Y1',8,1,GreenF),
  'B':ledpwm('Y3',10,1,BlueF)
},
1:{
  'R':ledpwm('Y4',11,1,RedF),
  'G':ledpwm('Y6',1,1,GreenF), #inv
  'B':ledpwm('X9',4,1,BlueF)
},
2:{
  'R':ledpwm('Y7',12,1,RedF),
  'G':ledpwm('Y2',8,2,GreenF),
  'B':ledpwm('X10',4,2,BlueF)
},
3:{
  'R':ledpwm('P18',2,1,RedF),
  'G':ledpwm('Y12',1,3,GreenF),
  'B':ledpwm('X17',2,2,BlueF)
},
4:{
  'R':ledpwm('X2',5,2,RedF),
  'G':ledpwm('X3',9,1,GreenF),
  'B':ledpwm('Y10',2,4,BlueF)
},
5:{
  'R':ledpwm('X4',5,4,RedF),
  'G':ledpwm('X6',0,0,GreenF),
  'B':ledpwm('X8',14,1,BlueF)
},
6:{
  'R':ledpwm('X7',13,1,RedF),
  'G':ledpwm('X5',0,0,GreenF),
  'B':ledpwm('Y9',2,3,BlueF)
},
7:{
'R':ledpwm('X1',5,1,RedF),
'G':ledpwm('Y11',1,2,GreenF), #inv
'B':ledpwm('LED_YELLOW',2,1,BlueF) #inv
}
}




def clear():
  for led in LED:
    for pin in LED[led]:
      LED[led][pin].pwm(100)

clear()

def writeRG(stepstring):
    colors = ['R','G']

    for i, col in enumerate(colors):
        for n in range(8):
            val = int(stepstring[n+(i*8)]) # value is pin number plus color number * 8
            val *= 10
            if val == 90: val = 100
            val = 100 - val
            LED[n][col].pwm(val)

def writeB(stepstring):
    if len(stepstring) == 24:
        for i, n in enumerate(stepstring[16:]):
            val = int(n)
            val *= 10
            if val == 90: val = 100
            val = 100 - val
            dimmer.target[i] = val

class Bdimmer():
    def __init__(self):
        self.pinval = [100] * 8
        self.target = [100] * 8
        self.rate = [0] * 8
        self.timer = [pyb.micros()] * 8

    def poll(self):

        for i, pin in enumerate(self.pinval):

            if pyb.elapsed_micros(self.timer[i]) > self.rate[i]:
                if pin > self.target[i]:
                    self.pinval[i] -= 1
                elif pin < self.target[i]:
                    self.pinval[i] += 1

                LED[i]['B'].pwm(self.pinval[i])

                self.timer[i] = pyb.micros()

if __name__ == "__main__":


    onloop = False
    loopcount = 0
    loop = 0


    start = pyb.micros()
    dimmerst =  pyb.micros()
    seq = sequence()
    dimmer = Bdimmer()
    dimmer.rate = [5000, 5000, 5000, 5000, 5000 , 5000, 5000, 5000]
    i = 1

    while True:
      if i > seq.length: break

      if pyb.elapsed_micros(dimmerst) > 100:
          dimmer.poll()
          dimmerst =  pyb.micros()

      if pyb.elapsed_micros(start) >= 55700:

            step = seq.getStep(i).replace(' ','')[:-1]
            i += 1


            if step[:3] == "seq":
                print(loopcount, loop)

                if not onloop:
                    loopstart = i
                    onloop = True

                else:
                    i = loopstart
                    loopcount += 1
                    if loopcount == loop:
                        loopcount = 0
                        onloop = False

                continue

            elif step[:4] == "loop":
                loop = int(step[5:])
                continue

            else:
                #print(i,loop,sname,step)
                writeRG(step)
                writeB(step)
                start = pyb.micros()
