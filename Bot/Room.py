###################
## Imports ########

import sys
if sys.version_info[0] > 2:
  import urllib.request as url
else:
  import urllib2 as url
import urllib.request 
import urllib.parse
import socket
from threading import Timer
from threading import Thread
import random

##################
## Variables #####

uid = ''
username = 'Mizukebot'
password = ''
host = ''
port = 5228;
roomName = "digitalmasterminds69"

sv10=110
sv12=116
w12=75
sv8=101
sv6=104
sv4=110
sv2=95
tsweights=[["5", w12], ["6", w12], ["7", w12], ["8", w12],
           ["16", w12], ["17", w12], ["18", w12], ["9", sv2],
           ["11", sv2], ["12", sv2], ["13", sv2], ["14", sv2],
           ["15", sv2], ["19", sv4], ["23", sv4], ["24", sv4],
           ["25", sv4], ["26", sv4], ["28", sv6], ["29", sv6],
           ["30", sv6], ["31", sv6], ["32", sv6], ["33", sv6],
           ["35", sv8], ["36", sv8], ["37", sv8], ["38", sv8],
           ["39", sv8], ["40", sv8], ["41", sv8], ["42", sv8],
           ["43", sv8], ["44", sv8], ["45", sv8], ["46", sv8],
           ["47", sv8], ["48", sv8], ["49", sv8], ["50", sv8],
           ["52", sv10], ["53", sv10], ["55", sv10], ["57", sv10],
           ["58", sv10], ["59", sv10], ["60", sv10], ["61", sv10],
           ["62", sv10], ["63", sv10], ["64", sv10], ["65", sv10],
           ["66", sv10], ["68", sv2], ["71", sv12], ["72", sv12],
           ["73", sv12], ["74", sv12], ["75", sv12], ["76", sv12],
           ["77", sv12], ["78", sv12], ["79", sv12], ["80", sv12],
           ["81", sv12], ["82", sv12], ["83", sv12], ["84", sv12]]


fontFace = "Adobe Garamond Pro";
fontSize = "14";
fontColor = "000";
nameColor = "093";

####################
## Connect To Pms ##

def connect():

    uid = genUID()
    print(uid)
    
    host = getServerId(roomName)
    print(host)
    
    global sock            
    sock = socket.socket()  
    sock.connect((host,port))

    sendLogin()

    Timer(20.0, ping).start()

    readThread = Thread(target = run)
    readThread.setDaemon(True)
    readThread.start()



##############################
##generate 16 digit user id##
def genUID():
    nid = "";
    while len(nid) < 16:
      nid += str(random.randint(0,10));
    return nid;


#############################
##Get server ID##############
def getServerId(name):
    name = name.replace("_", "q").replace("-", "q")
    
    mins = min(5, len(name))
    substr = name[0:mins]
    hexInt = int(substr,36)
    frontN = float(hexInt)
    
    lastN=1000
    if len(name)>6:
      
      mins2 = min(3, len(name) - 5 )
      substr2 = name[6: 6 + mins2]
      hexInt2 = int(substr2, 36)
      lastN = max(hexInt2,1000)
      
    num = (frontN % lastN) / lastN
    maxNum = 0
    for wgt in tsweights:
      maxNum += wgt[1]
    print(maxNum)
    sumfreq = 0
    servNum = 0
    for wgt in tsweights:
      sumfreq += float(wgt[1]) / maxNum
      if(num <= sumfreq):
        servNum = int(wgt[0])
        break
    server="s"+str(servNum)+".chatango.com"
    return server
        
###########################
## Read From Server Loop ##
def run():
  
    global running
    running = True

    while running:

        msg = str(sock.recv(1024).decode("utf-8"))
        
        try:
            if msg.startswith("b:"):
              onMsgRcv(msg)
              #print("[Room] Input : "+msg)
            if msg.startswith("ok:"):
              onConnectRcv()
              print("[Room] Input : "+msg)
              
            if msg.startswith("denied"):
              onConnectFailRcv()
              print("[Room] Input : "+msg)
              
            if msg.startswith("inited"):
              onInitRCV(msg)
              print("[Room] Input : "+msg)
              
            if msg.startswith("n:"):
              onCountRcv(msg)
              print("[Room] Input : "+msg)
              
            if msg.startswith("mods:"):
              onModsRcv(msg)
              print("[Room] Input : "+msg)
              
            if msg.startswith("participant:0"):
              onLeaveRcv(msg)
              print("[Room] Input : "+msg)
              
            if msg.startswith("participant:1"):
              onJoinRcv(msg)
              print("[Room] Input : "+msg)
              
            if msg.startswith("g_participants:"):
              onRoomNamesRcv(msg)
              print("[Room] Input : "+msg)
              
            if msg.startswith("blocked:"):
              onBanRcv(msg)
              print("[Room] Input : "+msg)
              
            if msg.startswith("unblocked:"):
              onUnbanRcv(msg)
              print("[Room] Input : "+msg)

            if msg.startswith("i:"):
              onPastMsgRcv(msg)
              print("[Room] Input : "+msg)

            if msg.startswith("blocklist:"):
              onBlocklistRcv(msg)
              print("[Room] Input : "+msg)

            if msg.startswith("delete:"):
              onMsgDeleteRcv(msg)
              print("[Room] Input : "+msg)

            if msg.startswith("show_fw:"):
              onFloodWarningRcv(msg)
              print("[Room] Input : "+msg)

            if msg.startswith("show_tb:"):
              onFloodBanRcv(msg)
              print("[Room] Input : "+msg)

            if msg.startswith("tb:"):
              onFloodBanRepeatRcv(msg)
              print("[Room] Input : "+msg)

            if msg.startswith("premium:"):
              onPremiumRcv(msg)
              print("[Room] Input : "+msg)

            if msg.startswith("deleteall:"):
              onAllMsgDeleteRcv(msg)
              print("[Room] Input : "+msg)
              
        except Exception:
            print(str(sys.exc_info()))
            continue


##############################
## Recieve Cmds From Server ##

#Msg
def onMsgRcv(msg):
  data = msg.split(":")
  sender=data[2]
  message=data[len(data)-1]
  print("[Room] MSG ("+sender+") : "+message)
  checkCommands(sender,message)

#On Connect
def onConnectRcv():
  sendMsg("Login Successful ^.^")


#Connect Fail
def onConnectFailRcv():
  running = False
  sock.close()
  sock = None

def onInitRcv(msg):
  pass

def onCountRcv(msg):
  pass

def onModsRcv(msg):
  pass

def onLeaveRcv(msg):
  pass

def onJoinRcv(msg):
  pass

def onRoomNamesRcv(msg):
  pass

def onBanRcv(msg):
  pass


def onUnbanRcv(msg):
  pass


def onPastMsgRcv(msg):
  pass

def onBlocklistRcv(msg):
  pass

def onMsgDeleteRcv(msg):
  pass

def onFloodWarningRcv(msg):
  pass

def onFloodBanRcv(msg):
  pass

def onFloodBanRepeatRcv(msg):
  pass

def onPremiumRcv(msg):
  pass

def onAllMsgDeleteRcv(msg):
  pass



#########################
## Send To Server Cmds ##

#Send
def sendToServer(message , usePrint):
  if(usePrint):
    print("[Room] Output : "+str(message.encode()))
  sock.send(str(message).encode())

#Login
def sendLogin():
  sendToServer("bauth:"+roomName+":"+ uid+":"+ username+":"+ password+"\x00" , True)

#Message
def sendMsg(msg):
  message = "bmsg:tl2r:"+"<n"+nameColor+"/><f x"+fontSize+fontColor+"=\""+fontFace+"\">"+msg+"\r\n"
  sendToServer(message, True)
  
#Ping
def ping():
  sendToServer("\r\n", False)
  Timer(20.0, ping).start()







############################
## Check Bot Commands ######
def checkCommands(sender,message):
  pass



#############
## Connect ##
connect()
