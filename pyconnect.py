#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import serial
import time

"""
Program to connect to a Froeling FHG-3000 log wood gasification 
boiler (or any other Froeling boiler with Lambatronic 3100 control)
"""

#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
ser.port = "/dev/rfcomm0"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 0             #non-block read
#ser.xonxoff = False     #disable software flow control
#ser.rtscts = False     #disable hardware (RTS/CTS) flow control
#ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
#ser.writeTimeout = 200     #timeout for write

# Data for Lambdatronic
sOpenPort = "\x52\x61\x03\x00\xFF\xF9\x02\xAE"
sOutValues = "\x4D\x41\x01\x01\x00\x90"

# Define output variables of Lambdatronic
sZustand = ""
iRestO2 = 0
iKesselTemp = 0
iAbgasTemp = 0
iAbgasSw = 0
iKesselStellgr = 0
iSaugzug = 0
iPrimLuft = 0
iPrimKlPos = 0
iSekLuft = 0
iSekKlPos = 0
iPufferTempOb = 0
iPufferTempUn = 0
iBoilertemp = 0
iOelkessel = 0
iAussentemp = 0
iVorlauftemp1Sw = 0
iVorlauftemp1 = 0
x = ""
y = ""
iLaufzeit = 0
sFeuererhalt = ""
iBoardTemp = 0

# Define array for storing Lambdatronic values
aLambdatronicValues = {
    "Kesselzustand": sZustand,
    "Rest O2": iRestO2,
    "Kesseltemperatur": iKesselTemp,
    "Abgastemperatur": iAbgasTemp,
    "Abgastemperatur Sollwert": iAbgasSw,
    "Kesselstellgroesse": iKesselStellgr,
    "Saugzug": iSaugzug,
    "Primaerzuluft": iPrimLuft,
    "Primaerklappenposition": iPrimKlPos,
    "Sekundaerzuluft": iSekLuft,
    "Sekundaerklappenposition": iSekKlPos,
    "Puffertemperatur oben": iPufferTempOb,
    "Puffertemperatur unten": iPufferTempUn,
    "Boilertemperatur": iBoilertemp,
    "Oelkessektemperatur": iOelkessel,
    "Aussentemperatur": iAussentemp,
    "Vorlauftemperatur 1 Sollwert": iVorlauftemp1Sw,
    "Vorlauftemperatur 1": iVorlauftemp1,
    "Laufzeit Kessel": iLaufzeit,
    "Feuererhaltung": sFeuererhalt,
    "Boardtemperatur Lambdatronic": iBoardTemp
}

# Open connection to serial port	
def openSerialPort():
    try:

        ser.open()

    except Exception as e:

        print("Error open serial port: " + str(e))

        exit()


# Close connection to serial port		
def closeSerialPort():
    try:

        if ser.isOpen():
            ser.close()

    except Exception as e:

        print("Port alread closed: " + str(e))

# Write values to serial port
def writeToSerialPort(sCommand):
    if ser.isOpen():

        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output
            #and discard all that is in buffer


            #write data
            ser.write(sCommand)

            time.sleep(0.5)  #give the serial port sometime to receive the data

            response = ser.readline() #read() #readline()

            return response
            #print("read data: " + response)
            #print("Response length: " + str(len(response)))



        except Exception as e:

                print("Error communicating...: " + str(e))

    else:

        print("cannot open serial port")


# Add checksum to command
def getCheckSum(sCommand):
	
	b = 0
	
	# Loop checksum and get numbers for ASCII characters of checksum
	i = 0
	while True:
		b += ord(sCommand[i:i+1])
		
		i += 1
        
		if i <= len(sCommand):
			break

        sChkSum = chr(int(b / 256)) + chr(int(b % 256))

        return sChkSum


def tryCheckSum(sChecksum):

    bState = False

    if len(sChecksum) < 2:
        bState = False
    #elif
    if sChecksum[len(sChecksum)-2:2] == getCheckSum(sChecksum[0:len(sChecksum)-2]):
        bState = True
    else:
        bState = False
    return bState


def getCommandString(sCommand, iPacket, aPacket):
	
	sCommandString = sCommand + chr(iPacket)
	
	i = 0
	while True:
		sCommandString = sCommandString + chr(aPacket[i])
		i += 1
      
		if i >= iPacket:
			break
			
	return sCommandString

def getAck(sCommand):
    sAck = sCommand[0:1] + sCommand[1:2] + chr(1) + chr(1)
    ack = sAck + getCheckSum(sAck)
    return ack
	
sTestINIT = "\x52\x62\x03\x00\x00\x01"
sTestINITfull = sTestINIT + getCheckSum(sTestINIT)
sTestLOG = "\x52\x62\x03\x00\x00\x00"

sTest2INIT = "\x52\x61\x03\x00\xFF\xF9\x02"
sTest2INITfull = sTest2INIT + getCheckSum(sTest2INIT)
##sTestChksum = addCheckSum("\x52\x62\x03\x00\x00\x00")
#print(makeCommandString("Ra", 3, [O0, \xFF, \xFF]))

# Open port
#openSerialPort()

# Open connection to Lambdatronic
#print(writeToSerialPort(sOpenPort))

# Get name of i values of Lambdatronic (i = 23, because of this amount of outgoing values)
"""
i = 1
while True:
    
	writeToSerialPort(sOutValues)#(sOutValues)
    
	i = i + 1
	if (i > 23):
        
		break
"""
# Close port
#closeSerialPort()

#print(sTestINITfull)

#openSerialPort()
#print(writeToSerialPort(sTestINITfull))
#for i in range(0, 5, 1):
#    output = writeToSerialPort(sTestINITfull)
#    print(output)
#sData = ""
#sData = getAck(getAck(sData))
#output = writeToSerialPort(sData)
#print(output)

#closeSerialPort()

ser.open()
ser.write(sTestINITfull)

bBlogSend = False

while True:

    sData = ""
    sSend = ""

    while True:
        # Read from port
        sData = ser.readline()
        print("Received: " + sData)
        if sData.find("Ra") != -1 or sData.find("Rb") != -1:

            for i in range(0, int(len(sData))-1, 1):

                if tryCheckSum(sData[0:1]):

                    sData = sData[i:]
                    break

        if tryCheckSum(sData) is not True:
            break

    # Get date and time
    if sData[0:2] == "M2":

        dDateTime = ""

        # Code...

        if bBlogSend is False:

            sSend = getAck(sData) + getAck(sData)
            bBlogSend = True

        else:
            sSend = getAck(sData)

    else:
        sSend = getAck(sData)


    # Get data from Lambdatronic
    if sData[0:2] == "M1":

        # Get status
        iState = ord(sData[4:5])
        sState = ""

        if (iState == 0):
            sState = "Stoerung"
        elif (iState == 1):
            sState = "Brenner aus"
        elif (iState == 2 ):
            sState = "Anheizen"
        elif (iState == 3):
            sState = "Heizen"
        elif (iState == 4):
            sState = "Feuerhaltung"
        elif (iState == 5):
            sState = "Feuer aus"
        elif (iState == 6):
            sState = "Tuer offen"
        else:
            sState = "Kein Status"
        print("Status: " + sState)
    # Kesseltemperatur
    iKesselTemp = sData[9:10]

    # Abgastemperatur
    iAbgasTemp = sData[11:12]

    ser.write(sSend)
    print("Send: " + sSend)


ser.close()
