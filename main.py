#pingwinka
import telebot
import modules.replys as replys
import modules.PO as pidoraOtvet
import modules.welcomToTheClub as welcomeToTheClub
import cache
import config
import time
import modules.gayRadar as gayRadar
import modules.bottle as bottle
import modules.randomVoice as randomVoice
import random

API_KEY = config.token
bot = telebot.TeleBot(API_KEY)
bot.set_webhook()

fingersList = ['🤙','👍','👈','👉','👆','🖕','👇','☝']

andreiID = 355407137

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
  bot.reply_to(message,'Спасибо за голосовое, петушара.👆',parse_mode='HTML')

@bot.message_handler(content_types=["new_chat_members"])
def foo(message):
  tempDateStamp = int(time.time())
  welcomeToTheClub.welcomToTheClub(bot,message,tempDateStamp)

@bot.message_handler(commands=['radar'])
def radar(message):
  gayRadar.gayRadarStart(bot,message, True)

@bot.message_handler(commands=['score'])
def radar(message):
  gayRadar.score(bot,message)

@bot.message_handler(commands=['radarReset'])
def radarReset(message):
  if message.from_user.id == andreiID:
    cache.pidorOfDay = ''
    cache.pidorOfDayDate = ''
    bot.send_message(message.chat.id, 'Ты опустошил мой бак...')

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

@bot.message_handler(commands=['scoreReset'])
def radarReset(message):
  cache.radarScoreStartingAt = ''
  cache.pidorOfDay = ''
  cache.pidorOfDayDate = ''
  if message.from_user.id == andreiID:
    for i in range(len(cache.chatUsers)):
      cache.chatUsers[i]['score'] = 0
    for i in range(len(cache.chatUsers)):
      cache.chatUsers[i]['total_messages'] = 0
    bot.send_message(message.chat.id, 'Ты опустошил мой бак...')

@bot.message_handler(commands=['chatUsersLen'])
def radarReset(message):
  if message.from_user.id == andreiID:
    bot.send_message(message.chat.id, len(cache.chatUsers))

@bot.message_handler()
def handle_message(message):
  tempDateStamp = int(time.time())

  if len(cache.chatUsers) < 7:
    if message.from_user.id != bot.user.id:
      if not any(d['id'] == message.from_user.id for d in cache.chatUsers):
        cache.chatUsers.append({'id':message.from_user.id,'username':message.from_user.username,'first_name':message.from_user.first_name,'last_name':message.from_user.last_name,'score':0,'total_messages':0})
  if cache.chatUsers != '':
    messageFromUser = ''
    messageFromUser = cache.chatUsers[find(cache.chatUsers,'id',message.from_user.id)]
    messageFromUser['total_messages'] = messageFromUser['total_messages'] + 1

  if gayRadar.radarCheckDate() and gayRadar.radarCheckHour():
    gayRadar.gayRadarStart(bot, message, False)
  
  if message.date - cache.lastBotMessageTime > cache.botTimeOut:
    if message.reply_to_message:
#agro answer
      if message.reply_to_message.from_user.id == bot.user.id:
        if message.reply_to_message.text == 'Хуй на.🤣':
          bot.reply_to(message, "Возьми два.🤣🤣🤣")
          cache.lastBotMessageTime = tempDateStamp
        else:
          if message.from_user.id == 867353082:
            vadimRand = random.randint(1,5)
            if vadimRand == 1:
              bot.send_message(message.chat.id, 'Ай, Вадим, иди нахуй.', reply_to_message_id=message.id)
              cache.lastBotMessageTime = tempDateStamp
            else:
              replys.replyFunc(bot,message,tempDateStamp)
          else:
            replys.replyFunc(bot,message,tempDateStamp)
#billy triger
    if any(ext in message.text.lower() for ext in replys.trigers):
      replys.replyFunc(bot,message,tempDateStamp)
#pidora otvet
    if message.text.lower() in pidoraOtvet.pidoraOtvietList:
      pidoraOtvet.pidoraOtviet(bot,message,tempDateStamp)
#huina
    if message.text.lower() in pidoraOtvet.daList:
      pidoraOtvet.daOtvet(bot,message,tempDateStamp)
#cs
    if message.text.lower() in pidoraOtvet.csListTriger:
      pidoraOtvet.csOtvet(bot,message,tempDateStamp)
#palec
    if any(ext in message.text for ext in fingersList):
      bot.reply_to(message,'Ох, блять, какой палец, его бы мне в жопу.')
      cache.lastBotMessageTime = tempDateStamp
#welcomeToTheClub pidor
    if any(ext in message.text.lower() for ext in welcomeToTheClub.pidorList):
      welcomeToTheClub.welcomToTheClub(bot,message,tempDateStamp)
#bottle
    if any(ext in message.text.lower() for ext in bottle.bottleList):
      bottle.sitOnBottle(bot,message,tempDateStamp)
    
#celebrate
    if "@Spermobakibot" in message.text:
      bot.send_message(message.chat.id, "Let's celebrate and suck some dick!")
      cache.lastBotMessageTime = tempDateStamp
#voice
    if (random.randint(1,120) == 69):
      randomVoice.randomVoicePlay(bot,message)

bot.polling(non_stop=True)
