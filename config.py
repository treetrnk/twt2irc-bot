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
# config.py Configuration for the bot
# 
"""Configures the bot
"""

# Connection Settings
host = 'irc.freenode.net'
chan = '#twt2irc-bottest'
port = 6667

# Bot Settings
nick = 'twt2irc-bot'  # Don't forget to register your nick first
passwd = 'twt2irc-bot'
realname = "twt2irc-bot"
owner = 'treetrunk'

# Twitter Settings
tweeter_color = '11' # https://github.com/treetrunk/twt2irc-bot/wiki/IRC-Colors
tweeters = [         # All twitter accounts to be tracked
  'youtube',
  'justinbieber',
  'katyperry',
  'twitter',
  'cnn',
  'foxnews'
]
