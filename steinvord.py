#!/usr/bin/python3.2

###
### steinvord.py
###


## SETUP

z_url = 'http://fqdn/zabbix/'
z_user = 'USER'
z_pass = 'PASS'

server = 'irc.example.com'
channel = '#example'
nick = 'steinvord'
botnick = 'Steinvord'
botuser = 'steinvord'

encoding = 'utf-8'
calibrate = 0


### begin
import sys, socket, time, re, datetime
from pyzabbix import ZabbixAPI
from difflib import Differ

trigprevlist = []
triglist = []
counter = 0

try:
    zapi = ZabbixAPI(z_url)
    zapi.session.timeout = 5
    zapi.login(z_user, z_pass)
except Exception as e:
    print(e)
    exit(3)
print ("Connected to Zabbix API Version %s" % zapi.api_version())

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print("Establishing connection to [%s]" % (server))
irc.connect((server, 6667))              #connects to the server
irc.setblocking(False)

sock_auth = "USER "+ botuser +" "+ botuser +" "+ botuser +" :This is the Steinvord bot!\n"
sock_nick = "NICK "+ botnick +"\n"
sock_nicksrv = "PRIVMSG nickserv :iNOOPE\r\n"
sock_join = "JOIN "+ channel +"\n"
irc.send(sock_auth.encode(encoding))
irc.send(sock_nick.encode(encoding))
irc.send(sock_nicksrv.encode(encoding))
irc.send(sock_join.encode(encoding))

def environment():
    currtemp = float(zapi.item.get(filter={'hostid': '10125', 'itemid': '26379'})[0]['lastvalue'])
    currhumid = calibrate + float(zapi.item.get(filter={'hostid': '10125', 'itemid': '26618'})[0]['lastvalue'])

    t_result = 't=' + str(currtemp) + '°C'
    if currtemp > 24:
        t_result += ' !! WARNING !!'
    t_result += ' h=' + str(currhumid) + '%'
    t_sock_result = 'PRIVMSG ' + channel + ' :' + t_result + '\n'
    irc.send(t_sock_result.encode(encoding))


while True:
    time.sleep(1)
    counter += 1

    if counter == 60:
        counter = 0
        ctime = datetime.datetime.now()
        if int(ctime.minute) == 20:
            environment() # print env data every 20 minutes

        triggers = zapi.trigger.get(only_true=1,
            skipDependent=1,
            monitored=1,
            active=1,
            output='extend',
            expandDescription=1,
            expandData='host',
            sortfield='triggerid'
        )
    
        for t in triggers:
            #print(t)
            if int(t['value']) == 1:
                triglist.append("{}".format(t['description'])
                #triglist.append("{0} - {1}".format(
                #    t['host'],
                #    t['description'],
                #    '')
                )
        
        for d in Differ().compare(trigprevlist, triglist):
            if re.match('^\+', d) is not None:
                sock_result = 'PRIVMSG ' + nick + " :" + d + '\n'
                irc.send(sock_result.encode(encoding))
            if re.match('^\-', d) is not None:            
                sock_result = 'PRIVMSG ' + nick + " :" + d + '\n'
                irc.send(sock_result.encode(encoding))
            time.sleep(1)
                
        trigprevlist = triglist
        triglist = []

    try:
        text=irc.recv(2040)  #receive the text
        decoded_text = text.decode(encoding)

        ### print (decoded_text)   #print text to console DEBUG

        if decoded_text.find('!ping') != -1:
            triggers = zapi.trigger.get(only_true=1,
                skipDependent=1,
                monitored=1,
                active=1,
                output='extend',
                expandDescription=1,
                expandData='host',
                sortfield='triggerid'
            )
            for t in triggers:
                if int(t['value']) == 1:
                    result = "{0} - {1} {2}".format(t['host'], t['description'], '')
                    sock_result = 'PRIVMSG ' + channel + " :" + result + '\n'
                    irc.send(sock_result.encode(encoding))
                    time.sleep(1)
        if decoded_text.find('!env') != -1:
            environment()

        # Prevent Timeout
        if decoded_text.find('PING') != -1:
            pingpong = 'PONG ' + decoded_text.split() [1] + '\r\n'
            irc.send(pingpong.encode(encoding))
    except Exception:
        continue

exit(0)

