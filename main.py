# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: azulbukh <azulbukh@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/11/06 18:55:18 by azulbukh          #+#    #+#              #
#    Updated: 2018/11/06 22:58:00 by azulbukh         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import base64
from github import Github
from github import InputGitTreeElement
import config
import telebot
from flask import Flask, request
import logging
import os

bot = telebot.TeleBot(config.token)

def push_to_git():
	g = Github(config.user, config.password)
	repo = g.get_user().get_repo('KazHackStan_References')
	file_list = [
		'./readme/README.md'
	]
	file_names = [
		'README.md',
	]
	commit_message = '[edit][README.md]'
	master_ref = repo.get_git_ref('heads/master')
	master_sha = master_ref.object.sha
	base_tree = repo.get_git_tree(master_sha)
	element_list = list()
	for i, entry in enumerate(file_list):
		with open(entry) as input_file:
			data = input_file.read()
		if entry.endswith('.png'):
			data = base64.b64encode(data)
		element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
		element_list.append(element)
	tree = repo.create_git_tree(element_list, base_tree)
	parent = repo.get_git_commit(master_sha)
	commit = repo.create_git_commit(commit_message, tree, [parent])
	master_ref.edit(commit.sha)

def	edit_file(mes):
	with open("./readme/README.md", "a") as f:
		s = ' '.join(mes[2:])
		f.write("* [" + s + "](" + mes[1] + ")\n")

@bot.message_handler(commands=['add'])
def add(message):
	print(message)
	mes = message.text.split("\n")
	for i in mes:
		line = i.split(" ")
		if (len(line) == 2):
			edit_file(line)
		else:
			print("nope")
	# push_to_git()
	bot.reply_to(message, 'saved? https://github.com/Zulbukharov/KazHackStan_References')

if "HEROKU" in list(os.environ.keys()):
	logger = telebot.logger
	telebot.logger.setLevel(logging.INFO)
	server = Flask(__name__)
	@server.route("/bot", methods=['POST'])
	def getMessage():
		bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
		return "!", 200
	@server.route("/")
	def webhook():
		bot.remove_webhook()
		bot.set_webhook(url="https://intense-sierra-53637.herokuapp.com/bot")
		return "?", 200
	server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
	bot.remove_webhook()
	bot.polling(none_stop=True)