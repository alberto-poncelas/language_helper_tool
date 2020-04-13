# -*- coding: utf-8 -*-



from googletrans import Translator


import itertools
import collections


from janome.tokenizer import Tokenizer as janome_tokenizer



#Get language
def get_language(text):
	translator= Translator()
	return translator.detect(text).lang

#Get pronunciation of list of sentences
def pronunciation(text_list,lang):
	translator= Translator()
	res=[]
	for text in text_list:
		res.append(translator.translate(text, src=lang, dest=lang).pronunciation)
	return res

#Get translation of list of sentences
def translation(text_list,src,trg):
	translator= Translator()
	res=[]
	for text in text_list:
		res.append(translator.translate(text, src=src, dest=trg).text)
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


