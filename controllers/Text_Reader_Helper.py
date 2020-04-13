# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request, redirect, url_for
import random


from flask import Blueprint
text_reader_helper_api = Blueprint('text_reader_helper_api', __name__)



import controllers.modules.text_process.translation as tp



@text_reader_helper_api.route('/text_read')
def text_read_helper():
	return render_template('text_read_helper/text_reader.html')



@text_reader_helper_api.route('/text_reader_results', methods=[ 'POST'])
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
		#"pronunciation": pronunciation, #"\n".join(pronunciation),
		"word_count": "\n".join(word_count)}
	if lines[0]!=pronunciation[0]:
		result["pronunciation"]=pronunciation
	return render_template('text_read_helper/text_reader_results.html',result=result)

