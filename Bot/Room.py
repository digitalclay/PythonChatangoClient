###############################################
#Room Bot - Jon Rollins - J.p. - Digitalclay ####
#This code and all code posted is in no way ###
#to be takenn as serious. Thrown together #####
#in about an hour as an example of how  #######
#simple it can be to write a bot from scratch,#
#without using exsiting libraries.This code ###
#purposly didnt use classes ect. to keep code##
#to a bare minimum. ###########################
###############################################
# mizukebot #

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
import re

##################
## Variables #####

uid = ''
username = 'mizukebot'
password = 'password-_____________-'
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
    
    global quiet
    quiet = False
    
    while running:
      
        if(writeLock == True):
          print("[Room] Error : Can't read while writing to server!!! ")
          continue
        
        if(quiet == True):
          print("[Room] Quiet "+quiet)
          continue
        
        msg = str(sock.recv(1024).decode("utf-8"))
        
        try:
            if msg.startswith("b:"):
              onMsgRcv(cleanMsg(msg))

            if msg.startswith("ok:"):
              onConnectRcv(msg)
              
            if msg.startswith("denied"):
              onConnectFailRcv()
              
            if "inited" in msg:
              onInitRcv(msg)
              
            if msg.startswith("n:"):
              onCountRcv(msg)
              
            if msg.startswith("mods:"):
              onModsRcv(msg)
              
            if msg.startswith("participant:0"):
              onLeaveRcv(msg)
              
            if msg.startswith("participant:1"):
              onJoinRcv(msg)
              
            if msg.startswith("g_participants:"):
              onRoomNamesRcv(msg)
              
            if msg.startswith("blocked:"):
              onBanRcv(msg)
              
            if msg.startswith("unblocked:"):
              onUnbanRcv(msg)

            if msg.startswith("i:"):
              onPastMsgRcv(msg)

            if msg.startswith("blocklist:"):
              onBlocklistRcv(msg)

            if msg.startswith("delete:"):
              onMsgDeleteRcv(msg)

            if msg.startswith("show_fw:"):
              onFloodWarningRcv(msg)

            if msg.startswith("show_tb:"):
              onFloodBanRcv(msg)

            if msg.startswith("tb:"):
              onFloodBanRepeatRcv(msg)

            if msg.startswith("premium:"):
              onPremiumRcv(msg)

            if msg.startswith("deleteall:"):
              onAllMsgDeleteRcv(msg)

        except Exception:
            print(str(sys.exc_info()))
            continue




############################
#Clean message from server##
def cleanMsg(msg):
  msg = re.sub("<.*?>", "", msg)
  msg = re.sub("â–“", "", msg)
  msg = re.sub("â–’", "", msg) 
  msg = msg.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&apos;", "'").replace("&amp;", "&")
  return msg





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
def onConnectRcv(msg):
  if ":" in msg:
    global owner
    owner = msg.split(":")[1]
    print("[Room] Owner : "+owner)
  else:
    return
  if "M:" not in msg:
    onLoginFail()
    return
  global mods
  mods = []
  msgArray = msg.split("M:")  
  msgArray2 = msgArray[1].split(":")
  msgArray3 = msgArray2[3].split(";")
  m = 0
  for mod in msgArray3:
    mods.append(msgArray3[m].split(",")[0])
    m += 1 
  print("[Room] Mods : "+str(mods))
  sendMsg("Login Successful ^.^")


#login fail
def onLoginFail():
  print("[Room] Error : Failed to login")


#Connect Fail
def onConnectFailRcv():
  print("[Room] Error : Connnect Failled : "+msg)
  running = False
  sock.close()
  sock = None


#init
def onInitRcv(msg):
  getPremium()
  getRoomUsers()
  getBlockList()

#Room count
def onCountRcv(msg):
  global count
  count = msg.split("n:")[1]
  print("[Room] Count : "+str(count))

#mod add or remove
def onModsRcv(msg):
  msg = msg.replace("mods:", "")
  if ":" not in msg:
    return
  msgParts = msg.split(":")
  newMods = []
  m = 0
  for mod in msgParts:
    newMods.append(msgParts[m].split(",")[0])
    m += 1
  global mods
  if len(mods) > len(newMods):
    mods = newMods
    print("[Room] Mod removed :"+str(mods))
  if len(mods) < len(newMods):
    mods = newMods
    print("[Room] Mod Added :"+str(mods))


#user leaves chat
def onLeaveRcv(msg):
  user = msg.split(":")[4]
  global users
  users.append(user)
  print("[Room] User left Chat : "+user)


#user joins chat
def onJoinRcv(msg):
  user = msg.split(":")[4]
  global users
  users.append(user)
  print("[Room] User Joined Chat : "+user)


#on user names rcv
def onRoomNamesRcv(msg):
  msg = msg.replace("g_participants:","")
  parts = msg.split(";")
  u = 0
  global users
  users = []
  for user in parts:
    users.append(parts[u].split(":")[3])
    u += 1
  print("[Room] Users : "+str(users))


#blocklist 
def onBlocklistRcv(msg):
  msg = msg.replace("blocklist:","")
  global banList
  banList = []
  if ";" not in msg and ":" not in msg:
    print("[Room] BanList : "+str(banList))
    return
  parts = msg.split(";")
  b = 0
  for ban in parts:
    banList.append(parts[b].split(":")[2])
    b += 1
  print("[Room] BanList : "+str(banList))


#on ban
def onBanRcv(msg):
  banned = msg.split(":")[3]
  banner = msg.split(":")[4]
  banList.append(banned)
  print("[Room] Ban : "+banned+" By mod : "+banner)

#on unban
def onUnbanRcv(msg):
  banned = msg.split(":")[3]
  banner = msg.split(":")[4]
  banList.remove(banned)
  print("[Room] UnBan : "+banned+" By mod : "+banner)

#past msgs **unused**
def onPastMsgRcv(msg):
  pass

#msg deleted
def onMsgDeleteRcv(msg):
  print("[Room] Messages deleted"+msg)
  

#flood warning
def onFloodWarningRcv(msg):
  print("[Room] Flood Warning!!!")
  if quiet == False:
    setQuiet(True)
    Timer(30.0, setQuiet(False)).start()
  
#flood Ban
def onFloodBanRcv(msg):
  print("[Room] Flood Banned!!!")

#flood ban repeat
def onFloodBanRepeatRcv(msg):
  print("[Room] Flood Ban Repeat!!!")

#set quiet
def setQuiet(mode):
  global quiet
  quiet = mode

#on premium rcv
def onPremiumRcv(msg):
  if "200" in msg:
    print("[Room] Premium available")
    setBG()
    setMedia()
  if "111" in msg:
    print("[Room] Premium not available")
    return

#on all msg deleted
def onAllMsgDeleteRcv(msg):
  print("[Room] All messages deleted")



#########################
## Send To Server Cmds ##

#Send
def sendToServer(message , usePrint):
  global writeLock
  writeLock = True
  if(usePrint):
    print("[Room] Output : "+str(message.encode()))
  try:
    checkDone = sock.sendall(str(message).encode())
    while(checkDone != None):
      continue
    writeLock = False
  except Exception:
    print("error in write")
    writeLock = False
    return


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

#get room users
def getRoomUsers():
  sendToServer("g_participants:start\r\n", True)

#get premium
def getPremium():
  sendToServer("getpremium:1\r\n", True)

# get bans
def getBlockList():
  sendToServer("blocklist:block::next:500\r\n", True)

#set bg
def setBG():
  sendToServer("msgbg:1\r\n",True)

#set video/audio recording
def setMedia():
  sendToServer("msgmedia:1\r\n",True)

#add mod
def addMod(name):
  sendToServer("addmod:"+name+"\r\n")

#remove mod
def removeMod(name):
  sendToServer("removemod:"+name+"\r\n")

#ban
def ban(userid,ip,name):
  sendToServer("block:"+userID+":"+ip+":"+name+"\r\n")

#unban  
def unBan(userid,ip,name):
  sendToServer("removeblock:"+userID+":"+ip+":"+name+"\r\n")

#delete msg
def deleteMsg(msgID):
  sendToServer("delmsg:"+msgID+"\r\n")

#delete all user msg  
def deleteUserAllMsg(userID):
  sendToServer("delallmsg:"+userID+"\r\n")

#flag
def flag(msgID):
  sendToServer("g_flag:"+msgID+"\r\n")

#clear chat
def clearAllMsg(name):
  sendToServer("clearall:\r\n")


############################
## Check Bot Commands ######
def checkCommands(sender,message):
  
  #example commannds
  if message.lower().startswith("-cmd"):
    sendMsg("My Example commands are  -mods , -count , -users , -bans , -quiet , -addmod , -removemod")
  
  if message.lower().startswith("-mods"):
    sendMsg("Owner - "+ owner + " Mods - " + str(mods))

  if message.lower().startswith("-count"):
    sendMsg("Room Count - "+str(count))

  if message.lower().startswith("-users"):
    sendMsg("Users - "+str(users))
    
  if message.lower().startswith("-bans"):
    sendMsg("Ban List - "+str(banList))
    
  if message.lower().startswith("-quiet"):
    if quiet == True :
      setQuiet(False)
    else:
      setQuiet(True)
    sendMsg("Quiet - "+quiet)

  if message.lower().startswith("-addmod") and username == owner:
    addMod(msg.split(" ")[1])
    
  if message.lower().startswith("-removemod") and username == owner:
    removeMod(msg.split(" ")[1])

#############
## Connect ##
connect()
