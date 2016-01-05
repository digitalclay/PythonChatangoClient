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


##################
## Variables #####

auid = ''
username = 'Mizukebot'
password = ''
host = 'c1.chatango.com'
port = 5222;
link = "http://chatango.com/login"
friendList = set()
blockList = set()



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

        msg = str(sock.recv(1024).decode("utf-8"))
        
        try:
            if msg.startswith("msg:"):
              onMsgRcv(msg)
              
            if msg.startswith("OK"):
              onConnectRcv()
              print("[PMS] Input : "+msg)
              
            if msg.startswith("DENIED"):
              onConnectFailRcv()
              print("[PMS] Input : "+msg)
              
            if msg.startswith("status:"):
              onStatusUpdateRcv(msg)
              print("[PMS] Input : "+msg)
              
            if msg.startswith("idleupdate:"):
              onIdleUpdateRcv(msg)
              print("[PMS] Input : "+msg)
              
            if msg.startswith("msgoff:"):
              onPmOfflineMsgRcv(msg)
              print("[PMS] Input : "+msg)
              
            if msg.startswith("wl:"):
              onFriendListRcv(msg)
              print("[PMS] Input : "+msg)
              
            if msg.startswith("wlonline:"):
              onFriendOnlineRcv(msg)
              print("[PMS] Input : "+msg)
              
            if msg.startswith("wloffline:"):
              onFriendOfflineRcv(msg)
              print("[PMS] Input : "+msg)
              
            if msg.startswith("block_list:"):
              onBlockListRCV(msg)
              print("[PMS] Input : "+msg)
              
            if msg.startswith("kickingoff:"):
              onServerKickRcv(msg)
              print("[PMS] Input : "+msg)
              
        except Exception:
            print(str(sys.exc_info()))
            continue


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
  pass

#Idle Update
def onIdleUpdateRcv(msg):
  pass

#PM Offline Msg
def onPmOfflineMsgRcv(msg):
  pass

#Friend List
def onFriendListRcv(msg):
  pass

#Friend Online
def onFriendOnlineRcv(msg):
  pass

#Friend Offline
def onFriendOfflineRcv(msg):
  pass

#Block List
def onBlockListRCV(msg):
  pass

#Server Kick
def onServerKickRcv(msg):
  pass



#########################
## Send To Server Cmds ##

#Send
def sendToServer(message , usePrint):
  if(usePrint):
    print("[PMS] Output : "+str(message.encode()))
  sock.send(str(message).encode())

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
  pass



#############
## Connect ##
connect()
