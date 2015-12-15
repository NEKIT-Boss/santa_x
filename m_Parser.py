#!/usr/env/bin python
# -*- coding: utf-8 -*-

from m_NamesTable import NamesTable

import os
import re
import codecs

class Parser:
	#Defines whether it is required to write output
	DEBUG = 1
	
	PARSE_OK = 1
	PARSE_ERROR = 0
	PARSE_FINISHED = -1
	
	LinePattern = re.compile(r".+\s*\((.+@.+)\)\s*:\s*(\s*.+\s*)+")
	NameEmailPattern = re.compile(r"(.+)\s*\((.+@.+)\)") 
	
	def __init__(self, file_name):
		if not os.path.exists(file_name):
			print "No \"{}\" file found!".format(file_name)
			raise Exception("Trouble")		
		
		self.File = codecs.open(file_name, "r", "utf-8")
		self.ParsedName = ""
		self.ParsedEmail = ""
		self.ParsedBuddies = []
		
	def ParseNext(self):
		line_read = self.File.readline()
		
		if (line_read == ""):
			return Parser.PARSE_FINISHED
			
		if (Parser.LinePattern.match(line_read)):
			smc_split = line_read.split(":")
			
			left_part = smc_split[0].strip()
			NameEmailMatch = Parser.NameEmailPattern.match(left_part)
			if (NameEmailMatch):
				self.ParsedName = NameEmailMatch.group(1).strip()
				self.ParsedEmail = NameEmailMatch.group(2).strip()
			else:
				return PARSE_ERROR
			
			right_part = smc_split[1].strip()
			self.ParsedBuddies = re.split("\s*[.*]*\s*", right_part)
			return Parser.PARSE_OK
		else:
			print "Line does not match!"
			self.ParsedName = ""
			self.ParsedEmail = ""
			self.ParsedBuddies = []
			return Parser.PARSE_ERROR