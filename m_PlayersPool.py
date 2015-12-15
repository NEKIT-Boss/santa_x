# -*- coding:utf-8 -*-


class Player:
	def __init__(self, ID, name, email=""):
		self.Name = name
		self.Email = email
		self.ID = ID
		
		#Will contain buddy id
		self.Buddies = []
		
	def BindEmail(self, email):
		self.Email = email
	
	def AddBuddy(self, buddy_id):
		self.Buddies.append(buddy_id)
		

class PlayersPool:
	def __init__(self):
		self.Players = []
		self.GeneratedID = -1
		
	def GenerateID(self):
		self.GeneratedID+=1
		return self.GeneratedID
		
	def Add(self, name, email=""):
		self.Players.append(Player(self.GenerateID(), name, email))
		return (len(self.Players) - 1)

	def NamesPool(self):
		for player in self.Players:
			yield player.Name

	def NameExists(self, name):
		if (name in self.NamesPool()):
			return True
		else:
			return False
		
	def GetNameID(self, name):
		for iter_number, iter_name in enumerate(self.NamesPool()):
			if (iter_name == name):
				return iter_number
		return -1
	
	def BindBuddy(self, player_id, buddy_id):
		#It is known, that ID exist
		self.Players[player_id].AddBuddy(buddy_id)
		
	def __getitem__(self, index):
		return self.Players[index]
		