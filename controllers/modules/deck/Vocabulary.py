

#import Model.deck_model as dm

import controllers.modules.deck.Model_vocab as dm



import random


class Vocabulary:
	__instance = None

	# Virtually private constructor.
	def __init__(self):
		if Vocabulary.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			dm.start_vocabulary_db()
			Vocabulary.__instance = self

	# Static access method. 
	def getInstance():
		if Vocabulary.__instance == None:
			Vocabulary()
		return Vocabulary.__instance


	def set_vocabulary(self,tuple_list):
		dm.set_vocabulary_db(tuple_list)

	def get_vocabulary(self):
		return dm.get_vocabulary_db()

