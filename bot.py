import sys
import socket
import string
from pattern.web import Twitter
import time

##############
#   CONFIG   #
##############

host = 'irc.freenode.net'
chan = '#twitterrealybottest'

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
irc.send("JOIN %s \r\n" % chan)


def get_tweets(irc):
    s = Twitter().stream('#fail')
    for i in range(10):
        time.sleep(3)
        s.update(bytes=1024)
        if s:
            tweets = s[-1].text
            tweets = tweets.encode('ascii', errors='ignore')
            return tweets

# Main loop
while True:
  

  data = irc.recv (4096)
  if data.find('PING') != -1:
    irc.send('PONG ' + data.split() [1] + '\r\n')
  print data

  tweet = get_tweets(irc)
  old_tweet = ""
  if tweet != old_tweet:
    old_tweet = tweet
    irc.send("PRIVMSG %s : %s \r\n" % (chan, old_tweet))
