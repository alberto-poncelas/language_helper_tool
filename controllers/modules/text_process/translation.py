# -*- coding: utf-8 -*-



from googletrans import Translator


import itertools
import collections
import re

from janome.tokenizer import Tokenizer as janome_tokenizer



def remove_emoji(sentence):
	emoji_pattern = re.compile("["
	        u"\U0001F600-\U0001F64F"  # emoticons
	        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
	        u"\U0001F680-\U0001F6FF"  # transport & map symbols
	        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
	                           "]+", flags=re.UNICODE)
	return emoji_pattern.sub(r'', sentence)


#Get language
def get_language(text):
	translator= Translator()
	return translator.detect(text).lang



def get_pronunciation(translator,sentence,lang):
	try:
		pronunciation=translator.translate(remove_emoji(sentence), src=lang, dest=lang).pronunciation
		return pronunciation
	except:
		print("ERROR in pronunciation")
		return ""



#Get pronunciation of list of sentences
def pronunciation(text_list,lang):
	translator= Translator()
	res=[]
	for text in text_list:
		res.append(get_pronunciation(translator,text,lang))
	return res


def do_translation(translator,sentence,src,trg):
	try:
		translation=translator.translate(remove_emoji(sentence), src=src, dest=trg).text
		return translation
	except:
		print("ERROR in translation")
		return ""



#Get translation of list of sentences
def translation(text_list,src,trg):
	translator= Translator()
	res=[]
	for text in text_list:
		res.append(do_translation(translator,text,src,trg))
	return res




def get_word_counts(lines,translate_into_english_from=""):
	lines_tok=[tokenizer(x,"ja") for x in lines]
	text_tok= list(itertools.chain.from_iterable(lines_tok))
	word_count=collections.Counter(text_tok)
	word_count_dict=dict(word_count)
	word_count_list=[(x,word_count_dict[x]) for x in word_count_dict.keys() if len(x.strip())>0]
	word_count_list_sorted=sorted(word_count_list, key=lambda x: -x[1])
	if len(translate_into_english_from)>0:
		translations=translation([x[0] for x in word_count_list_sorted],translate_into_english_from,"en")
		word_count_list_sorted=[ (w+"\t"+tr,c) for [(w,c),tr] in list(zip(word_count_list_sorted,translations)) ] 
	return word_count_list_sorted



def tokenizer(sentence,lang):
#	if lang=="ja":
	token_object = janome_tokenizer()
	return [x.surface for x in token_object.tokenize(sentence)]


