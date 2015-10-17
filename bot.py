import sys
import socket
import string
import urllib2
import re
import time
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

##############
#   CONFIG   #
##############

host = 'irc.freenode.net'
chan = '#twt2irc-bottest'

nick = 'twt2irc-bot'
realname = "twt2irc-bot"
passwd = 'twt2irc-bot'
port = 6667
owner = 'treetrunk'
tweeter_color = '10';
tweeters = [
  'youtube',
  'justinbieber',
  'katyperry',
  'barackobama',
  'twitter',
  'cnn',
  'wol_lay',
  'pix_xie',
  'foxnews'
]


print "  __         __    ___    _                 __        __ "
print " / /__    __/ /_  |_  |  (_)_______  ____  / /  ___  / /_"
print "/ __/ |/|/ / __/ / __/  / / __/ __/ /___/ / _ \/ _ \/ __/"
print "\__/|__,__/\__/ /____/ /_/_/  \__/       /_.__/\___/\__/ "
print ""
print "==========================================================="



# Connect to server and set nick
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((host, port))
irc.send("PASS %s \r\n" % passwd)
irc.send("NICK %s \r\n" % nick)
irc.send("USER %s %s %s :%s, owned by %s \r\n" % (nick, nick, nick, realname, owner))
irc.send("JOIN %s \r\n" % chan)


def print_tweet(tweets, old_tweets, tweeter):
  time.sleep(1)
  if tweeter in old_tweets:
    if old_tweets[tweeter] != tweets[tweeter]:
      irc.send("PRIVMSG %s : \x03%s@%s\x03 --- %s --- LINK: %s \r\n" % (
        chan,  
        tweeter_color,
        tweeter, 
        tweets[tweeter]['text'], 
        tweets[tweeter]['url']))
      print "%s >>> @%s --- %s --- LINK: %s \r\n" % (
        curr_time, 
        tweeter, 
        tweets[tweeter]['text'], 
        tweets[tweeter]['url'])
  old_tweets[tweeter] = tweets[tweeter]
  return old_tweets
    

def get_tweets(tweeters):
  
  tweets = {}
  stop = ""

  for tweeter in tweeters:
    
    page = urllib2.urlopen('https://twitter.com/'+ tweeter).read()
    if page.find("js-pinned") != -1:
      pinned = True
    else:
      pinned = False
    lines = page.split("\n")

    for line in lines:
      if stop != tweeter:
        if line.find('js-tweet-text tweet-text" lang="en" data-aria-label-part="0">') != -1:

          words = line.split()
          for word in words:
            if word.find('http://t.co/') != -1:
              url_text = word.split('"')
              url = url_text[1]

          no_html = re.compile(r'<[^>]+>')
          tweet = no_html.sub('', line)
          tweet = " ".join(tweet.split())
          tweets[tweeter] = {"text":tweet, "url":url}
          if pinned:
            pinned = False
          else: 
            stop = tweeter
    
  return tweets

old_tweets = {}

# Main loop
while True:
    
  curr_time = datetime.fromtimestamp(time.time()).strftime('%m/%d | %H:%M')
  
  data = irc.recv (4096)
  if data.find('PING') != -1:
    irc.send('PONG ' + data.split() [1] + '\r\n')

  tweets = get_tweets(tweeters)

  for tweeter in tweeters:
    old_tweets = print_tweet(tweets, old_tweets, tweeter)
    old_tweets[tweeter] = tweets[tweeter]
  
  if data.find('!previous') != -1:
      for tweeter in old_tweets:
        irc.send("PRIVMSG %s : \x03%s@%s\x03 --- %s --- LINK: %s \r\n" % (
          chan,  
          tweeter_color,
          tweeter, 
          old_tweets[tweeter]['text'], 
          old_tweets[tweeter]['url']))

