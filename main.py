#!/usr/env/bin python
# -*- coding: utf-8 -*-

import sys
import math
import codecs

from m_Parser import Parser
from m_Mailer import ImageMailer
from m_Randomizer import Randomizer
from m_PlayersPool import PlayersPool

DEBUG = 1
TEST = 0

if ( len(sys.argv) ) < 2:
	print "Expected file_name of list of names, as a first parameter!"
	sys.exit()
	
file_name = sys.argv[1]
parser = Parser(file_name)
players_pool = PlayersPool()

while True:
	parse_result = parser.ParseNext()
	if (parse_result == Parser.PARSE_OK):
		owner_id = -1
		if (not players_pool.NameExists(parser.ParsedName)):
			owner_id = players_pool.Add(parser.ParsedName, parser.ParsedEmail)
		else:
			owner_id = players_pool.GetNameID(parser.ParsedName)
			players_pool[owner_id].BindEmail(parser.ParsedEmail)
		
		for buddy_name in parser.ParsedBuddies:
			if (not players_pool.NameExists(buddy_name)):
				new_buddy_id = players_pool.Add(buddy_name)
			else:
				new_buddy_id = players_pool.GetNameID(buddy_name)
			players_pool.BindBuddy(owner_id, new_buddy_id)
	else:
		if (parse_result == Parser.PARSE_FINISHED):
			print "All document parsed!"
			break
		if (parse_result == Parser.PARSE_ERROR):
			print "Something went wrong"
			break
	
randomizer = Randomizer(players_pool)

randomization_status = randomizer.RollSantas()
if (randomization_status == Randomizer.ERROR):
	print "Randomization failed!"
	print randomizer.Santas
	sys.exit(1)
else:
	LOG_FILE_NAME = "random.log"
	with codecs.open(LOG_FILE_NAME, "w+", "utf-8") as log_file:
		for santa, reciever in enumerate(randomizer.Santas):
			log_file.write(u"{} is Santa of {}".format(players_pool[santa].Name, players_pool[reciever].Name))
			
			if (reciever in players_pool[santa].Buddies):
				log_file.write(u" (Nice one!)\n")
			else:
				log_file.write(u" (Never lucky)\n")
				
	print LOG_FILE_NAME, "was produced!"

# Uncomment to test with external script
# if (TEST):
# 	sys.exit(0)

if (DEBUG):
	for santa, reciever in enumerate(randomizer.Santas):
		print "{} is Santa of {}".format(players_pool[santa].Name.encode("utf-8"), players_pool[reciever].Name.encode("utf-8")),
		
		if (reciever in players_pool[santa].Buddies):
			print "Nice"
		else:
			print "Never lucky"
	
#Uncomment stuff below, to really send mails
mailer = ImageMailer()
mailer.Connect("smtp.gmail.com", 587)

#in auth file u enter your login and password for mail server(each from new line)
AUTH_FILE_NAME = "auth"
auth_file_content = codecs.open(AUTH_FILE_NAME, "r", "utf-8").readlines()
mailer.Auth(*auth_file_content)

# for santa_id, reciever_id in enumerate(randomizer.Santas):
# 	sender_email = players_pool[santa_id].Email.encode("utf-8")
# 	santa_name = players_pool[santa_id].Name.encode("utf-8")
# 	reciever_name = players_pool[reciever_id].Name.encode("utf-8")
	
# 	mailer.SendMail(sender_email, santa_name, reciever_name)

mailer.SendMail("ne_kit@mail.ua", "Никита", "Николай")