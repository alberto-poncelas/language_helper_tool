

import sqlite3

database_name='database/vocab.db'

#### VOCABULARY

def start_vocabulary_db():
	try:
		conn = sqlite3.connect(database_name, timeout=10)
		#conn.execute('DROP TABLE IF EXISTS deck')
		conn.execute('CREATE TABLE IF NOT EXISTS vocabulary (id_word TEXT, src_word TEXT, trg_word TEXT)')
		conn.commit()
		conn.close()
		return get_cards_db()
	except:
		print("Error creating VOCABULARY table")
		conn.rollback()
		return False



def set_vocabulary_db(tuple_list):
	#create_vocabulary_db()
	try:
		conn = sqlite3.connect(database_name, timeout=10)
		conn.execute('DELETE FROM vocabulary')
		conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
		cur = conn.cursor()
		for i in range(len(tuple_list)):
			[src_word,trg_word] = tuple_list[i]
			cur.execute("INSERT INTO vocabulary (id_word,src_word,trg_word) VALUES (?,?,?)",(str(i),src_word,trg_word) )
		conn.commit()
		conn.close()
		return True
	except:
		print("Error loading VOCABULARY table")
		conn.rollback()
		return False



def get_vocabulary_db():
	try:
		conn = sqlite3.connect(database_name)
		cur = conn.cursor()
		cur.execute("SELECT * FROM vocabulary")
		rows = cur.fetchall();
		conn.close()
		return rows
	except:
		conn.rollback()
		return []



#### DECK

def start_deck_db():
	try:
		conn = sqlite3.connect(database_name, timeout=10)
		#conn.execute('DROP TABLE IF EXISTS deck')
		conn.execute('CREATE TABLE IF NOT EXISTS deck (id_word TEXT, src_word TEXT, trg_word TEXT)')
		conn.commit()
		conn.close()
		return get_cards_db()
	except:
		print("Error creating DECK table")
		conn.rollback()
		return False


#Create table
def insert_deck_db(id_list):
	start_deck_db() #Restart deck
	id_list_str= ", ".join([str(x) for x in id_list])
	try:
		conn = sqlite3.connect(database_name, timeout=10)
		conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
		conn.execute('DELETE FROM deck')
		conn.execute('INSERT INTO deck SELECT * FROM vocabulary WHERE vocabulary.id_word IN ('+id_list_str+')')
		conn.commit()
		conn.close()
		return True
	except:
		print("Error inserting in DECK table")
		conn.rollback()
		return False



def get_cards_db():
	try:
		conn = sqlite3.connect(database_name, timeout=10)
		cur = conn.cursor()
		cur.execute("SELECT * FROM deck")
		rows = cur.fetchall();
		conn.close()
		return rows
	except:
		print("Error obtaining cards from DECK table")
		conn.rollback()
		return []


