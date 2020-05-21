# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, redirect, url_for
import random


from flask import Blueprint
text_getter_api = Blueprint('text_getter_api', __name__)



import controllers.modules.text_process.translation as tp
from twython import Twython




import configparser
config = configparser.ConfigParser()

config.read("config/twitter_config")


CONSUMER_KEY = config['TWITTER']['CONSUMER_KEY']
CONSUMER_SECRET = config['TWITTER']['CONSUMER_SECRET']
OAUTH_TOKEN = config['TWITTER']['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = config['TWITTER']['OAUTH_TOKEN_SECRET']


twitter = Twython(
    CONSUMER_KEY, CONSUMER_SECRET,
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)




def get_sentences_from_twitter(terms,language):
	res_list=[]
	results=twitter.search(q=terms,count='100',lang=language,include_entities='true')
	for result in results['statuses']:
		tweet_text = result['text'] #.replace("\n"," ")#.encode("utf-8")
		if len(tweet_text.strip())>0 and len(tweet_text.strip())<80:
			res_list.append(tweet_text)
	lengths=[len(x) for x in res_list]
	ordered=sorted(zip(res_list,lengths), key=lambda x: x[1])
	res=[x[0] for x in ordered]
	return res


def get_top_lines(term,lines,lang):
	NUM_SENT=15
	lines_with_val=[]
	wc_dict=dict(tp.get_word_counts(lines))
	for line in lines:
		if term in line:
			words_line=tp.tokenizer(line,lang)
			sent_val=min([wc_dict.get(x,9999999) for x in words_line])
			lines_with_val.append([line,sent_val])
	ordered=sorted(lines_with_val, key=lambda x: -x[1])
	res=[x[0] for x in ordered[0:NUM_SENT]]
	return res


@text_getter_api.route('/text_getter')
def text_getter():
	return render_template('text_read_helper/text_getter.html')


@text_getter_api.route('/text_getter_results', methods=[ 'POST'])
def text_getter_results():
	print(request.form)
	terms = request.form.get('terms')
	lang = request.form.get('lang',"")
	if lang=="":
		lang = tp.get_language(" ".join(terms))
	print(lang)
	if request.files and request.files['sentences_file']:
		f = request.files['sentences_file']
		file_lines=f.read().decode('utf-8')
		lines=get_top_lines(terms,file_lines.split("\n"),lang)
	else:
		lines = get_sentences_from_twitter(terms,lang)
	print(lines)
	translated = tp.translation(lines,lang,"en")
	pronunciation = tp.pronunciation(lines,lang)
	result={
		"text_size": len(lines),
		"text": lines, #"\n".join(lines),
		"translated": translated
		}
	if len(lines)>0 and lines[0]!=pronunciation[0]:
		result["pronunciation"]=pronunciation
	return render_template('text_read_helper/text_reader_results.html',result=result)






@text_getter_api.route('/text_getter_results', methods=[ 'POST'])
def read_text():
	text = request.form.get('text_to_analize')
	lines_raw=text.strip().split("\n")
	lines = [x.strip() for x in lines_raw if len(x.strip())>0]
	lang = tp.get_language(lines[0])
	translated = tp.translation(lines,lang,"en")
	pronunciation = tp.pronunciation(lines,lang)
	word_count_list = tp.get_word_counts(lines,lang)
	word_count = [x[0]+"\t"+str(x[1]) for x in word_count_list]
	result={
		"text_size": len(lines),
		"text": lines, #"\n".join(lines),
		"translated": translated, #"\n".join(translated),
		"word_count": "\n".join(word_count)}
	if lines[0]!=pronunciation[0]:
		result["pronunciation"]=pronunciation
	return render_template('text_read_helper/text_reader_results.html',result=result)

