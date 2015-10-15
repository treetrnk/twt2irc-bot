import sys
import socket
import string
import HTMLParser
from pattern.web import Twitter
import time

##############
#   CONFIG   #
##############

host = 'irc.freenode.net'
chanlist = [
  '#twitterrealybottest'
  ]

nick = 'TwitterRelayBot'
realname = "Twitter Relay bot, owned by treetrunk"
passwd = 'twitterbot'
port = 6667
owner = 'treetrunk'

# Connect to server and set nick
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((host, port))
irc.send("PASS %s \r\n" % passwd)
irc.send("NICK %s \r\n" % nick)
irc.send("USER %s %s %s :%s \r\n" % (nick, nick, nick, realname))
for chan in chanlist:
  irc.send("JOIN %s \r\n" % chan)

h = HTMLParser.HTMLParser()

def get_tweets(irc):
    s = Twitter().stream('#fail')
    for i in range(10):
        time.sleep(3)
        s.update(bytes=1024)
        if s:
            tweets = h.unescape(s[-1].text)
            irc.send(tweets+"\r\n")

# Main loop
while True:
  

  data = irc.recv (4096)
  if data.find('PING') != -1:
    irc.send('PONG ' + data.split() [1] + '\r\n')
  print data

  get_tweets(irc)
