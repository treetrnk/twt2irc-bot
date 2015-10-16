import sys
import socket
import string
import urllib2
import re
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
tweeter = 'username'

# Connect to server and set nick
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((host, port))
irc.send("PASS %s \r\n" % passwd)
irc.send("NICK %s \r\n" % nick)
irc.send("USER %s %s %s :%s \r\n" % (nick, nick, nick, realname))
irc.send("JOIN %s \r\n" % chan)

def get_tweets(tweeter):
  
  time.sleep(5)
  page = urllib2.urlopen('https://twitter.com/'+ tweeter).read()
  lines = page.split("\n")
  tweets = []

  for line in lines:

    if line.find('<p class="TweetTextSize TweetTextSize--26px js-tweet-text tweet-text" lang="en" data-aria-label-part="0">') != -1:
      
      words = line.split()

      for word in words:
        if word.find('http://t.co/') != -1:
          url_text = word.split('"')
          url = url_text[1]

      no_html = re.compile(r'<[^>]+>')
      line = line.encode('ascii', errors='ignore')
      tweet = no_html.sub('', line)
      tweet = " ".join(tweet.split())
      tweets.append({"text":tweet, "url":url})
  
  return tweets

old_tweet = ""

# Main loop
while True:
  

  data = irc.recv (4096)
  if data.find('PING') != -1:
    irc.send('PONG ' + data.split() [1] + '\r\n')
  print data

  tweets = get_tweets(tweeter)
  if tweets[0]['text'] != old_tweet:
    old_tweet = tweets[0]['text']
    irc.send("PRIVMSG %s : *** Tweet from @%s *** %s -- LINK: %s \r\n" % (chan, tweeter, tweets[0]['text'], tweets[0]['url']))
    print "*** Tweet from @%s *** %s -- LINK: %s \r\n" % (tweeter, tweets[0]['text'], tweets[0]['url'])
