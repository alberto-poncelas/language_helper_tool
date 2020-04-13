


import controllers.modules.deck.Model_vocab as dm


import random


class Deck:
	__instance = None
	card_list=[]

	# Virtually private constructor.
	def __init__(self):
		if Deck.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			self.card_list=dm.start_deck_db()
			Deck.__instance = self

	# Static access method. 
	def getInstance():
		if Deck.__instance == None:
			Deck()
		return Deck.__instance


	def set_cards(self,id_list):
		dm.insert_deck_db(id_list)
		self.card_list=dm.get_cards_db()

	def get_cards(self):
		return self.card_list

	def print_deck(self):
		print("Show "+str(len(self.card_list))+" cards:")
		for c in self.card_list:
			print(c)

	def get_QandA(self,num_alternatives):
		num_alternatives=min(num_alternatives,len(self.card_list))
		pairs2=list(self.card_list)
		random.shuffle(pairs2)
		q=pairs2[0][1]
		a=pairs2[0][2]
		altern=[x[2] for x in pairs2[0:num_alternatives]]
		random.shuffle(altern)
		return [q,a,altern]


