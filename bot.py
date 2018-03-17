#-*- coding:utf-8 -*-

### Автоматизированной системы онлайн игры «Виселица» "@viselic_bot".
### Разработчики: Лобанов Иван Алексеевич, Россия, г. Москва, РЭУ им. Г. В. Плеханова, ФМЭСИ; Трофимова Ксения Аркадьевна, Россия, г. Москва, РЭУ им. Г. В. Плеханова, ФМЭСИ.
### Версия 1.0.0

### Импорт необходимых дополнительных библиотек
import telebot
import constants
import random
from dictionary import words
from datetime import datetime
bot = telebot.TeleBot(constants.token)
users = {}

### Метод, выводящий всю информацию о пользователе в консоль администратора.
def log(message):
	print(constants.c_1)
	print(datetime.now())
	if (message.text.isupper())== False:
		print('Сообщение от {0} {1}. (id = {2})\nТекст - {3}'.format(message.from_user.first_name,message.from_user.last_name,str(message.from_user.id),message.text))
	else: print(constants.comment_13)
		
### Метод, инициализирующий начало игры.
def initGame(message):
	global users
	GAME_STARTED = True
	word=words[random.randrange(len(words))]
	len_word=len(word)
	health = 7
	test=False
	used_letters=""
	win_word=[]
	for i in range(len(word)):
		win_word+="*"

	users.update({message.chat.id: {'GAME_STARTED': GAME_STARTED, 'word': word, 'len_word': len_word, 'health': health, 'test': test, 'used_letters': used_letters, 'win_word': win_word}})
	bot.send_message(message.chat.id, constants.comment_12)

### Методы, отвечающие на команды.
@bot.message_handler(commands =['greeting'])
def game_vis(message):
	log(message)
	bot.send_message(message.chat.id, constants.comment_1)
	
@bot.message_handler(commands =['settings'])
def game_vis(message):
	log(message)
	bot.send_message(message.chat.id, constants.comment_2 )
	
@bot.message_handler(commands =['regulations'])
def game_vis(message):
	log(message)
	bot.send_message(message.chat.id, constants.comment_3)
        
@bot.message_handler(commands =['help'])
def game_vis(message):
	log(message)
	bot.send_message(message.chat.id, constants.comment_4)
        
@bot.message_handler(commands =['start'])
def game_vis(message):
	log(message)
	bot.send_message(message.chat.id, constants.comment_5)
	if message.text == "/start":
		initGame(message)
	

### Метод, обрабатывющий текст после нажатия команды /start. В нем же описана логика игры.
@bot.message_handler(content_types=['text'])
def asdasd(message):
	log(message)
	global users
	### Создание объектов пользовательской клавиатуры.
	user_markup = telebot.types.ReplyKeyboardMarkup(True)
	user_markup.row('а','б','в','г','д','е','ё','ж')
	user_markup.row('з','и','й','к','л','м','н','о')
	user_markup.row('п','р','с','т','у','ф','х','ц')
	user_markup.row('ч','ш','щ','ъ','ы','ь','э','ю','я')
	bot.send_message(message.chat.id,'\U0001F4AC', reply_markup=user_markup)
	### Проверка данных пользователя.  
	if message.chat.id in users and users[message.chat.id]['GAME_STARTED'] == True: 
		### Проверка количества неотгаданных букв и количество жизней у пользователя. 
		if users[message.chat.id]['len_word'] != 0 and users[message.chat.id]['health'] != 0:
			users[message.chat.id]['test']=False
			letter = message.text
			### Проверка входных данных. 
			if len(letter) == 1 and letter in constants.alfa and letter not in users[message.chat.id]['used_letters']:
				count=0
				### Проверка введенной буквы на нахождение ее в загаданном слове.
				for i in users[message.chat.id]['word']:
					if letter in i:
						users[message.chat.id]['len_word'] -= 1
						users[message.chat.id]['test']=True
						users[message.chat.id]['win_word'][count]=letter
					count+=1
				users[message.chat.id]['used_letters']+=letter
			elif letter not in constants.alfa:
				bot.send_message(message.chat.id, constants.comment_6)
						
			else:
				bot.send_message(message.chat.id, constants.comment_7)
				
			if users[message.chat.id]['test'] == 0 and letter in constants.alfa and letter not in (users[message.chat.id]['win_word']) :
				users[message.chat.id]['health'] -= 1
				bot.send_message(message.chat.id, constants.comment_8)
			if users[message.chat.id]['health']!=0:
				bot.send_message(message.chat.id, constants.s*(users[message.chat.id]['health']))

		print(constants.c_2, users[message.chat.id]['word'], constants.c_6, constants.c_3, users[message.chat.id]['health'], constants.c_6, constants.c_4, users[message.chat.id]['used_letters'], constants.c_6, constants.c_5, users[message.chat.id]['win_word'])		
		bot.send_message(message.chat.id, ''.join(users[message.chat.id]['win_word']))
	
		### Проверка на победу.
		if users[message.chat.id]['len_word'] == 0:
			bot.send_message(message.chat.id, constants.comment_9)
			bot.send_message(message.chat.id, text = constants.b)
			users[message.chat.id]['GAME_STARTED'] = False
			### Сброс всех данных игрока, после окончания игры
			users.pop(message.chat.id)
		
		### Проверка на поражение.
		elif users[message.chat.id]['health'] == 0: 
			bot.send_message(message.chat.id, constants.comment_10)
			bot.send_message(message.chat.id, constants.comment_14)
			bot.send_message(message.chat.id, users[message.chat.id]['word'])
			users[message.chat.id]['GAME_STARTED'] = False
			### Сброс всех данных игрока, после окончания игры
			users.pop(message.chat.id)

		else: bot.send_message(message.chat.id, constants.comment_12)
		

### постоянное обновление списка новых сообщений.
bot.polling(none_stop=True, interval=0)
	

