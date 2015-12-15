# -*- coding:utf-8 -*-

import random

class Randomizer:
	#Defin debug mode
	DEBUG = 0
	
	REQUIRED_PROB = 0.75
	
	ERROR = -1
	CORRECT = 1
	
	def __init__(self,  players_pool):
		self.PlayersPool = players_pool
		
		self.PlayersTotal = len(players_pool.Players)
		self.PlayersQueue = sorted([player for player in self.PlayersPool], key=(lambda p: len(p.Buddies)))
		
	def GetRepetitions(self, buddies_total, variants_total):
		required_non_buddies = Randomizer.REQUIRED_PROB*(variants_total - buddies_total)
		required_buddies = buddies_total - Randomizer.REQUIRED_PROB * buddies_total
		return int(buddies_total * ( required_non_buddies / required_buddies )) 

	def CheckTheSantas(self):
		# Fixes the situation, when last roller got himself
		for i,s in enumerate(self.Santas):
			if (i == s):
				return i
		return -1
		
	def RollSantas(self):
		self.UnboundPlayers = [i for i in range(0, self.PlayersTotal)]
		
		self.Santas = self.PlayersTotal*[-1]
		random.seed()
		
		for player in self.PlayersQueue:
			buddies_pool = [buddy for buddy in player.Buddies if (buddy in self.UnboundPlayers) ]
			buddies_pool_len = len(buddies_pool)
			total_pool_len = len([p for p in self.UnboundPlayers if p != player.ID])
			
			if (Randomizer.DEBUG):
				print "For player: ", player.Name, player.ID
				print "Total: {}; Buddies: {}".format(total_pool_len, buddies_pool_len)
			
			if (total_pool_len == 1):
				random_pool = [p for p in self.UnboundPlayers if p != player.ID]
				self.Santas[player.ID] = random_pool[0]
				self.UnboundPlayers.pop(self.UnboundPlayers.index(random_pool[0]))
				continue
			if (total_pool_len == 0):
				self.Santas[player.ID] = player.ID
				continue
			
			random_pool = []
			if ( ( buddies_pool_len / total_pool_len ) < Randomizer.REQUIRED_PROB ) and (buddies_pool_len > 0) :
				required_repetitions = self.GetRepetitions(buddies_pool_len, total_pool_len)
				
				if (Randomizer.DEBUG):
					print "Required: {}".format(required_repetitions)
					
				multiplication = required_repetitions / buddies_pool_len
				for buddy in buddies_pool:
					random_pool.extend( [buddy] * multiplication )
				excess_repetitions = required_repetitions % buddies_pool_len 
				if (excess_repetitions):
					for i in range(0, excess_repetitions):
						random_pool.append(buddies_pool[random.randrange(0, buddies_pool_len)])
				random_pool.extend([p for p in self.UnboundPlayers if ((p not in buddies_pool) and (p != player.ID) ) ])
					
			else:
				if (Randomizer.DEBUG):
					print "Satisfies the brobability!"
				random_pool = [ p for p in self.UnboundPlayers if (p != player.ID) ]
			
			random.shuffle(random_pool)
			chosen = random_pool[random.randrange(0, len(random_pool))]
			self.Santas[player.ID] = chosen
			
			if (Randomizer.DEBUG):
				print "B4 shuffle:", random_pool	
				print "Pool: ", random_pool
				print "Got: ", chosen
				
				print "Unbound: ", self.UnboundPlayers
				print "Eliminated(index): ", self.UnboundPlayers.index(chosen)
				
			self.UnboundPlayers.pop(self.UnboundPlayers.index(chosen))
		
		#Check the non-varinat situation	
		problem_index = self.CheckTheSantas()
		if (problem_index != -1):
			buddies_pool = self.PlayersPool[problem_index].Buddies
			random.shuffle(buddies_pool)
			chosen = buddies_pool[random.randrange(0, len(buddies_pool))]
			self.Santas[problem_index] = self.Santas[chosen]
			self.Santas[chosen] = problem_index
			
			print "Non-variant solved"
			if (self.CheckTheSantas() == -1):
				print "Control check success!"
			else:
				print "GG WP, delete the Dota"
				return Randomizer.ERROR
				
			if (Randomizer.DEBUG):
				print "{} swapped with {}(got {})".format(problem_index, chosen, self.Santas[chosen])
				print "Problem is fixed!"
		
		
		check_correct = len(set(self.PlayersPool)) == len(set(self.Santas))
		if (check_correct):
			print "Randomization was correct!"
			return Randomizer.CORRECT
		else:
			print "Something went wrong!"
			return Randomizer.ERROR
			
			
		