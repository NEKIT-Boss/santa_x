# -*- coding: utf-8 -*-

import cairo
import codecs
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

class ImageMailer:
	#defines whther it is to run in debug mode
	DEBUG = 0
	
	def __init__(self):
		self.Subject = "{}, узнай, кто выпал тебе!"
		self.SenderName = "Secret Santa"
		self.ImagePatternFileName = "santa.png"
		self.Server = None
	
	def Connect(self, server_smtp, port):
		self.Server = smtplib.SMTP(server_smtp, port)
		
		if (ImageMailer.DEBUG):
			self.Server.set_debuglevel(True)
		
		self.Server.ehlo()
		self.Server.starttls()
		self.Server.ehlo()
		
	def Auth(self, login, password):
		if (self.Server):
			self.Server.login(login, password)
			self.Sender = login
			return 0
		else:
			return -1
			
	def ComposeImage(self, santa_name, reciever_name):
		letter_image = cairo.ImageSurface.create_from_png(self.ImagePatternFileName)
		
		context = cairo.Context(letter_image)
		
		line1_start = (475, 555)
		context.set_source_rgb(0.1, 0.1, 0.2)
		context.select_font_face("Comic Sans MS", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
		context.set_font_size(36)
		
		context.move_to(*line1_start)
		context.show_text(santa_name+"!")
		
		line2_start = (500,615)
		context.move_to(*line2_start)
		context.show_text("Тебе выпал:")
		
		(text_x, text_y, text_width, text_height, dx, dy) = context.text_extents(reciever_name)
		line3_end = (810,670)
		context.move_to(line3_end[0] - text_width, line3_end[1])
		context.show_text(reciever_name)
		
		letter_image.flush()
		result_file_name = "result.png"
		letter_image.write_to_png(result_file_name)
		return result_file_name

	def ComposeLetter(self, reciever_email, santa_name, reciever_name ):
		#With HTML support means "related"
		message_root = MIMEMultipart("related")
		message_root['Subject'] = self.Subject.format(santa_name)
		message_root['From'] = self.SenderName
		message_root['To'] = reciever_email
		
		alternate = MIMEMultipart('alternative')
		message_root.attach(alternate)

		plain_text = MIMEText("Тебе выпал: {}".format(reciever_name), "", "utf-8")
		alternate.attach(plain_text)
		
		html_pattern_file_name = "letter_pattern.html"
		html_pattern_file =  codecs.open(html_pattern_file_name, "r", "utf-8")
		html_pattern = html_pattern_file.read()
		html_pattern_file.close()	
			
		html_message = MIMEText(html_pattern, "html", "utf-8")
		alternate.attach(html_message)
		
		image_file_name = self.ComposeImage(santa_name, reciever_name)
		image_file = open(image_file_name, "rb")
		message_image = MIMEImage(image_file.read())
		image_file.close()
		
		message_image.add_header("Content-ID", "<main_image>")
		message_root.attach(message_image)
		
		return message_root
		
	def SendMail(self, to_email, santa_name, reciever_name):
		if (not self.Server):
			print "Server problem"
			return
		
		message_to_send = self.ComposeLetter(to_email, santa_name, reciever_name)
		try:		
			self.Server.sendmail(self.Sender, to_email, message_to_send.as_string())
			print "Sent to", to_email
		except:
			print "Trouble sending"
	