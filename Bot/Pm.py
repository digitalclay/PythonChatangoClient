###############################################
#PM Bot - Jon Rollins - J.p. - Digitalclay ####
#This code and all code posted is in no way ###
#to be takenn as serious. Thrown together #####
#in about an hour as an example of how  #######
#simple it can be to write a bot from scratch,#
#without using exsiting libraries.This code ###
#purposly didnt use classes ect. to keep code##
#to a bare minimum. ###########################
###############################################


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
import re


##################
## Variables #####

auid = ''
username = 'mizukebot'
password = 'password =/'
host = 'c1.chatango.com'
port = 5222;
link = "http://chatango.com/login"




####################
## Connect To Pms ##

def connect():
    
    params = urllib.parse.urlencode({
            'user_id':username,
            'password':password,
            'storecookie':'on',
            'checkerrors':'yes'
    }).encode()
    req = url.Request(link,params)
    resp = urllib.request.urlopen(req)
    print(resp)
    headers = resp.headers
    for header,value in headers.items():
        if header.lower() == "set-cookie":
            if value.startswith("auth.chatango.com="):
                a , b = value.split("=",1)
                d , c = b.split(";",1)
                auid = d 
    global sock            
    sock = socket.socket()  
    sock.connect((host,port))

    sendLogin("tlogin:" + auid +":2")

    Timer(20.0, ping).start()

    readThread = Thread(target = run)
    readThread.setDaemon(True)
    readThread.start()



###########################
## Read From Server Loop ##
def run():
  
    global running
    running = True

    while running:
        if(writeLock == True):
          print("[PM] Error : Can't read while writing to server!!! ")
          continue
        
        msg = str(sock.recv(4096).decode("utf-8"))
        
        try:
            if msg.startswith("msg:"):
              onMsgRcv(cleanMsg(msg))
              
            if msg.startswith("OK"):
              onConnectRcv()
              
            if msg.startswith("DENIED"):
              onConnectFailRcv()
              
            if msg.startswith("status:"):
              onStatusUpdateRcv(msg)
              
            if msg.startswith("idleupdate:"):
              onIdleUpdateRcv(msg)
              
            if msg.startswith("msgoff:"):
              onPmOfflineMsgRcv(msg)
              
            if msg.startswith("wl:"):
              onFriendListRcv(msg)
              
            if msg.startswith("wlonline:"):
              onFriendOnlineRcv(msg)
              
            if msg.startswith("wloffline:"):
              onFriendOfflineRcv(msg)
              
            if msg.startswith("block_list:"):
              onBlockListRCV(msg)
              
            if msg.startswith("kickingoff:"):
              onServerKickRcv(msg)

              
        except Exception:
            print(str(sys.exc_info()))
            pass


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
  sender=data[1]
  message=data[6]
  print("[PM] MSG ("+sender+") : "+message)
  checkCommands(sender,message)

#On Connect
def onConnectRcv():
  print("[PM] Connected to Pms ")
  if(running):
    sendWL()
    sendBlockList()

#Connect Fail
def onConnectFailRcv():
  running = False
  sock.close()
  sock = None

#Status Update
def onStatusUpdateRcv(msg):
  print("[PMS] Input : "+msg)

#Idle Update
def onIdleUpdateRcv(msg):
  print("[PMS] Input : "+msg)

#PM Offline Msg
def onPmOfflineMsgRcv(msg):
  print("[PMS] Input : "+msg)

#Friend List
def onFriendListRcv(msg):
  global friendList
  friendList = msg.split(":")[1:][0::4]
  print(friendList)

#Friend Online
def onFriendOnlineRcv(msg):
  print("[PMS] Input : "+msg)

#Friend Offline
def onFriendOfflineRcv(msg):
  print("[PMS] Input : "+msg)

#Block List
def onBlockListRCV(msg):
  global blockList
  blockList = msg.split(":")[1:]
  blockList[len(blockList)-1] = blockList[len(blockList)-1].split("\r")[0]
  print(blockList)

#Server Kick
def onServerKickRcv(msg):
  print("[PMS] Input : "+msg)



#########################
## Send To Server Cmds ##

#Send
def sendToServer(message , usePrint):
  global writeLock
  writeLock = True
  if(usePrint):
    print("[PMS] Output : "+str(message.encode()))
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
def sendLogin(login):
  sendToServer(login+"\x00" , True)

#Message
def sendMsg(name,msg):
  message = "msg:" + name + ":<n7/><m v=\"1\">" + msg + "</m>\r\n"
  sendToServer(message, True)
  
#Ping
def ping():
  sendToServer("\r\n", False)
  Timer(20.0, ping).start()


#Send for WL(Friend List)
def sendWL():
  sendToServer("wl\r\n", True)

#Get BlockList
def sendBlockList():
  sendToServer("getblock\r\n", True);

#Block User
def block(user):
  g = "block:"+user+"\r\n";
  sendToServer(g, True);

#Unblock User	
def unBlock(user):
  g = "unblock:"+user+"\r\n";
  sendToServer(g, True);

#Remove Friend
def removeFriend(user):
  g = "wldelete:"+user+"\r\n";
  sendToServer(g, True);

#Add Friend	
def addFriend(user):
  g = "wladd:"+user+"\r\n";
  sendToServer(g, True);




############################
## Check Bot Commands ######
def checkCommands(sender,message):
  #example pm commands
  if message.lower().startswith("hey"):
    sendMsg(sender, "Hello "+sender+", how is life? ^.^")
  if message.lower().startswith("blocks"):
    sendMsg(sender,str(blockList))
  if message.lower().startswith("friends"):
    sendMsg(sender,str(friendList))



#############
## Connect ##
connect()
