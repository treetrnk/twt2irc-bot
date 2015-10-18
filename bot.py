#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# twt2irc-bot
# Copyright (C) 2014, Nathan Hare <nhare330@gmail.com>,
#
# This file is part of twt2irc-bot.
#
# twt3irc-bot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# twt2irc-bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with twt2irc-bot.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributor(s):
#
# Nathan Hare <nhare330@gmail.com>
#
#
# bot.py Main program
#
"""Runs the bot.
"""
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
port = 6667

nick = 'twt2irc-bot'
passwd = 'twt2irc-bot'
realname = "twt2irc-bot"
owner = 'treetrunk'

tweeter_color = '11';
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

# End config

print "  __         __    ___    _                 __        __ "
print " / /__    __/ /_  |_  |  (_)_______  ____  / /  ___  / /_"
print "/ __/ |/|/ / __/ / __/  / / __/ __/ /___/ / _ \/ _ \/ __/"
print "\__/|__,__/\__/ /____/ /_/_/  \__/       /_.__/\___/\__/ "
print ""
print "========================================================="


# Connect to server and set nick
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((host, port))
irc.send("PASS %s \r\n" % passwd)
irc.send("NICK %s \r\n" % nick)
irc.send("USER %s %s %s :%s, owned by %s \r\n" % (nick, nick, nick, realname, owner))
irc.send("JOIN %s \r\n" % chan)
irc.send("MSG nickserv %s %s" % (nick, passwd))


# Print individual tweets to console and IRC
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
    

# Scrape twitter.com/tweeter and strip down html to find tweets.
# Then package them up to be posted.
def get_tweets(tweeters):
  
  tweets = {}
  stop = ""

  for tweeter in tweeters:
    
    # Grab twitter page
    page = urllib2.urlopen('https://twitter.com/'+ tweeter).read()
    if page.find("js-pinned") != -1:
      pinned = True
    else:
      pinned = False
    lines = page.split("\n")

    # Find tweets
    for line in lines:
      if stop != tweeter:
        if line.find('js-tweet-text tweet-text" lang="en" data-aria-label-part="0">') != -1:

          # Find URL to specific tweet
          words = line.split()
          for word in words:
            if word.find('http://t.co/') != -1:
              url_text = word.split('"')
              url = url_text[1]

          # Strip HTML tags
          no_html = re.compile(r'<[^>]+>')
          tweet = no_html.sub('', line)
          tweet = " ".join(tweet.split())

          tweets[tweeter] = {"text":tweet, "url":url}

          # if the user has any pinned tweets, repeat once
          if pinned:
            pinned = False
          else: 
            # Stop the looping for this tweeter once the first tweet is found
            stop = tweeter
    
  return tweets

# Create old tweets dictionary to hold the last tweets from each user
old_tweets = {}

# Main loop
while True:
    
  # Find the current time for timestamps
  curr_time = datetime.fromtimestamp(time.time()).strftime('%m/%d | %H:%M')
  
  # Talk to server if pinged
  data = irc.recv (4096)
  if data.find('PING') != -1:
    irc.send('PONG ' + data.split() [1] + '\r\n')
  print curr_time + " " + data

  # Get tweets from each user
  tweets = get_tweets(tweeters)

  # Print tweets if new and replace precious tweets
  for tweeter in tweeters:
    old_tweets = print_tweet(tweets, old_tweets, tweeter)
    old_tweets[tweeter] = tweets[tweeter]
  
  # !LAST TWEET cmd - Print previous tweets from each tweeter
  if data.find('!last tweet') != -1:
    for tweeter in old_tweets:
      irc.send("PRIVMSG %s : \x03%s@%s\x03 --- %s --- LINK: %s \r\n" % (
        chan,  
        tweeter_color,
        tweeter, 
        old_tweets[tweeter]['text'], 
        old_tweets[tweeter]['url']))

