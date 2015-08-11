#!/usr/bin/env python
import sys
import os
import time
from twitter import *
global our_name
our_name = "@makearhyme"


def chunks(string, chars):
  for start in range(0, len(string), chars):
    yield string[start:start + chars]


def send_dm(rhyme, screen_name):
  twitter.direct_messages.new(
      user=screen_name,
      text=rhyme)


def load_last_mention_id():
  f = open("last_id.log")
  return f.readline().strip()


def save_last_mention_id(id):
  mention_log = open("last_id.log", 'w')
  print(id, file=mention_log)
  mention_log.close()


def makearhyme(name, screen_name):
  ame = "b" + name[1:]
  n = name[0]
  name2 = "f" + ame[1:]
  ame2 = "m" + ame[1:]
  if n.lower() in ('b'):
    name2 = "f" + ame[1:]
    ame2 = "m" + ame[1:]
    ame = ame[1:]

  if n.lower() in ('m'):
    name2 = "f" + ame[1:]
    ame2 = ame[1:]

  if n.lower() in ('f'):
    name2 = ame[1:]
    ame2 = "m" + ame[1:]

  if n.lower() in ('a', 'e', 'o', 'u'):
    ame = "b" + name.lower()
    name2 = "f" + name.lower()
    ame2 = "m" + name.lower()

  rhyme = """@{screen_name} {name}, {name}, bo-{ame}
Banana-fana fo-{name2}
Fee-fi-mo-{ame2}
{name}!""".format(n=n, name2=name2, ame=ame, name=name, ame2=ame2, screen_name=screen_name)

  if len(rhyme) > 140:
    for chunk in chunks(rhyme, 140):
      send_dm(chunk, screen_name)
    rhyme = "@{screen_name} you requested {name} as a rhyme but it's too long for twitter. I DMed you!".format(
        name=name, screen_name=screen_name)
  return rhyme


def init_twitter():
  CONSUMER_KEY = "PLEASE"
  CONSUMER_SECRET = "CREATE"
  oauth_token = "YOUR"
  oauth_token_secret = "OWN"
  global twitter
  twitter = Twitter(auth=OAuth(
      oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET))


def get_tweets():
  kwargs = dict(count=200, include_rts=0, since_id=load_last_mention_id())
  try:
    mentions = list(reversed(twitter.statuses.mentions_timeline(**kwargs)))
  except:
    #   print('An exeception while getting the mentions')
    mentions = ""
  return mentions


def reply(text, screen_name):
  words = text.split()
  print
  for idx, word in enumerate(words):
    if word != our_name and idx == 0:
      return 0
    if word != our_name and word[1:] != "@":
      return makearhyme(str(word), screen_name)


def main():
  init_twitter()
  mentions = get_tweets()
  for idx, item in enumerate(mentions):
    status = reply(item['text'], item['user']['screen_name'])
    if status != 0:
      try:
        twitter.statuses.update(
            status=status, in_reply_to_status_id=item['id'])
        save_last_mention_id(item['id'])
      except:
        print("An exception while tweeting")
    time.sleep(10)

if __name__ == "__main__":
  main()
