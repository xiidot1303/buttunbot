import telebot
from telebot import types
import telegram
import os
import youtube_dl
from video_utils import Video
import random
client = telebot.TeleBot('1392923431:AAGZ88Zs5S2W1gDurRIicQVuweaFqfMbByI')

alp = 'qwertyuioplkjhgfdsazxcvbnm'


@client.message_handler(commands = ['get_info', 'info'])

def get_user_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text = 'yes!', callback_data='yes')
    item_no = types.InlineKeyboardButton(text = 'No!', callback_data='no')
    markup_inline.add(item_yes, item_no)
    client.send_message(message.chat.id, "do you want to get inf about us?", reply_markup = markup_inline)


@client.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == 'yesa':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_id = types.KeyboardButton('my id')
        item_username = types.KeyboardButton('my name')
        item_home = types.KeyboardButton('Home')

        markup_reply.add(item_id, item_username, item_home)
        client.send_message(call.message.chat.id, "enter a button", reply_markup = markup_reply) 
    elif call.data == 'no':
        pass
   
    if call.data == 'yes':
        try:
            content = types.InputTextMessageContent("https://www.youtube.com/watch?v=kt9pELoqzkw")
            r = types.InlineQueryResultVideo('video', '124323', 'text/html', 'https://core.telegram.org/file/811140016/2/2b_B7nq9OQA/161b06d38843930fe5','Title', content)
            print('yea')
            client.answer_inline_query(call.id, [r])
        except Exception as e:
            print(e)


@client.message_handler(content_types = ['text'])

def get_text(message):
    
    if message.entities:             # Работа со ссылками pkanal = 6
        for item in message.entities:
            if item.type == "url" and message.text.find('  ') == -1:
                if 'youtube.com' in message.text or 'youtu.be' in message.text:           #  Загружаем с Ютуб
                    doc = random.choices(alp, k=10)
                    ydl_opts = {'outtmpl': '/tmp/{}.mp4'.format(doc), 'preferredcodec': 'mp4', 'max_filesize': 600000000000000, 'resolution': 160}
                    
                    link_of_the_video = message.text
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([link_of_the_video])
                    client.delete_message(message.chat.id, message.message_id)

                    #if os.path.exists('/tmp/f.mp4'):  # файл есть
                    client.send_chat_action(chat_id=message.chat.id, action=telegram.chataction.ChatAction.TYPING)
                    video = open('D:\\x\\XIIdot\\python\\bots\\buttun bot\\tmp\\{}.mp4'.format(doc), 'rb')
                    client.send_video(message.chat.id, video)
                    #os.remove('D:\\x\\XIIdot\\python\\bots\\buttun bot\\tmp\\{}.mp4'.format(doc))
                    pkanal = 6
                    #else:       # файла нет
                        #client.send_message(message.chat.id, 'Слишком большой файл', parse_mode='html', disable_web_page_preview=True)    
    

    if message.text == 'photo':
        client.send_photo(message.chat.id, 'https://www.nationalgeographic.com/content/dam/photography/rights-exempt/best-of-photo-of-the-day/2018/june/03_best-pod-june-18.ngsversion.1531168256893.adapt.1900.1.jpg')
    if message.text == 'shaha':
        client.send_message(message.chat.id, f'Yes I am')
    elif message.text == 'my id':
        client.send_message(message.chat.id, f'Your ID: {message.from_user.id}')
    elif message.text == 'my name':
        client.send_message(message.chat.id, f'Your name: {message.from_user.first_name}')

    if message.text == 'Home':
        markup_home = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_sticker = types.KeyboardButton('Sticker')
        markup_home.add(item_sticker)

        client.send_message(message.chat.id, 'Home', reply_markup=markup_home)


@client.message_handler(content_types = ['sticker'])
def get_sticker(message):
    client.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJpu19Ejk2a7Hk48RUlW1p5XvLQZEcqAALGBgACRvusBNj-1yvTm2cNGwQ')
    client.send_chat_action(chat_id=message.chat.id, action=telegram.chataction.ChatAction.TYPING)
    markup_location_and_contact = types.ReplyKeyboardMarkup()
    get_location = telegram.KeyboardButton(text='Send location', request_location=True)
    get_contact = telegram.KeyboardButton(text='Send contact', request_contact=True)
    markup_location_and_contact.add(get_contact, get_location)
    client.send_message(message.chat.id, 'You must send your contact and location', reply_markup=markup_location_and_contact)

# @bot.inline_handler(lambda query: query.query == 'video')

 







client.polling()



