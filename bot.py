import sys
import socket
import string
import logging

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

# Main loop
while True:
  

  data = irc.recv (4096)
  if data.find('PING') != -1:
    irc.send('PONG ' + data.split() [1] + '\r\n')
  print data
