""""
Copyright (c) 2021 Daniel Mihai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from machine import Pin, PWM
from machine import ADC
import utime
import tm1637

global avss, maxss, minss
global lstplen, lstwper, lststy, lstfrq
global plen, wper, sty, frq
global focusplen, focuswper, focussty, focusfrq

focusplen=7
focuswper=4
focussty=3
focusfrq=3

lstplen=[50, 75, 100, 150, 200, 250, 300, 350, 400, 500]
lstwper=[20, 30, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300]
lststy=[0, 50, 100, 150, 200, 250, 300, 350, 400, 500, 700]
lstfrq=[20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160]

plen=lstplen[focusplen]
wper=lstwper[focuswper]
sty=lststy[focussty]
frq=lstfrq[focusfrq]

rd=machine.ADC(1) 
tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))
tm.brightness(0)

tm.show("----") 
impuls=Pin(16, Pin.OUT)
buzzer=PWM(Pin(15))

btplen = Pin(10, Pin.IN, Pin.PULL_UP)
btwper = Pin(11, Pin.IN, Pin.PULL_UP)
btsty = Pin(12, Pin.IN, Pin.PULL_UP)
btop = Pin(13, Pin.IN, Pin.PULL_UP)
bfrq= Pin(9, Pin.IN, Pin.PULL_UP)

while True:
    if not bfrq.value():
        if focusfrq == 11:
            focusfrq=-1
        focusfrq=focusfrq+1
        frq=lstfrq[focusfrq]
        tm.number(frq)
        utime.sleep_ms(500)
    if not btplen.value():
        if focusplen == 9:
            focusplen=-1
        focusplen=focusplen+1
        plen=lstplen[focusplen]
        tm.number(plen)
        utime.sleep_ms(500)
    if not btwper.value():
        if focuswper == 12:
            focuswper=-1
        focuswper=focuswper+1
        wper=lstwper[focuswper]
        tm.number(wper)
        utime.sleep_ms(500)
    if not btsty.value():
        if focussty == 10:
            focussty=-1
        focussty=focussty+1
        sty=lststy[focussty]
        tm.number(sty)
        utime.sleep_ms(500)
    if not btop.value():
        plen=lstplen[focusplen]
        wper=lstwper[focuswper]
        sty=lststy[focussty]
        frq=lstfrq[focusfrq]
        tm.show("SCAL")
        buzzer.freq(1000)
        buzzer.duty_u16(1000)
        utime.sleep_us(500000)
        buzzer.duty_u16(0)
        lstcal=[]
        for i in range (0,6):
            impuls.value(1)
            utime.sleep_us(plen)
            impuls.value(0)
            utime.sleep_us(wper)
            vadcal=rd.read_u16()
            lstcal.append(vadcal)
            utime.sleep_us(frq*1000)
        avss=round(sum(lstcal)/len(lstcal))
        maxss= max(lstcal)+sty
        minss= min(lstcal)-sty
        utime.sleep_us(200000)
        buzzer.freq(600)
        buzzer.duty_u16(1000)
        utime.sleep_us(500000)
        buzzer.duty_u16(0)
        tm.show("ECAL")
        utime.sleep_us(1000000)
        while True:
            impuls.value(1)
            utime.sleep_us(plen)
            impuls.value(0)
            utime.sleep_us(wper)
            vadc=rd.read_u16()
            if (vadc <= minss) or (vadc>=maxss):
                buzzer.duty_u16(1000)
                utime.sleep_us(frq*1000)
            else:
                utime.sleep_us(frq*1000)
            buzzer.duty_u16(0)
            dif=minss-vadc
            if dif<=0:
                dif=0
            tm.number(round(dif/100))        
            

